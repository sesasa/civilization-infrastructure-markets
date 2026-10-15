import concurrent.futures, csv, datetime as dt, json, pathlib, requests, time

ROOT=pathlib.Path(__file__).parent
START=int(dt.datetime(2021,10,11,tzinfo=dt.timezone.utc).timestamp())
END=int(dt.datetime(2026,10,10,tzinfo=dt.timezone.utc).timestamp())
SYMBOLS=['^GSPC','^IXIC','^RUT','^STOXX50E','^N225','000300.SS','SPY','QQQ','IWM','VGK','EEM','INDA','MCHI','TLT','IEF','HYG','LQD','BIL','GLD','SLV','CPER','USO','UNG','VNQ','REET','XLE','ICLN','TAN','FAN','URA','ITA','PAVE','XLU','BTC-USD','ETH-USD','DX-Y.NYB','NVDA','TSM','ASML','AVGO','MU','ANET','VRT','ETN','PWR','GEV','POWL','HPS-A.TO','AAON','MYRG','ITRI','BELFB','NVT','HUBB','STRL','MOD','GE','CEG','VST','LNG','FSLR','ENPH','PLUG','FLNC','ORSTED.CO','VWS.CO','SU.PA','NKT.CO','PRY.MI','EQIX','DLR','PLD','BXP','MSFT','GOOGL','AMZN','META','PANW','CRWD','NET','COIN','ASTS','RKLB','XOM','CAT','ABB','MTZ']

def fetch(symbol):
 url='https://query1.finance.yahoo.com/v8/finance/chart/'+symbol
 r=requests.get(url,params={'period1':START,'period2':END,'interval':'1d','events':'div,splits'},headers={'User-Agent':'Mozilla/5.0'},timeout=40)
 r.raise_for_status(); data=r.json(); item=data['chart']['result'][0]
 (ROOT/'raw'/(symbol.replace('/','_')+'.json')).write_text(json.dumps(data))
 quote=item['indicators']['quote'][0]['close']; adj=item['indicators'].get('adjclose',[{}])[0].get('adjclose',quote)
 rows=[(dt.datetime.fromtimestamp(t,dt.timezone.utc).date().isoformat(),p,a) for t,p,a in zip(item.get('timestamp',[]),quote,adj) if p is not None and a is not None and t < END]
 if not rows: return {'symbol':symbol,'error':'no observations'}
 first,last=rows[0],rows[-1]
 out={'symbol':symbol,'currency':item['meta'].get('currency'),'start_date':first[0],'end_date':last[0],'start_close':first[1],'end_close':last[1],'price_change_pct':100*(last[1]/first[1]-1),'adjusted_change_pct':100*(last[2]/first[2]-1),'source':r.url}
 for y in range(2021,2027):
  eligible=[x for x in rows if x[0][:4]==str(y)]
  if eligible: out[str(y)+'_last_close']=eligible[-1][1]
 return out

if __name__=='__main__':
 results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  futures={pool.submit(fetch,s):s for s in SYMBOLS}
  for f in concurrent.futures.as_completed(futures):
   try: result=f.result()
   except Exception as e: result={'symbol':futures[f],'error':str(e)}
   results.append(result); print(result['symbol'],result.get('end_date',result.get('error')),flush=True)
 results.sort(key=lambda x:x['symbol'])
 (ROOT/'output'/'market_prices.json').write_text(json.dumps(results,indent=2))
 fields=list(dict.fromkeys(k for r in results for k in r))
 with (ROOT/'output'/'market_prices.csv').open('w') as f:
  writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader();writer.writerows(results)
