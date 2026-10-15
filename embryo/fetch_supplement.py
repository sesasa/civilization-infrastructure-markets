import sys,pathlib,requests,json,csv,concurrent.futures
from bs4 import BeautifulSoup
R=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent))
from fetch_prices import fetch

def get(s):
 p=fetch(s);u='https://stockanalysis.com/stocks/'+s.lower()+'/statistics/'
 r=requests.get(u,timeout=30);r.raise_for_status();b=BeautifulSoup(r.text,'html.parser');(R/(s+'_valuation.txt')).write_text(b.get_text(' ',strip=True))
 v={}
 for tr in b.select('tr'):
  c=tr.find_all(['td','th'])
  if len(c)==2:v[c[0].get_text(' ',strip=True)]=c[1].get_text(' ',strip=True)
 for k in ['Market Cap','Enterprise Value','PE Ratio','Forward PE','PS Ratio','Revenue','Net Income']:p[k]=v.get(k)
 p['valuation_source']=u;p['valuation_retrieved']='2026-10-12';p['notes']='USD share prices, splits adjusted. Dividends excluded in price_change_pct; adjusted_change_pct is vendor distribution-adjusted. IOT shorter history from IPO. Business composition changed through acquisitions/divestitures; not organic growth measures.'
 return p
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 fs={ex.submit(get,s):s for s in ['EMR','ROK','XYL','IOT']}
 for f in concurrent.futures.as_completed(fs):
  try:x=f.result();out.append(x);print(x['symbol'],x['start_date'],round(x['price_change_pct'],1),x.get('Market Cap'),x.get('Forward PE'),flush=True)
  except Exception as e:out.append({'symbol':fs[f],'error':str(e)});print(fs[f],str(e),flush=True)
(R/'supplemental_markets.json').write_text(json.dumps(out,indent=2))
keys=list(dict.fromkeys(k for row in out for k in row))
with (R/'supplemental_markets.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(out)
