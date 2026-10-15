from pathlib import Path
import json,csv,zipfile
from report_sources import S
R=Path(__file__).parent;O=R/'output'
intro='''ACTUAL CODEX–CLAUDE DISCUSSION, 12 OCTOBER 2026\n\nFour exchanges through the installed Claude CLI using read-only research tools.\nThese are the actual prompts and final responses, not a simulated dialogue.\nResearch-stage claims and figures were corrected in later rounds. Read the final\nreport and rounds 3–4 for the settled assessment. Earlier claims are retained\nfor transparency and are not all endorsed. Tool-by-tool search traces are not\nincluded here. The shared dataset was prepared by Codex; this was critical\nreview, not two statistically independent studies.\n\n'''
parts=[intro]
for i in range(1,5):
 for role,kind in [('CODEX','prompt'),('CLAUDE','response')]:
  p=R/'discussion'/f'round{i}_{kind}.txt'
  parts.append(f'\n{"="*72}\nROUND {i} — {role}\n{"="*72}\n\n'+p.read_text())
(O/'claude_discussion.txt').write_text('\n'.join(parts))
evidence=[]
def e(company,period,metric,value,unit,yoy,source,status='reported'):
 evidence.append(dict(company=company,period=period,metric=metric,value=value,unit=unit,yoy_pct=yoy,status=status,source=S[source]['url']))
