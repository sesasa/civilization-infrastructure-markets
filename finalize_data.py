import json,csv,pathlib
R=pathlib.Path(__file__).parent;O=R/'output'
a=json.loads((O/'market_prices.json').read_text())
for r in a:
 s=r['symbol'];notes=[]
 if 'error' in r:r['metric_type']='unavailable';continue
 typ='listed_equity_or_fund'
 if '=F' in s:typ='continuous_futures_quote';notes.append('Quote change only; not spot price or an investable rolled-futures return.')
 elif '=X' in s:typ='FX_quote';notes.append('Quote convention matters: percentage increase in local currency per USD is not the local-currency depreciation percentage.')
 elif s=='^TNX':
  typ='government_bond_yield';r['yield_change_bps']=(r['end_close']-r['start_close'])*100
  r.pop('price_change_pct',None);r.pop('adjusted_change_pct',None);notes.append('Levels in percent; change in basis points; not a bond investment return.')
 elif s.startswith('^') or s=='DX-Y.NYB':typ='price_index';notes.append('Price index, not a total-return index.')
 elif s.endswith('-USD'):typ='crypto_quote';notes.append('24/7 daily quote sampled through 9 October 2026; no staking yield.')
 if s in ['GEV','CEG','FLNC','2082.SR']:notes.append('Shorter observed history; see actual start_date. ACWA coverage begins Dec 2021 in downloaded series.')
 if s in ['ORSTED.CO','NKT.CO']:notes.append('Rights issues affect shareholder outcomes; vendor price/adjusted series is not a reconstruction of rights participation or sale proceeds.')
 if s in ['GE','RELIANCE.NS']:notes.append('Corporate spinoffs complicate investor total returns; vendor adjustment has not been reconciled to distributed securities.')
 if r['currency']!='USD':notes.append('Local-currency change, not USD return.')
 r['metric_type']=typ;r['notes']=' '.join(notes)
(O/'market_prices.json').write_text(json.dumps(a,indent=2))
keys=list(dict.fromkeys(k for r in a for k in r))
with (O/'market_prices.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(a)
print('Annotated',len(a),'requested series; unavailable:',[r['symbol'] for r in a if 'error' in r])
