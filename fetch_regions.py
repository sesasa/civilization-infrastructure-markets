import fetch_prices as fp,concurrent.futures,json,csv
symbols=['GC=F','SI=F','HG=F','CL=F','BZ=F','NG=F','DBA','DBB','WOOD','CGW','^TNX','^NSEI','^TASI.SR','KSA','UAE','QAT','300750.SZ','300274.SZ','601012.SS','1211.HK','9988.HK','0700.HK','0981.HK','601138.SS','688256.SS','LT.NS','POWERINDIA.NS','KEC.NS','KPIL.NS','TATAPOWER.NS','RELIANCE.NS','ABB.NS','POLYCAB.NS','ADANIPORTS.NS','2082.SR','2222.SR','EMAR.AE','EMAAR.AE','EURUSD=X','CADUSD=X','DKKUSD=X','INR=X','CNY=X','BTC-USD','ETH-USD']
results=json.loads((fp.ROOT/'output'/'market_prices.json').read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 fs={pool.submit(fp.fetch,s):s for s in symbols}
 for f in concurrent.futures.as_completed(fs):
  try:r=f.result()
  except Exception as e:r={'symbol':fs[f],'error':str(e)}
  results=[x for x in results if x['symbol']!=r['symbol']];results.append(r)
  print(r,flush=True)
results.sort(key=lambda x:x['symbol'])
(fp.ROOT/'output'/'market_prices.json').write_text(json.dumps(results,indent=2))
with (fp.ROOT/'output'/'market_prices.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in results for k in r)));w.writeheader();w.writerows(results)
