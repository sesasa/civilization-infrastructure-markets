import csv,json,pathlib,concurrent.futures,requests
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).parent
paths={s:'stocks/'+s.lower() for s in ['NVDA','VRT','ETN','PWR','POWL','AAON','BELFB','ITRI','MYRG','STRL','MOD','FSLR','ENPH','PLUG','FLNC','GEV','EQIX','DLR','BXP','PANW','CRWD','RKLB','LNG']}
paths.update({'HPS-A.TO':'quote/tsx/HPS.A','SU.PA':'quote/epa/SU','NKT.CO':'quote/cph/NKT','ORSTED.CO':'quote/cph/ORSTED','LT.NS':'quote/nse/LT','POWERINDIA.NS':'quote/nse/POWERINDIA','KEC.NS':'quote/nse/KEC','300750.SZ':'quote/she/300750','300274.SZ':'quote/she/300274','2082.SR':'quote/tadawul/2082','2222.SR':'quote/tadawul/2222'})
def f(item):
 symbol,path=item;url='https://stockanalysis.com/'+path+'/statistics/'
 r=requests.get(url,timeout=30);r.raise_for_status();soup=BeautifulSoup(r.text,'html.parser')
 text=soup.get_text(' ',strip=True);(ROOT/'raw'/(symbol+'_valuation.txt')).write_text(text)
 result={'symbol':symbol,'source':url,'retrieved':'2026-10-12'}
 for tr in soup.select('tr'):
  cells=tr.find_all(['td','th'])
  if len(cells)==2:result[cells[0].get_text(' ',strip=True)]=cells[1].get_text(' ',strip=True)
 return result
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 fs={ex.submit(f,x):x[0] for x in paths.items()}
 for ft in concurrent.futures.as_completed(fs):
  try:r=ft.result()
  except Exception as e:r={'symbol':fs[ft],'error':str(e)}
  results.append(r);print(r['symbol'],r.get('Market Cap',r.get('error')),r.get('PE Ratio'),r.get('Forward PE'),flush=True)
(ROOT/'output'/'valuations.json').write_text(json.dumps(results,indent=2))
keys=['symbol','Market Cap','Enterprise Value','PE Ratio','Forward PE','PS Ratio','EV / EBITDA','Revenue','Net Income','Shares Outstanding','source','retrieved','error']
with (ROOT/'output'/'valuations.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(results)