e('Powell','FY2021','Revenue',470.559,'USD million','','powl21')
e('Powell','Q3 FY2026 ended 2026-06-30','Revenue',312,'USD million',9,'powl')
e('Powell','Q3 FY2026 ended 2026-06-30','Orders',934,'USD million',158,'powl')
e('Powell','2026-06-30','Backlog',2400,'USD million',69,'powl')
for year,v in [(2021,380),(2022,558),(2023,710),(2024,788),(2025,898)]:e('Hammond Power Solutions',str(year),'Revenue (rounded)',v,'CAD million','','hpshist')
e('Hammond Power Solutions','Q2 2026','Revenue',325,'CAD million',44.7,'hps')
e('Hammond Power Solutions','Q2 2026','Adjusted EBITDA',53,'CAD million','','hps')
e('AAON','Q2 2026','Revenue',627,'USD million',101.2,'aaon')
e('AAON','Q2 2026','Operating income',68.9,'USD million',192.1,'aaon')
e('Bel Fuse','Q2 2026','Revenue',210.7,'USD million',25.1,'bel')
e('Bel Fuse','Q2 2026','GAAP net income',25.5,'USD million','','bel')
e('Itron','Q2 2026','Revenue',563,'USD million',-7,'itron')
e('Itron','Q2 2026','Annual recurring revenue',417,'USD million',21,'itron')
e('Vertiv','Q2 2026','Revenue',3274,'USD million',24,'vertiv')
e('Quanta Services','Q2 2026','Revenue',9560,'USD million','','quanta')
e('Quanta Services','2026-06-30','RPO (distinct from total backlog)',33600,'USD million','','quanta')
e('GE Vernova','2026-06-30','Firm gas equipment backlog',53,'GW','','gev')
e('GE Vernova','2026-06-30','Gas equipment slot reservations',63,'GW','','gev','reservation')
e('GE Vernova','Q2 2026','Gas equipment shipped',3,'GW','','gev')
e('Fluence','FY2026, guidance revised 2026-09-16','Revenue',2400,'USD million','','fluence','forecast')
e('Fluence','FY2026, guidance revised 2026-09-16','Adjusted EBITDA',-200,'USD million','','fluence','forecast')
e('Digital Realty','Q2 2026','Core FFO per share excluding promote',2.13,'USD','','dlr')
e('CATL','FY2025','Battery sales',661,'GWh',39,'catl')
e('CATL','FY2025','Revenue',423700,'CNY million',17,'catl')
e('CATL','FY2025','Net profit',72200,'CNY million',42,'catl')
e('State Grid','H1 2026','Fixed asset investment (more than)',310000,'CNY million',12.6,'sgcc')
e('Hitachi Energy India','Q1 FY2027 ended 2026-06-30','Revenue',24937,'INR million',68.6,'hitachi')
e('Larsen & Toubro','2026-06-30','Order book',7790000,'INR million',27,'lt')
e('ACWA','H1 2026','Battery capacity commissioned',0.8,'GWh','','acwa')
e('ACWA','H1 2026','Water capacity commissioned',0.9,'million cubic metres/day','','acwa')
e('Aramco','Q2 2026','Adjusted net income',33400,'USD million','','aramco')
e('CrowdStrike','Q2 FY2027 ended 2026-07-31','Revenue',1470,'USD million',26,'crwd')
e('CrowdStrike','2026-07-31','Annual recurring revenue',5840,'USD million',25,'crwd')
e('Google','2026-03-19','Contracted demand response',1,'GW','','google','contracted; not continuously dispatched')
with (O/'company_evidence.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(evidence[0]));w.writeheader();w.writerows(evidence)
readme='''RESEARCH PACKAGE — 12 October 2026\n\nStart with civilization_infrastructure_markets_2026.pdf.\nMarket prices generally span 11 October 2021–9 October 2026. Exact dates,\ncurrencies and exceptions are in the tables. FX timestamps start on 10 October\n2021 UTC in the vendor feed. Valuations were retrieved 12 October 2026.\n\nData files\n- market_prices.csv/json: prices, adjusted changes, source links and warnings.\n- annual_returns.csv: 2021 is partial from October; 2026 through October 9.\n  GEV, CEG, FLNC and ACWA histories begin later; check start dates.\n  Futures and FX rows show quotation changes, not strategy returns.\n  The Treasury yield is excluded from annual return calculations.\n- valuations.csv/json: vendor snapshot ratios; fiscal and adjustment bases vary.\n- company_evidence.csv: selected manually checked primary-source fundamentals.\n- property.csv/json: local nominal and CPI-deflated BIS price indices.\n- renewable_capacity.csv: IRENA nameplate GW, not generation or firm power.\n- sources.json: the report's linked sources.\n- claude_discussion.txt: actual exchange; early errors are corrected later.\n\nScripts\nRun from the project directory. Python dependencies: requests, beautifulsoup4,\nmatplotlib, pypdf, reportlab, openpyxl. Fonts: system DejaVu Sans.\nRaw vendor series and valuation extracts are retained in research/raw.\npython research/analyze_data.py regenerates charts/annual changes from raw data.\npython research/finalize_data.py reapplies metric labels and special warnings.\npython research/build_report.py regenerates the PDF.\npython research/package_research.py rebuilds the dialogue, evidence table and ZIP.\nNetwork fetch scripts are included, but refetches may differ after revisions.\n\nThe sample is not exhaustive, a sector backtest, or a historical P/E panel.\nListed funds are proxies. Rights issues and spinoffs need separate investor-\nreturn reconstruction. Exact source and date metadata take precedence over\nrounded prose. The report distinguishes actuals, reservations, forecasts and\ninterpretation. Source agreement is not proof.\n'''
(O/'README.txt').write_text(readme)
with zipfile.ZipFile(O/'research_bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in O.iterdir():
  if f.is_file() and f.suffix!='.zip' and not f.name.startswith('preview_'):z.write(f,'research/output/'+f.name)
 for f in R.glob('*.py'):z.write(f,'research/'+f.name)
 for f in (R/'discussion').glob('*.txt'):z.write(f,'research/discussion/'+f.name)
 for f in (R/'raw').iterdir():
  if f.is_file() and f.suffix in ['.json','.txt','.csv','.pdf']:z.write(f,'research/raw/'+f.name)
print('Packaged',len(evidence),'fundamental records; ZIP bytes:',(O/'research_bundle.zip').stat().st_size)
