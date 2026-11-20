#!/usr/bin/env python3
"""Metadata-only, low-rate source watch. External edits become REVIEW_REQUIRED, never facts.

This job never copies article contents, images or untrusted remote instructions.
A forbidden/blocked API response is recorded as ACCESS_BLOCKED, not as a revision.
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import pathlib
import urllib.error
import urllib.parse
import urllib.request

ROOT=pathlib.Path(__file__).resolve().parents[1]
STATE=ROOT/"sourcing/watch-state.json"
BACKLOG=ROOT/"sourcing/change-backlog.csv"
REPORT=ROOT/"sourcing/watch-report.json"
FIELDS=["event_id","source_id","franchise_id","page_url","previous_version",
        "new_version","detected_utc","status"]
UA="Barnskoj-SourceWatch/0.1 (+https://github.com/Hybrismannen/Barnskoj; metadata-only)"
TIMEOUT=6
def load(p):
    with p.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
def serial_csv(rows):
    out=io.StringIO(newline="")
    wr=csv.DictWriter(out,fieldnames=FIELDS,quoting=csv.QUOTE_ALL,lineterminator="\n")
    wr.writeheader()
    for r in rows: wr.writerow(r)
    return out.getvalue()
def build_api_endpoint(source):
    url=urllib.parse.urlparse(source["page_url"])
    if url.scheme!="https" or not url.hostname:
        raise ValueError("Non-HTTPS/unexpected source")
    host=url.hostname
    # These domains are edited in the repo, NOT provided by responses.
    if host.endswith(".fandom.com"):
        api="https://"+host+"/api.php"
    elif host in ("tolkiengateway.net","bulbapedia.bulbagarden.net"):
        api="https://"+host+"/w/api.php"
    elif host=="awoiaf.westeros.org":
        api="https://"+host+"/api.php"
    else:
        raise ValueError("No approved MediaWiki API host: "+host)
    params=urllib.parse.urlencode({
        "action":"query","prop":"revisions","rvprop":"ids|timestamp",
        "titles":source["page_title"],"format":"json","formatversion":2,
        "redirects":1,"maxlag":5
    })
    return api+"?"+params
def fetch_version(source):
    mode=source["watch_mode"]
    if mode=="manual":
        return None,"MANUAL_REVIEW_REQUIRED"
    target=build_api_endpoint(source) if mode=="mediawiki" else source["page_url"]
    parsed=urllib.parse.urlparse(target)
    orig=urllib.parse.urlparse(source["page_url"])
    if parsed.scheme!="https" or parsed.hostname!=orig.hostname:
        raise ValueError("Unexpected redirectable host")
    request=urllib.request.Request(target,headers={"User-Agent":UA,"Accept":"application/json" if mode=="mediawiki" else "*/*"},
                                   method="GET" if mode=="mediawiki" else "HEAD")
    try:
        with urllib.request.urlopen(request,timeout=TIMEOUT) as resp:
            if urllib.parse.urlparse(resp.geturl()).hostname!=orig.hostname:
                return None,"CROSS_HOST_REDIRECT_BLOCKED"
            if mode=="mediawiki":
                if "json" not in resp.headers.get("Content-Type",""):
                    return None,"BAD_CONTENT_TYPE"
                data=json.loads(resp.read(256000).decode("utf-8"))
                pages=data.get("query",{}).get("pages",[])
                if not pages or pages[0].get("missing"):
                    return None,"PAGE_NOT_FOUND"
                rev=pages[0].get("revisions",[])
                if not rev: return None,"NO_REVISIONS"
                return str(rev[0]["revid"]),"OBSERVED"
            # Avoid hashing dynamic HTML or storing copyrighted bodies.
            stamp=resp.headers.get("ETag") or resp.headers.get("Last-Modified")
            if not stamp: return None,"NO_STABLE_HEADER"
            return stamp,"OBSERVED"
    except urllib.error.HTTPError as exc:
        return None,("ACCESS_BLOCKED" if exc.code in (401,403,429,451) else "HTTP_"+str(exc.code))
    except (urllib.error.URLError,TimeoutError,OSError,ValueError,KeyError,json.JSONDecodeError):
        return None,"NETWORK_UNAVAILABLE"
def merge_observation(sources,state,events,observations,now):
    """Pure state transition, safely unit-testable without network."""
    past=dict(state.get("sources",{}))
    changed=[]
    event_ids={e["event_id"] for e in events}
    for source in sources:
        sid=source["source_id"]
        result=observations.get(sid)
        if not result: continue
        version,status=result
        prev=dict(past.get(sid,{}))
        prev["last_attempt_utc"]=now
        prev["fetch_status"]=status
        if status=="OBSERVED" and version:
            prior=prev.get("version","")
            if prior and prior!=version:
                stable="|".join((sid,prior,version))
                uid="SRC-CHANGE-"+hashlib.sha256(stable.encode()).hexdigest()[:16]
                if uid not in event_ids:
                    changed.append({"event_id":uid,"source_id":sid,
                                    "franchise_id":source["franchise_id"],
                                    "page_url":source["page_url"],"previous_version":prior,
                                    "new_version":version,"detected_utc":now,
                                    "status":"REVIEW_REQUIRED"})
                    event_ids.add(uid)
            prev["version"]=version
            prev["last_observed_utc"]=now
        past[sid]=prev
    return {"schema":"barnskoj.sourcewatch/v1","sources":past}, events+changed,changed
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--network",action="store_true",help="Use external network for metadata checks only")
    p.add_argument("--max-pages",type=int,default=26)
    p.add_argument("--check-fixture",action="store_true",help="Run deterministic offline mutation check")
    args=p.parse_args()
    if args.check_fixture:
        sample={"source_id":"WIK-TEST-001","franchise_id":"TEST","page_url":"https://example.org/test"}
        t1,q1,c1=merge_observation([sample],{"sources":{}},[],{"WIK-TEST-001":("100","OBSERVED")},"2026-11-20T00:00:00Z")
        t2,q2,c2=merge_observation([sample],t1,q1,{"WIK-TEST-001":("101","OBSERVED")},"2026-11-21T00:00:00Z")
        t3,q3,c3=merge_observation([sample],t2,q2,{"WIK-TEST-001":(None,"ACCESS_BLOCKED")},"2026-11-22T00:00:00Z")
        assert not c1 and len(c2)==1 and c2[0]["status"]=="REVIEW_REQUIRED"
        assert len(q3)==1 and not c3 and t3["sources"]["WIK-TEST-001"]["version"]=="101"
        print("PASS: baseline only, revision queues review, 403/429 never erases evidence")
        return 0
    if not args.network:
        print("No external access without --network. Use --check-fixture for offline tests.")
        return 0
    sources=load(ROOT/"sourcing/wiki_sources.csv")
    state=json.loads(STATE.read_text(encoding="utf-8"))
    events=load(BACKLOG)
    targets=sources[:max(0,args.max_pages)]
    observations={}
    for source in targets:
        observations[source["source_id"]]=fetch_version(source)
    now=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
    latest,new_events,changed=merge_observation(targets,state,events,observations,now)
    STATE.write_text(json.dumps(latest,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    BACKLOG.write_text(serial_csv(new_events),encoding="utf-8")
    status={v[1]:sum(1 for x in observations.values() if x[1]==v[1]) for v in observations.values()}
    summary={"checked_attempts":len(targets),"new_review_events":len(changed),
             "pending_review_events":sum(x["status"]=="REVIEW_REQUIRED" for x in new_events),
             "statuses":dict(sorted(status.items())),"checked_utc":now,
             "unobserved_sources":len(sources)-len(targets)}
    REPORT.write_text(json.dumps(summary,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__":
    raise SystemExit(main())
