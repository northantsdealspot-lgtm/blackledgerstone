#!/usr/bin/env python3
import json, re, time, hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'config/raven_sources.json').read_text(encoding='utf-8'))
OUT=ROOT/'data/leads.json'
UA='BlackLedgerStone-RavenScout/3.0 (+public property intelligence; contact via repo)'


def clean(s): return re.sub(r'\s+',' ',s or '').strip()
def uid(source,url,text): return hashlib.sha1(f'{source}|{url}|{text[:120]}'.encode()).hexdigest()[:16]

def score(text,source_weight):
    t=text.lower(); s=source_weight; signals=[]
    for group, pts in [('motivation',7),('development',4),('public',5)]:
        for k in CFG['keywords'][group]:
            if k in t:
                s+=pts; signals.append(k)
    return min(100,s), sorted(set(signals))[:12]

def scan_source(src):
    rows=[]
    try:
        r=requests.get(src['url'],headers={'User-Agent':UA},timeout=20)
        r.raise_for_status()
        soup=BeautifulSoup(r.text,'html.parser')
        seen=set()
        for a in soup.find_all('a', href=True):
            txt=clean(a.get_text(' ',strip=True))
            href=urljoin(src['url'],a['href'])
            blob=f'{txt} {href}'
            sc,sigs=score(blob,src.get('weight',10))
            if not sigs or len(txt)<8 or href in seen: continue
            seen.add(href)
            rows.append({
              'id':uid(src['name'],href,txt),'title':txt[:220],'url':href,
              'source':src['name'],'country':src['country'],'category':src['category'],
              'score':sc,'signals':sigs,'discovered':datetime.now(timezone.utc).isoformat(),
              'status':'new','evidence':'Public web page link; verify availability, ownership, price, title and planning before treating as a deal.'
            })
        rows=sorted(rows,key=lambda x:x['score'],reverse=True)[:40]
        return rows, None
    except Exception as e:
        return [], f'{type(e).__name__}: {e}'

def main():
    leads=[]; health=[]
    for src in CFG['sources']:
        rows,err=scan_source(src); leads.extend(rows)
        health.append({'source':src['name'],'ok':not err,'count':len(rows),'error':err})
        time.sleep(.5)
    dedup={x['id']:x for x in leads}
    leads=sorted(dedup.values(),key=lambda x:(x['score'],x['discovered']),reverse=True)[:500]
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({
      'generated':datetime.now(timezone.utc).isoformat(),
      'version':'3.0','lead_count':len(leads),'health':health,'leads':leads
    },indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'Raven Scout wrote {len(leads)} leads to {OUT}')

if __name__=='__main__': main()
