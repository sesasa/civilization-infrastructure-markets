import csv,datetime as dt,json,pathlib,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=pathlib.Path(__file__).parent
OUT=ROOT/'output'
prices=json.loads((OUT/'market_prices.json').read_text())
def series(symbol,adj=True):
 d=json.loads((ROOT/'raw'/(symbol+'.json')).read_text())['chart']['result'][0]
 q=d['indicators']['quote'][0]['close']
 p=d['indicators'].get('adjclose',[{}])[0].get('adjclose',q) if adj else q
 return [(dt.datetime.fromtimestamp(t,dt.timezone.utc),v) for t,v in zip(d['timestamp'],p) if v is not None and t<1791590400]
annual=[]
for r in prices:
 if 'error' in r or r['symbol']=='^TNX':continue
 try:s=series(r['symbol'])
 except Exception:continue
 x={'symbol':r['symbol'],'currency':r['currency'],'start_date':r['start_date'],'end_date':r['end_date']}
 first=s[0][1];prev=first;peak=first;drawdown=0
 for t,v in s:peak=max(peak,v);drawdown=min(drawdown,v/peak-1)
 for yr in range(2021,2027):
  sub=[v for t,v in s if t.year==yr]
  if sub:
   x[str(yr)]=100*(sub[-1]/prev-1);prev=sub[-1]
 x['max_drawdown_pct']=drawdown*100;annual.append(x)
with (OUT/'annual_returns.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['symbol','currency','start_date','end_date','2021','2022','2023','2024','2025','2026','max_drawdown_pct']);w.writeheader();w.writerows(annual)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'#26384a','text.color':'#172b3a','figure.facecolor':'white'})
fig,axes=plt.subplots(2,1,figsize=(10.5,9.5))
for ax,syms,title in [(axes[0],['SPY','QQQ','IWM','VGK','MCHI','INDA','UAE'], 'Equity regions and size: growth is uneven'),(axes[1],['GLD','CPER','TLT','VNQ','XLE','ICLN','BIL'],'Assets and sectors: scarcity, rates and capital returns')]:
 for sym in syms:
  s=series(sym);x,y=zip(*s);ax.plot(x,[v/y[0]*100 for v in y],label=sym,lw=1.7)
 ax.set_title(title,loc='left');ax.axhline(100,color='#aaaaaa',lw=.7);ax.set_ylabel('Adjusted close; start = 100');ax.grid(alpha=.15);ax.legend(ncol=4,fontsize=8,frameon=False)
fig.suptitle('October 2021–October 2026 | selected USD exchange-traded funds',fontsize=14,fontweight='bold')
fig.text(.08,.015,'Source: Yahoo Finance daily series; distribution-adjusted proxy returns, before investor taxes.\nFunds are not spot commodities or direct property. Sample is illustrative, not a complete investment universe.',fontsize=8)
fig.tight_layout(rect=[0,.055,1,.96]);fig.savefig(OUT/'market_regimes.png',dpi=180);plt.close(fig)

fig,axes=plt.subplots(1,2,figsize=(10.5,5.2))
for ax,syms,title in [(axes[0],['POWL','HPS-A.TO','VRT','AAON','ITRI','SPY'],'Equipment: repricing is highly selective'),(axes[1],['300750.SZ','300274.SZ','601012.SS','ENPH','PLUG','SPY'],'Deployment can grow while shares fall')]:
 for sym in syms:
  s=series(sym,False);x,y=zip(*s);ax.plot(x,[v/y[0]*100 for v in y],label=sym,lw=1.5)
 ax.set_yscale('log');ax.axhline(100,color='#aaa',lw=.7);ax.set_title(title,fontsize=11,loc='left');ax.set_ylabel('Price index; logarithmic scale');ax.grid(alpha=.15);ax.legend(fontsize=8,frameon=False,ncol=2)
fig.text(.07,.015,'Source: Yahoo Finance. Local-currency split-adjusted prices, dividends excluded; start = 100.\nDifferent currencies and businesses: these are case studies, not a sector backtest.',fontsize=8)
fig.tight_layout(rect=[0,.08,1,1]);fig.savefig(OUT/'company_divergence.png',dpi=180);plt.close(fig)

data={'US':[325.822,352.490,385.283,427.886,467.918],'World':[3077.120,3379.389,3872.829,4457.340,5149.280],'China':[1017.852,1156.126,1453.701,1817.956,2258.016],'EU':[514.661,565.469,635.960,709.457,779.443],'India':[147.418,163.295,175.874,205.390,250.519],'GCC':[3.793,6.137,10.631,15.183,23.889]}
fig,ax=plt.subplots(figsize=(10.5,4.9))
for name,v in data.items():ax.plot(range(2021,2026),[x/v[0]*100 for x in v],marker='o',label=f'{name}: {v[-1]:,.0f} GW in 2025')
ax.set_title('Operating renewable generation capacity: regional paths',loc='left');ax.set_ylabel('End-2021 = 100');ax.set_xticks(range(2021,2026));ax.grid(alpha=.15);ax.legend(frameon=False)
fig.text(.08,.01,'Source: IRENA Renewable Capacity Statistics 2026, total renewable capacity. GCC = six states summed.\nNameplate GW is not generation, firm capacity, storage GWh, or non-fossil capacity including nuclear.',fontsize=8)
fig.tight_layout(rect=[0,.08,1,1]);fig.savefig(OUT/'physical_capacity.png',dpi=180);plt.close(fig)
with (OUT/'renewable_capacity.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['region','2021_GW','2022_GW','2023_GW','2024_GW','2025_GW','CAGR_2021_2025_pct']);
 for k,v in data.items():w.writerow([k,*v,100*((v[-1]/v[0])**.25-1)])
print('Charts and annual return table written.', len(prices),'market series requests;',sum('error' not in p for p in prices),'successful.')
