RESEARCH PACKAGE — 12 October 2026

Start with civilization_infrastructure_markets_2026.pdf.
Market prices generally span 11 October 2021–9 October 2026. Exact dates,
currencies and exceptions are in the tables. FX timestamps start on 10 October
2021 UTC in the vendor feed. Valuations were retrieved 12 October 2026.

Data files
- market_prices.csv/json: prices, adjusted changes, source links and warnings.
- annual_returns.csv: 2021 is partial from October; 2026 through October 9.
  GEV, CEG, FLNC and ACWA histories begin later; check start dates.
  Futures and FX rows show quotation changes, not strategy returns.
  The Treasury yield is excluded from annual return calculations.
- valuations.csv/json: vendor snapshot ratios; fiscal and adjustment bases vary.
- company_evidence.csv: selected manually checked primary-source fundamentals.
- property.csv/json: local nominal and CPI-deflated BIS price indices.
- renewable_capacity.csv: IRENA nameplate GW, not generation or firm power.
- sources.json: the report's linked sources.
- claude_discussion.txt: actual exchange; early errors are corrected later.

Scripts
Run from the project directory. Python dependencies: requests, beautifulsoup4,
matplotlib, pypdf, reportlab, openpyxl. Fonts: system DejaVu Sans.
Raw vendor series and valuation extracts are retained in research/raw.
python research/analyze_data.py regenerates charts/annual changes from raw data.
python research/finalize_data.py reapplies metric labels and special warnings.
python research/build_report.py regenerates the PDF.
python research/package_research.py rebuilds the dialogue, evidence table and ZIP.
Network fetch scripts are included, but refetches may differ after revisions.

The sample is not exhaustive, a sector backtest, or a historical P/E panel.
Listed funds are proxies. Rights issues and spinoffs need separate investor-
return reconstruction. Exact source and date metadata take precedence over
rounded prose. The report distinguishes actuals, reservations, forecasts and
interpretation. Source agreement is not proof.
