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
UA='BlackLedgerStone-RavenScout/4.0 (+public property intelligence; contact via repo)'
MIN_FEE_GBP=3000


def clean(s): return re.sub(r'\s+',' ',s or '').strip()
def uid(source,url,text): return hashlib.sha1(f'{source}|{url}|{text[:120]}'.encode()).hexdigest()[:16]

def base_score(text,source_weight):
    t=text.lower(); s=source_weight; signals=[]
    for group, pts in [('motivation',7),('development',4),('public',5)]:
        for k in CFG['keywords'][group]:
            if k in t:
                s+=pts; signals.append(k)
    return min(100,s), sorted(set(signals))[:12]

def commercialise(score,signals,category,country,seen_before=False):
    s=' '.join(signals).lower(); c=(category or '').lower(); commercial=score
    if re.search(r'receiver|administration|probate|vacant|surplus|reduced|auction|repossess|failed sale|relisted',s): commercial+=8
    if re.search(r'planning|development|brownfield|conversion|site|land|care home|pub|office|commercial',s+' '+c): commercial+=5
    if re.search(r'government|council|mod|public|disposal',s+' '+c): commercial+=5
    if country=='Ireland': commercial+=1
    if seen_before: commercial+=2
    commercial=min(100,commercial)
    tier='T1' if commercial>=70 else 'T2' if commercial>=55 else 'WATCH'
    if re.search(r'auction',s+' '+c): action='Check catalogue, legal pack, guide price, auction date and unsold/withdrawn status.'
    elif re.search(r'planning|development|land|site|brownfield|conversion',s+' '+c): action='Verify planning, ownership, constraints, value uplift and developer/investor fit.'
    elif re.search(r'receiver|administration|probate|surplus|vacant|disposal',s+' '+c): action='Verify seller authority, availability, ownership and protected route to approach.'
    else: action='Open source evidence, verify commercial facts and decide whether to promote to due diligence.'
    evidence_confidence='Medium' if score>=35 else 'Low'
    estimated_fee=MIN_FEE_GBP if tier in ('T1','T2') else 0
    return commercial,tier,action,evidence_confidence,estimated_fee

def prior_ids():
    try:
        old=json.loads(OUT.read_text(encoding='utf-8'))
        return {x.get('id') for x in old.get('leads',[]) if x.get('id')}
    except Exception:
        return set()

def scan_source(src,old_ids):
    rows=[]
    try:
        r=requests.get(src['url'],headers={'User-Agent':UA},timeout=20)
        r.raise_for_status()
        soup=BeautifulSoup(r.text,'html.parser')
        seen=set()
        for a in soup.find_all('a', href=True):
            txt=clean(a.get_text(' ',strip=True)); href=urljoin(src['url'],a['href'])
            blob=f'{txt} {href}'; sc,sigs=base_score(blob,src.get('weight',10))
            if not sigs or len(txt)<8 or href in seen: continue
            seen.add(href); lead_id=uid(src['name'],href,txt)
            commercial,tier,action,confidence,fee=commercialise(sc,sigs,src['category'],src['country'],lead_id in old_ids)
            rows.append({
              'id':lead_id,'title':txt[:220],'url':href,'source':src['name'],'country':src['country'],
              'category':src['category'],'score':sc,'commercial_score':commercial,'tier':tier,'signals':sigs,
              'next_action':action,'evidence_confidence':confidence,'estimated_fee_gbp':fee,
              'repeat_signal':lead_id in old_ids,'discovered':datetime.now(timezone.utc).isoformat(),
              'status':'new','evidence':'Public web page link; verify availability, ownership, price, title, planning and buyer fit before treating as a deal.'
            })
        return sorted(rows,key=lambda x:x['commercial_score'],reverse=True)[:40], None
    except Exception as e:
        return [], f'{type(e).__name__}: {e}'

def main():
    old_ids=prior_ids(); leads=[]; health=[]
    for src in CFG['sources']:
        rows,err=scan_source(src,old_ids); leads.extend(rows)
        health.append({'source':src['name'],'ok':not err,'count':len(rows),'error':err})
        time.sleep(.5)
    dedup={x['id']:x for x in leads}; leads=sorted(dedup.values(),key=lambda x:(x['commercial_score'],x['discovered']),reverse=True)[:500]
    t1=sum(1 for x in leads if x['tier']=='T1'); t2=sum(1 for x in leads if x['tier']=='T2')
    summary={
      'raven_found':len(leads),'tier_1':t1,'tier_2':t2,
      'potential_fee_pipeline_gbp':sum(x['estimated_fee_gbp'] for x in leads),
      'healthy_sources':sum(1 for x in health if x['ok']),'total_sources':len(health)
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({'generated':datetime.now(timezone.utc).isoformat(),'version':'4.0','summary':summary,'lead_count':len(leads),'health':health,'leads':leads},indent=2,ensure_ascii=False),encoding='utf-8')
    print(f"Raven Scout wrote {len(leads)} leads: {t1} Tier 1, {t2} Tier 2, fee pipeline £{summary['potential_fee_pipeline_gbp']:,}")

if __name__=='__main__': main()
