import csv,io,json,pathlib,requests,concurrent.futures
ROOT=pathlib.Path(__file__).parent
def fetch(area,kind):
 url=f'https://stats.bis.org/api/v1/data/WS_SPP/Q.{area}.{kind}.628?format=csv'
 r=requests.get(url,timeout=30);r.raise_for_status()
 (ROOT/'raw'/f'property_{area}_{kind}.csv').write_text(r.text)
 rows=[x for x in csv.DictReader(io.StringIO(r.text)) if x.get('OBS_VALUE') and x.get('TIME_PERIOD','')<='2026-Q2']
 if not rows:return {'area':area,'kind':kind,'error':'no data'}
 end=max(rows,key=lambda r:r['TIME_PERIOD']);year,q=end['TIME_PERIOD'].split('-');start_date=str(int(year)-5)+'-'+q
 starts=[x for x in rows if x['TIME_PERIOD']==start_date]
 if not starts:return {'area':area,'kind':kind,'error':'no start'}
 start=starts[0];v0=float(start['OBS_VALUE']);v1=float(end['OBS_VALUE'])
 return {'area':area,'kind':kind,'start_date':start_date,'end_date':end['TIME_PERIOD'],'start_index':v0,'end_index':v1,'change_pct':100*(v1/v0-1),'source':url}
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 fs={ex.submit(fetch,a,k):(a,k) for a in ['US','CN','IN','XM','DK','DE','GB','AE','SA','QA'] for k in ['N','R']}
 for f in concurrent.futures.as_completed(fs):
  try:r=f.result()
  except Exception as e:r={'area':fs[f][0],'kind':fs[f][1],'error':str(e)}
  out.append(r);print(r,flush=True)
(ROOT/'output'/'property.json').write_text(json.dumps(out,indent=2))
with (ROOT/'output'/'property.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in out for k in r)));w.writeheader();w.writerows(out)
