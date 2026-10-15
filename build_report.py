from pathlib import Path
import json,csv,math,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from report_sources import S
R=Path(__file__).parent;O=R/'output'
for name,file in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf'),('DV-Italic','DejaVuSans-Oblique.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV-Italic',boldItalic='DV-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='DV',fontSize=9.1,leading=13.4,spaceAfter=8,textColor=colors.HexColor('#243746')))
styles.add(ParagraphStyle(name='TitleX',fontName='DV-Bold',fontSize=24,leading=29,spaceAfter=18,textColor=colors.HexColor('#12364a')))
styles.add(ParagraphStyle(name='Lead',fontName='DV-Bold',fontSize=15,leading=20,spaceAfter=14,textColor=colors.HexColor('#12364a')))
styles.add(ParagraphStyle(name='SmallX',fontName='DV',fontSize=7.2,leading=9.4,spaceAfter=5,textColor=colors.HexColor('#4d6070')))
styles.add(ParagraphStyle(name='CellX',fontName='DV',fontSize=7.4,leading=10,textColor=colors.HexColor('#243746')))
styles.add(ParagraphStyle(name='CellHead',fontName='DV-Bold',fontSize=7.4,leading=10,textColor=colors.white))
P={r['symbol']:r for r in json.loads((O/'market_prices.json').read_text()) if 'error' not in r}
V={r['symbol']:r for r in json.loads((O/'valuations.json').read_text()) if 'error' not in r}
A={r['symbol']:r for r in csv.DictReader((O/'annual_returns.csv').open())}
used=[];story=[]
def cite(*keys):
 result=[]
 for k in keys:
  if k not in used:used.append(k)
  result.append('<a href="'+html.escape(S[k]['url'],quote=True)+'" color="#086788">['+str(used.index(k)+1)+']</a>')
 return ' '+', '.join(result)
def p(t,*sources,small=False):story.append(Paragraph(t+cite(*sources),styles['SmallX' if small else 'Body']))
def title(t,new=True):
 if new:story.append(PageBreak())
 story.append(Paragraph(t,styles['Lead']))
def table(headers,rows,widths=None):
 data=[[Paragraph(html.escape(str(x)),styles['CellHead']) for x in headers]]
 for row in rows:data.append([Paragraph(str(x),styles['CellX']) for x in row])
 tb=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#12364a')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#edf3f6'),colors.white]),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#12364a'))]))
 story.append(tb);story.append(Spacer(1,9))
def fig(file,w=500):
 iw,ih=ImageReader(str(O/file)).getSize();story.append(Image(str(O/file),width=w,height=w*ih/iw));story.append(Spacer(1,8))
def pct(x):return f'{float(x):+.1f}%'
def ret(s,adj=True):return pct(P[s]['adjusted_change_pct' if adj else 'price_change_pct'])
def companyrow(s,label,currency='USD'):
 v=V.get(s,{});return [label,ret(s,False),currency+' '+v.get('Market Cap','—'),v.get('PE Ratio','—'),v.get('Forward PE','—')]

story.append(Paragraph('What civilization is<br/>building and scaling',styles['TitleX']))
p('<b>A global market and infrastructure study, October 2021–October 2026</b><br/>US • Europe • China • GCC • India<br/>Prepared 12 October 2026 | Codex research, challenged in four rounds with Claude')
p('<b>The joint conclusion:</b> the evidence supports a buildout of more electrified, compute-intensive and increasingly automated production and services. The scarce complements are reliable power, connections, electrical equipment, cooling, networks, skilled execution, and institutions that let these components work together.')
p('At the civilization level, the useful interpretation is that societies scale <b>the range, reliability and reach of collectively deployable capabilities</b>: useful work, knowledge and coordinated action. Energy and information are inputs into this process. This is an interpretive framework; five years of market data cannot establish a universal law of history.')
table(['Evidence','What it establishes'],[
['Global renewable capacity: 3,077 → 5,149 GW, end-2021 to end-2025','Actual operating nameplate capacity grew 67%; four-year compound growth about 13.7%.'],
['2026 grid investment: about $550bn, up about 20%','IEA estimate of spending; a broad electricity buildout beyond AI.'],
['North American primary data-center markets: 10.9 GW, +33.7% year on year','CBRE evidence of delivered capacity; vacancy only 1.4%.'],
['Powell: quarterly orders $934m; Hammond: quarterly sales C$325m','Demand is visible below the megacap level, in switchgear and transformers.'],
['Solar, storage and wind shares often lag physical deployment','Building useful infrastructure does not ensure attractive investor returns.']],[225,275])
p('Sources for these anchors. Detailed definitions, dates and limitations follow.','irena','iea','cbre','powl','hps',small=True)
p('<b>Phase:</b> substantial installation and difficult integration, with different financial cycles. Grid equipment remains constrained; AI customer returns are still being tested; some renewable manufacturing is already commoditized. There is no defensible single “early” or “late” label for the whole transition.')
p('This report includes 126 usable market series, current company valuation screens, primary earnings evidence, physical deployment data and seven national/regional property markets. It is a broad sample, not every priced asset. Raw data and the actual Claude exchange accompany the PDF.',small=True)

title('Reading your civilization thesis critically')
p('Your two-axis model is useful because energy and coordination really are complements. A power station without a connected customer is not a working energy service; a model without reliable power, data and a usable workflow is not an economic capability. The market evidence repeatedly points to the missing complement rather than the most visible invention.')
p('<b>What I would change.</b> Replace “more energy” with “more useful services and capabilities, subject to resource constraints.” Electrification and efficiency can increase useful work without proportionate growth in primary energy. Replace “population is the output” with a feedback system: population also changes specialization, institutions, demand and innovation. “Every production gain became more people” is too absolute to carry a historical argument.')
p('The six infrastructure jobs are a good organizing device, but they omit material transformation, transport of physical goods, water, waste, maintenance and human skill formation. Much information is embodied in factories, procedures and trained people. AI models store statistical structure and support cognition; they are not a complete substitute for databases, science or institutions.')
p('Path dependence is real, but physical assets are often reused and institutions can become obsolete. Overbuilding sometimes creates cheap capacity for later users; it can also leave unusable equipment and debt. Those are possible outcomes, not a historical rule that every speculative bubble funds a productive new era.')
p('<b>Waste heat is a boundary condition, not a dated forecast.</b> Persistent exponential energy growth ultimately encounters planetary limits. The cited theoretical work examines such conditional trajectories. A claim that Earth becomes uninhabitable within a fixed few centuries needs assumptions about growth, energy sources, net additions to the heat budget and climate response. Using incoming sunlight also requires careful accounting of what would otherwise have been absorbed. This is not the binding explanation for the next five years of capital spending.','heat')
p('Likewise, “speed matters most” is too strong for regional transitions. Pace matters together with replacement employment, skills, local fiscal support, ownership and credible institutions. The supplied coal, canal and whaling examples are suggestive case studies, not a controlled demonstration of one decisive variable.')
p('<b>What is civilization for?</b> Prices cannot answer that normative question. They reveal what owners expect to monetize under existing institutions. Health, leisure, scientific knowledge, biodiversity and political freedom can improve without a corresponding listed-market capitalization. A civilization can become more capable while distributing the benefits badly.')
table(['More defensible framework','Observable counterpart in this study'],[
['Inputs: energy, materials, knowledge, labor, capital','GW, GWh, equipment output, research expenditure, capex'],
['Conversion: institutions, skills, interoperability, contracts','Commissioning, utilization, software revenue, connection rights'],
['Outputs: reliable useful services','Power delivered, computation used, water supplied, production'],
['Financial capture: who receives the surplus','Margins, cash flow, valuation and dilution'],
['Purpose and distribution','Requires social judgment beyond asset prices']],[235,265])

title('How to read the evidence without confusing signals')
p('<b>Market window:</b> first available observation on or after 11 October 2021 through 9 October 2026; Gulf listings usually end on 8 October. Exact dates are in each row; FX vendor timestamps can begin on 10 October UTC. Some listings have shorter histories. Physical series stop at their latest reported quarter or year; full-year 2026 spending and later commissioning plans are forecasts, not completed work.')
p('Price change = ending close / beginning close − 1. Equity prices are vendor split-adjusted. ETF adjusted-close changes are distribution-adjusted return proxies, before investor taxes and transaction costs. They reflect fund expenses and composition; they are not the underlying country economy or a pure commodity spot return.','prices')
p('Company prices outside the US are shown in local currency. Regional ETFs are USD instruments, making currency exposure part of their result. Valuations were retrieved on 12 October 2026 and can use different quote and reporting timestamps. Forward P/E reflects provider-defined analyst estimates, not a common fiscal year or guaranteed earnings. Current market cap is an equity stock of value; capex is a spending flow.','values')
table(['Evidence stage','Useful question','Common error'],[
['Announcement / target','Has financing, land and permission been secured?','Treating a press release as capacity'],
['Reservation / firm contract','What can be cancelled, and at what cost?','Adding slot reservations to orders without a label'],
['Construction / backlog','Can it be executed at the quoted price?','Treating backlog as guaranteed profit'],
['Energized or commissioned capacity','Is it connected and usable?','Confusing GW, GWh and TWh'],
['Utilization / realized sales','Is someone paying for output?','Assuming a leased shell proves GPU utilization'],
['Profit / cash return','Does revenue cover operating and capital costs?','Substituting adjusted profit for cash generation'],
['Market valuation','What future success is already assumed?','Inferring spending volume from a rising stock']],[116,190,194])
p('<b>Identification limits:</b> this is a deliberately broad, thematic sample with winners and counterexamples, not a randomized universe or a factor-adjusted backtest. Rates, inflation, currency, acquisitions, regulation and starting valuations can explain returns alongside infrastructure demand. We corroborate price patterns with earnings, contracts and physical data rather than claim that prices identify a single cause.')
p('The phrase “free-market signal” needs qualification. State-owned grids, regulated tariffs, subsidies, export controls, public procurement and sovereign investment strongly shape these markets. The useful signal is what firms and investors commit to under those actual rules. A state-backed order is real demand but is not evidence of purely private willingness to pay.')
p('Direct price-index changes in the same window were: S&amp;P 500 +79.1%, Nasdaq Composite +88.9%, Russell 2000 +26.4%, Euro Stoxx 50 +51.6%, Nikkei 225 +142.2% and Nifty 50 +25.5%. These exclude dividends and use each index’s native currency.', 'prices',small=True)
p('Uncovered or thinly covered markets include private credit, unlisted infrastructure, farmland, fine art, regional commercial-property transactions and some local commodity benchmarks. Four requested ticker series failed and remain marked unavailable. National GCC housing indices were not obtained. No missing series is replaced with an invented value.',small=True)

title('The five-year cross-asset scorecard')
rows=[]
for s,label in [('SPY','US large cap / S&amp;P 500'),('QQQ','Nasdaq-100'),('IWM','US small cap'),('VGK','Europe equities'),('MCHI','China equities'),('INDA','India equities'),('KSA','Saudi equities'),('UAE','UAE equities'),('QAT','Qatar equities'),('EEM','Emerging-market equities'),('TLT','Long US Treasuries'),('IEF','7–10 year US Treasuries'),('LQD','US investment-grade credit'),('HYG','US high-yield credit'),('BIL','US Treasury bills'),('GLD','Gold fund'),('SLV','Silver fund'),('CPER','Copper futures fund'),('DBA','Agriculture futures fund'),('VNQ','US listed property'),('REET','Global listed property'),('XLE','US energy equities'),('XLU','US utilities'),('ICLN','Global clean energy equities'),('TAN','Solar equities'),('URA','Uranium-linked equities'),('ITA','US aerospace / defense'),('PAVE','US infrastructure equities'),('WOOD','Timber / forestry equities'),('CGW','Global water equities')]:
 rows.append([label,s,ret(s),pct(A[s]['max_drawdown_pct'])])
table(['Exposure; USD fund','Ticker','Adjusted change','Max. drawdown*'],rows,[237,53,105,105])
p('*Largest peak-to-trough decline within the sampled daily adjusted series. Not a forecast of downside. Different fund structures and holdings matter. The complete dataset also contains local indices, FX, crypto, commodities and companies.','prices',small=True)

title('The path matters as much as the endpoint')
fig('market_regimes.png',490)
p('The same five-year interval contains several different regimes. Duration-sensitive assets and speculative growth were weak in 2022; later gains became concentrated in parts of technology, power equipment and energy. The charts prevent a single start/end return from disguising major reversals.','prices',small=True)

title('Oil, metals, rates, gold and crypto: different messages')
rows=[]
for s,label,unit in [('BZ=F','Brent','$ / barrel'),('CL=F','WTI','$ / barrel'),('NG=F','US natural gas','$ / MMBtu'),('GC=F','Gold','$ / troy oz'),('SI=F','Silver','$ / troy oz'),('HG=F','Copper','$ / lb'),('BTC-USD','Bitcoin','$'),('ETH-USD','Ether','$')]:
 r=P[s];rows.append([label,f"{r['start_close']:,.2f}",f"{r['end_close']:,.2f}",ret(s,False),unit])
table(['Series','Start','End','Quote change','Units'],rows,[90,103,103,103,101])
p('Commodity rows are vendor continuous-futures quotations, not spot benchmarks or a realizable roll strategy. For example, USO returned '+ret('USO')+' on adjusted closes while the WTI quotation rose '+ret('CL=F',False)+'. UNG returned '+ret('UNG')+' while the gas quotation fell '+ret('NG=F',False)+'. Contract rolls, collateral, curve shape and fund design matter.','prices')
r=P['^TNX'];p(f'<b>Capital became more expensive.</b> The US 10-year yield series rose from {r["start_close"]:.3f}% to {r["end_close"]:.2f}%, roughly {r["yield_change_bps"]:.0f} basis points. Long Treasury losses and weak listed-property returns show why a rising demand forecast alone cannot make a capital-intensive project attractive. The relevant hurdle is expected cash return relative to financing cost.','prices')
p('<b>Oil is still part of the system.</b> Energy-equity returns substantially exceeded the change in crude quotations. Cash distributions, operating leverage, discipline and valuations matter. Oil demand, gas generation and renewable installation can grow together; a transition does not imply immediate replacement of the incumbent asset base. The IEA’s 2026 estimate puts gas investment at $330bn, a decade high, while oil investment is below $500bn for a third consecutive annual decline. War-related supply disruption also affects prices.','iea')
p('<b>Gold is not evidence of data-center demand.</b> In Q2 2026, technology used 80.4 tonnes out of 1,268.9 tonnes of total gold demand, about 6.3%. Reserve, investment, currency and risk motives matter. Central-bank purchases in H1 were 345 tonnes, the lowest first-half figure since 2022; Q1 estimates were revised sharply downward. A higher gold price cannot uniquely diagnose “loss of trust.”','gold','goldcb')
p('Silver and copper are relevant electrical inputs, but their prices also respond to supply, inventories, other uses and monetary conditions. Crypto prices establish tradable demand for the assets, not the realized productivity of decentralized coordination. Agriculture and timber give useful counterweights: not every real asset shares the electrical-equipment cycle.')
table(['Adjusted fund return','2022','2023','2024','2025','2026 to Oct 9'],[[s]+[pct(A[s][str(y)]) for y in range(2022,2027)] for s in ['SPY','QQQ','TLT','GLD','XLE','ICLN']],[100,80,80,80,80,80])
p('Calendar-year changes, except the explicitly partial 2026 column.','prices',small=True)

title('Real estate: location and use matter more than the label')
prop=json.loads((O/'property.json').read_text());d={(r['area'],r['kind']):r for r in prop if 'change_pct' in r}
rows=[]
for c,label in [('US','United States'),('CN','China'),('XM','Euro area'),('IN','India'),('DE','Germany'),('DK','Denmark'),('GB','United Kingdom')]:
 n=d[c,'N'];rr=d[c,'R'];rows.append([label,n['start_date']+' → '+n['end_date'],pct(n['change_pct']),pct(rr['change_pct'])])
table(['Residential property','Actual five-year interval','Nominal','CPI-deflated'],rows,[119,165,108,108])
p('BIS series: national/regional residential price indices in local currency. Real means adjusted for domestic consumer inflation, not USD conversion. These are price changes excluding rent, leverage, maintenance and taxes; comparison quarters differ because publication lags differ.','bis')
p('Listed US property returned only '+ret('VNQ')+' including the vendor distribution adjustment. That aggregate hides BXP at '+ret('BXP')+', Digital Realty at '+ret('DLR')+' and Equinix at '+ret('EQIX')+'. Office, powered data-center sites and housing have different demand and financing structures. A REIT share is not the same instrument as an unlevered building.','prices')
p('CBRE’s H1 survey of primary North American data-center markets recorded 10,903 MW of inventory, up 33.7% year on year; 1.4% vacancy; and 7,481 MW under construction, 80.4% preleased. Those are strong local scarcity signals. Preleasing does not establish end-customer AI profitability, uninterrupted financing, or actual compute utilization.','cbre')
p('Digital Realty reported Q2 core FFO excluding promote income of $2.13 per share versus $1.87. Its 2026 guidance on that basis was $8.15–$8.20. At the sampled $178.76 close, that is about <b>21.9 times guided recurring core FFO</b>. Reported Q2 core FFO of $2.65 contains promote income and would overstate the repeatable run rate. Cash renewal rents rose 25.4%.','dlr')
p('<b>The defensible inference:</b> within real estate, power access and specialized usable capacity have become more valuable relative to some conventional space. China’s falling housing values and contracting development alongside electrical investment show a changing composition of capital formation. We have not traced a flow proving that a dollar withdrawn from housing went into data centers.')
p('Emaar is a useful GCC company case, not a national house-price index: H1 revenue was AED23.9bn, up 21%, with a large AED164.9bn revenue backlog. The business and equity are influenced by sales mix, timing, leverage and local development policy. GCC property coverage in this study remains less complete than US, European and Chinese coverage.','emaar')

title('Physical buildout: what is actually being added')
fig('physical_capacity.png',495)
cap=list(csv.DictReader((O/'renewable_capacity.csv').open()))
table(['Region','End-2021 GW','End-2025 GW','Annual compound growth'],[[r['region'],f"{float(r['2021_GW']):,.1f}",f"{float(r['2025_GW']):,.1f}",f"{float(r['CAGR_2021_2025_pct']):.1f}%"] for r in cap],[125,120,120,135])
p('Four annual intervals, not a five-year CAGR. Renewable generation nameplate capacity excludes nuclear and does not measure firm supply or electricity produced. GCC is the sum of Bahrain, Kuwait, Oman, Qatar, Saudi Arabia and the UAE; its very high growth comes from a small base.','irena')
p('The IEA estimates $3.4tn of total energy investment in 2026, including about $665bn in renewable power, about $550bn in grids and more than $100bn in storage. These categories should not be added to hyperscaler equipment spending as if all boundaries were independent. Grid spending is up roughly 20% in a year; that is nominal investment, not a 20% increase in energized line capacity.','iea')
p('The EIA reports US operating battery power capacity of 43.6 GW at end-2025 and about 52 GW by June 2026. Another 54 GW was planned over the following two and a half years. That is <b>additional planned capacity</b>, not an increase from 52 to 54 GW. Power in GW does not specify duration or stored energy in GWh.','storage')

title('US compute: real spending, incomplete proof of final returns')
p('Nvidia’s quarter ended July 26, 2026 generated $96.2bn in revenue, up 106%; data-center revenue was $89bn. Its FY2022 revenue, for the year ended January 2022, was $26.9bn. The change in scale is unmistakable, but comparing a quarter with an earlier year is not a like-for-like growth rate. The sampled equity price rose '+ret('NVDA',False)+', and the valuation screen shows about $5.54tn of market value.','nvda','nvda21','values')
table(['Customer / supplier','Observed operating evidence','What it does and does not prove'],[
['Microsoft, FY2026 Q4','$41bn capex including leases; about two-thirds in short-lived CPU/GPU assets; cloud revenue $59.3bn, +27%','A disclosed company-specific spending mix. It does not establish the mix of the whole industry.'],
['Amazon, H1 2026','$96.3bn cash capex versus $55.6bn a year earlier','Includes AWS and logistics; not all AI.'],
['Meta, Q2 2026','$31.08bn capex; $0.784bn free cash flow versus $8.55bn','Cash investment can rise much faster than current cash returns.'],
['Arista, Q2 2026','$3.036bn revenue, +37.7%; GAAP operating margin 45.4%','Network scaling generates delivered revenue and substantial profit.'],
['TSMC, Jan–Sep 2026','NT$3.899tn revenue, +41.1%, unaudited monthly totals','Foundry demand is visible upstream; revenue is not a pure AI measure.']],[103,210,187])
p('Primary evidence for the table. Microsoft’s capex accounting includes leases; Amazon’s row is cash capex. These are deliberately not summed.','msft','amzn','meta','arista','tsmc',small=True)
p('<b>Why monetization remains open.</b> Customers are already paying for cloud services, advertising and software. That does not isolate the incremental return from the latest AI capital wave. Microsoft reported cloud gross margin of 65%, down as AI investment scaled. Meta’s net profit also reflected legal and restructuring charges, so it is incorrect to attribute the entire decline to AI.','msft','meta')
p('A disciplined test is incremental gross profit and customer retention against depreciation, power, operating costs and replacement capex. Cash flow should be reconciled to leases and financing classifications. Microsoft’s calendar-2026 capex headline changed with a shift between finance and operating leases; an accounting change is not automatically a reduction in physical construction.','msft')
p('The strongest near-term conclusion is rapid equipment installation and network expansion. A universal productivity boom, sustainable final-customer returns, and the eventual market-clearing price of inference are not yet established by these filings.')

title('Below the megacaps: the valuation cross-section')
rows=[]
for s,l,c in [('NVDA','Nvidia','USD'),('VRT','Vertiv','USD'),('ETN','Eaton','USD'),('PWR','Quanta Services','USD'),('POWL','Powell Industries','USD'),('HPS-A.TO','Hammond Power Solutions','CAD'),('AAON','AAON','USD'),('BELFB','Bel Fuse B','USD'),('MYRG','MYR Group','USD'),('ITRI','Itron','USD'),('MOD','Modine','USD'),('STRL','Sterling Infrastructure','USD'),('FSLR','First Solar','USD'),('FLNC','Fluence*','USD'),('PLUG','Plug Power','USD')]:rows.append(companyrow(s,l,c))
table(['Company','Price change','Current market cap','TTM P/E','Forward P/E'],rows,[160,76,108,78,78])
p('Price changes use the observed 2021–2026 window, except Fluence from 28 October 2021. Current valuation screens were retrieved 12 October 2026; “—” or “n/a” is not zero. Forward multiples use provider definitions and may exclude items included in trailing earnings. CAD and USD caps must not be directly ranked without conversion.','prices','values',small=True)
p('The smaller-company evidence matters: Bel, Itron, Hammond, MYR and Fluence are still only a few billion in equity value, while Powell and AAON are around $7bn. Some historical small caps have become much larger. A “small-cap theme” cannot be tested by classifying today’s winners using today’s size alone.')
p('The cross-section says investors distinguish scarce electrical equipment from commodity exposure and difficult execution. It does not say that every company in the favored category will win. Itron’s lower multiple coincides with falling total revenue despite growing recurring software revenue; Fluence has demand but major delivery problems.')
p('<b>A rising industry can still deliver a poor stock return.</b> As a purely illustrative calculation, earnings growing 10% annually for five years while P/E falls from 40 to 20 leave the stock price at 0.81 times its starting level, before dividends. Conversely, at a stable multiple, the same earnings growth lifts price by 61%. Valuation is a claim on an uncertain future, not an extra unit of installed infrastructure.')

title('Smaller companies: earnings and execution validate the theme')
p('<b>Hammond Power Solutions: transformers.</b> Annual sales rose from about C$380m in 2021 to C$558m in 2022, C$710m in 2023, C$788m in 2024 and C$898m in 2025: approximately 24% compound annual growth over four years. Q2 2026 sales reached C$325m, up 44.7%; adjusted EBITDA was C$53m, a 16.4% margin. Backlog was up 96.9% year on year but down 6.9% sequentially as deliveries overtook bookings. The stock rose far more than revenue, so operations alone cannot explain its repricing.','hpshist','hps')
p('<b>Powell: switchgear and power distribution.</b> FY2021 sales were $470.6m with just $1.0m of operating income. The quarter ended June 2026 alone produced $312m revenue, $52.2m net income and a 30.6% gross margin. Orders were $934m, 3.0 times sales; backlog was $2.4bn, up 69%. A $400m data-center-related order sits alongside LNG and fertilizer work. The business serves a wider power and industrial expansion. One large order also makes quarterly growth lumpy.','powl21','powl')
p('<b>AAON: cooling capacity meets ramp costs.</b> Q2 revenue was $627m, up 101.2%, and operating income was $68.9m, up 192.1%. Backlog approached $2bn but fell 7.4% sequentially. Gross margin declined from 26.6% to 24.3% during the production ramp. Faster conversion is good for delivery, but the cost of expanding manufacturing can absorb some of the benefit. BASX-branded sales and the BASX reporting segment are different measures and should not be interchanged.','aaon')
p('<b>Bel Fuse: components and power electronics.</b> Q2 revenue rose 25.1% to $210.7m, but GAAP net income fell to $25.5m from $26.9m while adjusted earnings rose. The company also raised $441.6m of equity and repaid debt. Demand spans data centers and defense; dilution and accounting adjustments matter alongside the headline growth rate.','bel')
p('<b>MYR: construction is not one cycle.</b> Q2 revenue was about $1.08bn. Transmission/distribution revenue rose only about 3.5%, while commercial/industrial revenue rose about 41.5%. That does not refute a global grid boom; it shows one contractor’s mix and project timing.','myr')
p('<b>Vertiv and Eaton confirm scale beyond niche cases.</b> Vertiv’s Q2 revenue rose 24%, but organic growth was 18%; acquisitions and currency explain the remainder. Its adjusted operating margin reached 22.6%. Eaton’s Electrical Americas rolling orders grew 41% and backlog 33%. Neither reported growth rate should be casually treated as an equivalent increase in physical equipment volumes.','vertiv','eaton')
p('<b>Quanta’s $53.4bn backlog is not all firm purchase orders.</b> Its Q2 release distinguished $33.6bn in remaining performance obligations from estimates embedded in master service agreements. Revenue reached $9.56bn versus $6.77bn. Contractors can capture the expansion too; “equipment always beats construction” is contradicted by the sample.','quanta')

title('Europe: grid technology, constrained projects, selective returns')
table(['Company / signal','Observed evidence','Interpretation'],[
['Prysmian','Q2 organic growth: transmission 14.3%, power grid 13.0%, digital solutions 18.0%','Energy and data connectivity are expanding inside one supplier.'],
['NKT','Q2 transmission backlog about €13bn, versus €13.5bn in Q1','A large book with ongoing conversion; falling backlog is not automatically falling demand.'],
['Schneider Electric','Q2 revenue €11.5bn; organic growth 17%','Electrical and control equipment demand reaches a diversified vendor.'],
['Ørsted','H1 offshore generation +23%; underlying EBITDA +8%; ROCE 3.1%','More energy produced can coexist with weak capital returns.']],[111,205,184])
p('Primary company releases. NKT figures at current metal prices; its standard-metal-price backlog differs. Ørsted recorded impairments and lower net earnings.','prysmian','nkt','schneider','orsted',small=True)
p('Prysmian shares rose '+ret('PRY.MI',False)+' in EUR, Schneider '+ret('SU.PA',False)+' in EUR, and NKT '+ret('NKT.CO',False)+' in DKK over the sample. Vestas fell '+ret('VWS.CO',False)+'. Ørsted’s vendor price series fell roughly 84%, but its rights issue means that number is <b>not</b> a complete investor-return calculation. Rights participation or sale proceeds would need reconstruction.','prices')
p('These cases suggest that the ability to connect, control and deliver power can capture more value than simply having a development pipeline. Offshore construction costs, financing, permitting and contractual pricing create risks distinct from manufacturing cables or electrical gear. It is a sector and contract distinction, not a judgment that renewable generation stopped growing.')
p('<b>What Europe is scaling:</b> transmission, interconnection, electrical equipment, industrial efficiency, networks and a more flexible power system. Renewable capacity in the EU rose from 515 GW to 779 GW between end-2021 and end-2025. That physical growth sits beside weak outcomes for some developers.','irena')
p('<b>Immediate to one year:</b> complete substations and connections, strengthen project contracts, use storage and demand flexibility, and expand scarce equipment and skilled labor. <b>Five years:</b> larger transmission and interconnector projects, electrified industry and generation that can be financed at realistic costs. Many of these needs survive an AI-capex slowdown because their customers include households, industry and renewable projects.')
p('Europe is also an exporter of infrastructure capability. Its listed companies’ revenues and valuations cannot be interpreted as measures only of construction inside Europe. Conversely, a European growth bottleneck can create revenue for an Indian factory or a Chinese component supplier.')

title('China: manufacturing scale, falling property, uneven profits')
p('China’s renewable capacity rose from 1,018 GW at end-2021 to 2,258 GW at end-2025. State Grid invested more than CNY310bn in H1 2026, up 12.6%, and reported commissioning the Shaanbei–Anhui ultra-high-voltage link. This is direct evidence of grid construction and integration, not an inference from AI stocks.','irena','sgcc')
p('CATL’s 2025 battery sales reached 661 GWh, up 39%; revenue was CNY423.7bn, up 17%, and net profit CNY72.2bn, up 42%. Manufacturing capacity was 772 GWh, with a further 321 GWh under construction. These are different quantities: shipments, plant capability and future capacity. The company also spent CNY22.1bn on research.','catl')
table(['Chinese company','Local price change','Valuation / meaning'],[
['CATL',ret('300750.SZ',False),'CNY1.40tn cap; screen forward P/E 12.6×'],
['Sungrow',ret('300274.SZ',False),'CNY169.7bn cap; forward P/E 11.3×'],
['LONGi',ret('601012.SS',False),'PV manufacturing exposure; severe price decline'],
['SMIC',ret('0981.HK',False),'HKD-listed semiconductor manufacturing'],
['Foxconn Industrial Internet',ret('601138.SS',False),'CNY-listed electronics and computing infrastructure']],[158,112,230])
p('Prices and valuation screens; local-currency returns, not USD. These are different securities and competitive positions.','prices','values',small=True)
p('The lesson is not that Chinese battery firms fail to earn profits—CATL contradicts that. It is that large physical gains do not require large five-year share gains, particularly when the starting price assumed rapid growth. For more commoditized suppliers, competition can transfer benefits to users through cheaper equipment.')
p('At the same time, NBS reported property-development investment down 19.9% and new starts down 24.8% in January–August 2026. BIS real residential prices fell about 25.1% over five years through Q2 2026. This supports a changing composition of investment, but does not prove that electrical investment fully offsets property’s macroeconomic drag.','china','bis')
p('<b>What China contributes globally:</b> industrial manufacturing capacity, batteries, power electronics, solar equipment and increasingly semiconductor capability. A verified example of the remaining interdependence is Fluence’s September 2026 global battery supply agreement with EVE Power; US localization is handled separately. Trade barriers modify the network rather than erase every connection.','eve')
p('<b>Next year:</b> grid absorption, storage deployment, export access, factory utilization and cash discipline matter more than another capacity announcement. <b>Five years:</b> further electrification, industrial automation, recycling and system integration are plausible extensions. Neither a property rebound nor ever-rising equipment margins is necessary for that physical pathway.')

title('India: domestic electrification and an export construction layer')
p('India’s renewable capacity grew from 147 GW to 251 GW between end-2021 and end-2025. MNRE’s September 2026 non-fossil total was 308 GW, including nuclear, with about 24.6 GW added in the first half of the fiscal year. The figures are not interchangeable: they use different dates and technology boundaries.','irena','india')
p('Hitachi Energy India’s April–June 2026 revenue was INR24.94bn, up 68.6%; backlog was INR322.22bn. Underlying orders grew 26.1% excluding large HVDC orders, and exports accounted for 33.6% of orders on that same exclusion basis. Its new factory activity and export orders link Indian production to customers in Europe, North America and South Asia.','hitachi')
p('Larsen &amp; Toubro’s June order book was INR7.79tn, up 27%. International business represented 52%; 71% of that international book was in the Middle East and 14% in Europe. The arithmetic implies about <b>37% of its total backlog is Middle Eastern</b>. This is a concrete cross-regional relationship, not a generic “India growth” story. The book contains conventional energy, green energy, infrastructure and utilities.','lt')
table(['Indian company','INR price change','Current valuation where checked'],[
['Hitachi Energy India',ret('POWERINDIA.NS',False),'INR1.39tn cap; forward P/E 79.9×'],
['Larsen &amp; Toubro',ret('LT.NS',False),'INR4.98tn cap; forward P/E 23.8×'],
['KEC International',ret('KEC.NS',False),'INR96.6bn cap; forward P/E 13.2×'],
['Kalpataru Projects',ret('KPIL.NS',False),'Construction and transmission exposure'],
['ABB India',ret('ABB.NS',False),'Electrical equipment and automation'],
['Polycab',ret('POLYCAB.NS',False),'Wires and cables']],[171,109,220])
p('Selected examples, not a complete sector portfolio.','prices','values',small=True)
p('The contrast between Hitachi Energy India and KEC is large enough to reject the idea that all infrastructure businesses receive the same benefit. Pricing power, execution terms, working capital and valuation matter. A nearly 80-times forward multiple is a demanding expectation, not evidence of an inexpensive opportunity.')
p('The local Nifty index rose about 25.5%, but the USD-listed INDA fund’s adjusted change was only '+ret('INDA')+'. USD/INR rose from about 75.31 to 96.82: that is a 28.6% increase in the quotation, equivalent to a <b>22.2% fall in the rupee’s USD value</b>. Index composition, distributions and fees also explain differences.','prices')
p('<b>Next year:</b> manufacturing throughput, substations, storage, power quality and execution of the existing order book. <b>Five years:</b> more reliable industrial electricity and exported engineering capability. India can supply pieces of both Gulf construction and European electrification while its own domestic system expands.')

title('GCC: power, water, gas and urban capacity built together')
p('The six GCC states’ renewable capacity increased from about 3.8 GW in 2021 to 23.9 GW in 2025. That is rapid growth from a small base; it is not evidence that hydrocarbons have been displaced. The emerging infrastructure mix combines gas, renewables, storage, desalination, urban development and planned compute.','irena')
p('ACWA’s H1 2026 portfolio headline was 98.2 GW, but that includes operating, construction and development projects. Its 32 projects under construction represented about 47 GW plus water capacity. Actual H1 additions reaching commercial operation included 0.8 GWh of batteries and 0.9 million cubic metres per day of water. Profit fell to SAR653m from SAR909m. <b>Portfolio, construction and commissioning are three separate stages.</b>','acwa')
p('Aramco reported Q2 adjusted net income of $33.4bn, operating cash flow of $25.4bn and free cash flow of $12.3bn. Expansion at Jafurah and Fadhili targeted 2027, showing continuing investment in gas supply. QatarEnergy’s November 2025 plan envisaged LNG capacity rising from 77 to 142 million tonnes per year by 2030; it is a pre-conflict target whose timing should not be treated as assured in October 2026.','aramco','qatar')
table(['Public-market signal','Observed change / valuation','Boundary'],[
['UAE / Saudi / Qatar funds',ret('UAE')+' / '+ret('KSA')+' / '+ret('QAT')+' adjusted USD','Different sector composition; not comparable pure infrastructure baskets'],
['Emaar',ret('EMAAR.AE',False)+' price; '+ret('EMAAR.AE')+' adjusted','Company equity, not a Dubai house-price index'],
['ACWA',ret('2082.SR',False)+' since Dec 2021; forward P/E 51.3×','Shorter data history; high expected growth and execution exposure'],
['Aramco',ret('2222.SR',False)+' price; '+ret('2222.SR')+' adjusted','Distributions materially change the result']],[115,202,183])
p('Price data in local currency for companies and USD for regional funds. Valuation screens retrieved 12 October.','prices','values',small=True)
p('<b>What is being assembled:</b> energy and water services that support industry, cities, logistics and digital activity. Compute sites also require chips, fiber, customers, cooling, security and credible power contracts. We do not count announced sovereign AI campuses as commissioned capacity or profitable demand.')
p('The less obvious link is that Gulf capital buys a multinational production system: Indian engineering, imported electrical equipment and batteries, international software and chips, and local energy and land. L&amp;T’s order book demonstrates one part of this directly. ACWA’s water commissioning demonstrates that “AI and power” is too narrow a description of the region’s capacity buildout.')
p('<b>Immediate to one year:</b> execution, supply routes, contracted power and water, commissioning and financing continuity. <b>Five years:</b> finish economically supported gas, grid, storage, desalination and industrial projects; stage compute expansion against actual power and customer commitments. Conflict risk can delay, relocate or raise the cost of that process.')

title('What the regions are scaling together')
table(['Link','Concrete evidence','System-level inference'],[
['Compute ↔ electricity','Hyperscaler capex; Vertiv, Powell and Eaton demand; Google flexibility contracts','Information processing is becoming a larger electrical customer, and a potentially flexible one.'],
['China ↔ global storage integrators','EVE–Fluence agreement; CATL manufacturing scale','Factory scale supplies an international deployment network, modified by localization rules.'],
['India ↔ Gulf and Europe','L&amp;T international backlog; Hitachi Energy India export orders','Engineering and equipment cross borders even when the final asset stays local.'],
['Europe ↔ global power and data','Prysmian transmission, power-grid and digital growth; Schneider demand','Connectivity and control technology participate in several regional expansions.'],
['GCC energy ↔ urban and industrial services','ACWA commissioned water and batteries; Aramco gas investment','Power alone is insufficient; water, land, logistics and contracts complete the service.'],
['Taiwan and semiconductor supply ↔ global compute','TSMC sales growth; Nvidia and Arista revenue','Fabrication, design and networking must scale together.']],[105,198,197])
p('Source support is provided in the regional and company pages; these connections are synthesis, not estimates of global trade shares.')
p('<b>The common product is reliable service capacity.</b> A useful data center combines semiconductor fabrication, networks, electrical supply, thermal management, buildings, software, trained staff, security and enforceable contracts. Many of the same components also support factories, homes and electrified transport. The apparent separate booms are partly demand for shared complements.')
p('The relationship is neither purely coordinated nor purely coincidental. Different motives—industrial development, energy security, climate policy, AI, replacement of aging assets—converge on transformers, copper, substations, engineering labor and finance. Demand can be mutually reinforcing while countries duplicate capacity, restrict exports or compete for the same equipment.')
p('This explains a pattern that a technology-only narrative misses: <b>the scarce asset is often the permission and practical ability to operate at a location</b>. A connected site, an executable construction contract, reliable water or a firm power arrangement can be more valuable than another unconnected machine. It also explains why a fast-growing end market can squeeze supplier profits if manufacturing becomes abundant.')
p('The data do not demonstrate that the world is building a single intelligence, that digital minds will replace population, or that space expansion is the main destination of present capital. Those remain separate hypotheses. The earnings-supported buildout is much more concrete: electricity delivery, compute, connectivity, industrial equipment and supporting institutions.')
title('Physical success and shareholder returns can diverge')
fig('company_divergence.png',495)
p('<b>Fluence is a direct test of the distinction.</b> Its September 16 revision cut expected FY2026 revenue to about $2.4bn, from the prior $3.0bn midpoint, and changed expected adjusted EBITDA from a $10m loss to a $200m loss. Management cited US manufacturing and supply-chain problems while describing demand as strong. This supersedes the August outlook. A needed product and a large backlog did not prevent a severe execution shortfall.','fluence')
p('The chart compares selected local-currency price paths, normalized to the same starting level on a logarithmic scale. It is not an equal-weighted strategy or a complete industry index. The electrical-equipment winners and renewable-manufacturing losers were chosen to test whether a single deployment story can explain shareholder returns. It cannot.')
p('CATL is especially informative: substantial battery shipments and profit growth coexist with a modest five-year share-price change. Meanwhile, Powell and Hammond experienced both substantial operational expansion and much larger equity repricing. Starting expectations and later expectations matter alongside actual earnings.')
p('If abundant batteries lower project costs, users can capture value that suppliers previously retained. If transformer capacity catches up, connections can become easier even as manufacturer margins fall. A successful transition need not preserve today’s scarcity profits; society’s productive gain and an incumbent investor’s gain are different outcomes.')

title('Coordination and trust: already being built, still incomplete')
p('The original essay says renewables lack a coordination layer and AI lacks a trust layer. A more accurate claim is that these layers exist and are being expanded, but their capabilities are uneven and often lag the new load.')
p('<b>Contracts and flexibility.</b> Google announced 1 GW of demand-response capacity incorporated in long-term utility contracts in March 2026. It can shift or limit some machine-learning workloads. This is signed flexibility, not proof of a continuously delivered 1 GW reduction. It shows a concrete way in which compute and grid operation are becoming coupled.','google')
p('<b>Software and instrumentation.</b> Itron’s Q2 total revenue fell 7% to $563m, while annual recurring revenue rose 21% to $417m and its Outcomes business grew 13%. Hardware cycles and software/service adoption can move in different directions. The control layer is not simply absent.','itron')
p('<b>Reliability institutions.</b> PJM’s July 2026 auction for delivery in 2028/29 cleared at the regulated $325/MW-day cap and fell 6,831 MW short of its reserve criterion. That is a procurement shortfall, not a forecast that outages will necessarily occur. It is evidence that generation, load forecasts, contracting, reliability rules and cost allocation are not automatically matching.','pjm')
p('<b>Digital security.</b> CrowdStrike’s quarter ended July 2026 produced $1.47bn revenue, up 26%, ARR of $5.84bn, up 25%, and $377m free cash flow. GAAP operating loss was $33.2m while adjusted operating income was $371.6m. There is monetized security demand; the accounting distinction remains material. This does not measure a separate market for autonomous-agent identity or liability.','crwd')
p('The next institutional tasks are practical: permissions for agents, verifiable delegation, access control, audit trails, evaluation in real workflows, incident recovery and allocation of responsibility. On the power side they include interoperable equipment, credible load forecasts, network charging, connection processes and enforceable flexibility. These are inferred complements needed to use the installed hardware, not a dollar-sized market forecast.')
p('Automation is also broader than generative AI. IFR’s 2026 release reports approximately five million industrial robots operating at end-2025, up 9%, with China accounting for 59% of new installations. This is established industrial deployment. It should not be conflated with announced humanoid factories or assumed near-term general-purpose robot economics.','ifr')
p('Security and continuity also have a physical dimension. SIPRI estimated 2025 military expenditure at $2.887tn, up 2.9% in real terms, with European spending up 14%. Defense-equity strength has a procurement context. It does not establish that all such spending improves welfare or productive efficiency.','sipri')

title('Which phase are we in? Separate the clocks')
table(['Layer','Evidence now','Best-supported phase'],[
['AI accelerators and networks','Rapid delivered revenue and customer spending','Large-scale installation; replacement and utilization risks remain'],
['Data-center buildings / power / cooling','Low surveyed vacancy; strong equipment deliveries and orders','Installation constrained by power, connections and execution'],
['Grid transmission / transformers / cables','Global spending and order growth','Capacity expansion around bottlenecks; regional timing differs'],
['Solar manufacturing','Rising deployment with weak supplier share performance','Mature scale and competitive pressure in important segments'],
['Battery storage','Rapid operating additions; uneven manufacturer/integrator cash flow','Deployment acceleration plus manufacturing and delivery adjustment'],
['AI workflow / trust institutions','Real security revenue, but incomplete agent-specific evidence','Integration and institutional adaptation'],
['GCC megaprojects','Large books of construction and development; selective commissioning','Execution with financing and geopolitical exposure']],[129,208,163])
p('<b>Ordering is the open question.</b> Claude views falling Hammond and AAON backlogs as a possible late-ordering / early-conversion warning. My assessment is that the order-cycle peak is undetermined: shipments, order timing and capacity ramps can produce the same pattern. We agree that no broad demand peak is established by those two observations, especially alongside Powell’s strong book-to-bill.')
p('The agreed test is sustained bookings below shipments accompanied by wider pricing pressure, cancellations or margin weakness after ramp costs normalize. A backlog that falls because profitable deliveries accelerate is not the same as one that falls because customers cancel.')
p('<b>Financial maturity can precede physical maturity.</b> A supplier can still have years of work while its share price already anticipates much of the growth. Conversely, a falling share price can coexist with useful capacity delivered to customers. High forward multiples show demanding expectations, but cannot establish that “everything is priced in.”')
p('The five-year sequence is therefore better understood as overlapping adjustments: the 2021 starting point contained optimistic valuations in parts of clean technology; 2022 exposed rate and energy sensitivity; later compute demand increased orders for chips and supporting equipment; today the constraint often lies in delivering, connecting and economically using the systems. The return paths and operational releases support this narrative, but they do not prove a single global causal sequence.')

title('What needs to be built now, next year and over five years')
table(['Horizon','Priority implied by observed constraints','Evidence or timing anchor'],[
['Now–end 2026','Finish and energize existing projects; switchgear, transformers, cooling, power quality, fiber and skilled commissioning; verify customer credit and contracts','Powell/Eaton orders, CBRE vacancy, manufacturing delays and PJM procurement shortfall'],
['Through October 2027','Expand factory throughput; substations and local grid reinforcement; storage with dispatch arrangements; exercise flexibility contracts; improve construction cash discipline','Existing backlog conversion and actual storage commissioning are more informative than new announcements'],
['Through October 2027','Make AI useful in workflows: security, permissions, evaluation, data integration and monitoring; measure unit economics','Cloud and security revenue show demand; sector-wide incremental AI returns remain unresolved'],
['2028–October 2031','Staged transmission/HVDC, larger substation networks, turbine and electrical factory capacity, storage and economically contracted firm supply','Long delivery cycles and disclosed manufacturing expansion targets'],
['2028–October 2031','Semiconductor and network upgrades, industrial automation, water infrastructure, maintenance, recycling and skills','Existing regional capacity and order patterns; no guarantee that every announced project clears its financing hurdle']],[96,232,172])
p('This is a set of inferred priorities, not an assertion that all current shortages deserve unlimited investment. Demand must be credible at the delivered price, and the people paying for the infrastructure may differ from those using it.')
p('<b>Quantitative five-year anchors.</b> The IEA forecasts data-center electricity consumption rising from 485 TWh in 2025 to 950 TWh in 2030, about 14.4% annually, reaching roughly 3% of global electricity. Its 2025 growth estimate was 17%, compared with 3% for world electricity overall. Local concentration makes the grid impact much larger than the global share suggests. These are estimates and forecasts, not guaranteed demand.','ai')
p('GE Vernova’s June 2026 gas equipment position comprised 53 GW of firm backlog and 63 GW of slot reservations. It shipped 3 GW in Q2. Management targeted a 20 GW annual manufacturing rate in Q3 2026, 24 GW in 2028 and 30 GW in 2030. These targets provide a concrete supply-response clock; reservations must not be reported as completed plants.','gev')
p('The EIA’s planned additional 54 GW of US battery power by end-2028 is another execution clock. Plans can slip, and GW alone cannot establish adequacy during a multi-day supply shortfall. New generation, storage, networks and demand flexibility should be evaluated as a system.','storage')
p('Fusion, large-scale space power and a digital-mind population are not required to explain this five-year base case. The practical task is converting equipment, contracts and knowledge already being financed into reliable services and cash-generating uses.')

title('What would change this assessment?')
table(['Scenario / test','What to watch','Implication'],[
['Base: continued installation with uneven returns','Commissioned capacity grows; orders broadly convert; cash generation improves after ramps','Physical thesis survives while stock selection remains difficult'],
['AI spending pause','Hyperscaler cash and lease commitments fall; cancellations rise; utilization or rental pricing weakens','Compute-specific suppliers face downside before the installed asset base shrinks'],
['Successful integration','Faster connections; flexibility actually dispatched; higher utilization and customer gross profit','More useful output per unit of capital; supplier scarcity rents may normalize'],
['Execution or financing failure','Working-capital stress, project delays, cost overruns, defaults, equity dilution','A real end-market need fails to become profitable company growth'],
['Geopolitical or energy disruption','Supply routes, fuel costs, insurance, export permissions, regional commissioning delays','The geography, cost and timing of deployment change'],
['Equipment supply catches demand','Shorter lead times, falling reservation premiums, softer pricing and book-to-bill','The system can improve while incumbent supplier margins and multiples compress']],[121,217,162])
p('<b>Quarterly dashboard.</b> Track actual orders separately from reservations; backlog conversion and cancellations; organic sales versus acquisitions; gross margin versus temporary ramp costs; cash flow versus adjusted earnings; customer concentration; and leverage or dilution. Follow energized MW, battery GWh and utilization alongside revenue. A firm can grow revenue while destroying capital.')
p('<b>Annual dashboard.</b> Compare grid and data-center capex with completed assets, power adequacy, customer adoption and incremental cash returns. Test whether grid investment remains strong in a year of weaker AI investment. That would help distinguish the shared equipment cycle from AI’s specific contribution.')
p('Do not use an arbitrary threshold as a universal law. Two quarters of weak bookings with broader pricing pressure is a useful warning rule proposed in our discussion, not a statistically validated cycle predictor. Likewise, a change in Treasury yields affects valuations without necessarily changing the amount of hardware already installed.')
p('<b>Stranding is specific.</b> Accelerators can age quickly; a building, connection or turbine may last longer. But even durable assets can strand if they are in the wrong location, lack water or power rights, or serve a customer that cannot pay. The fiber-bubble analogy is therefore a possibility to investigate, not a promise that every AI loss leaves society a reusable asset.')

title('What the actual Claude discussion changed')
p('This was a real four-round exchange through the installed Claude CLI, with read-only research tools. The accompanying transcript contains our prompts and Claude’s replies. Earlier replies include preliminary claims later corrected; they are retained for transparency and are not all endorsed by the final report.')
table(['Question challenged','Resolution'],[
['Is this mostly data-center equipment, with little broad grid modernization?','Claude withdrew the broad claim after global grid spending, State Grid, Prysmian and India evidence. Growth still differs by segment.'],
['Can Nvidia revenue divided by hyperscaler capex establish the share spent on short-lived assets?','No. Overlapping scopes and double counting invalidate that inference. Microsoft’s own disclosed mix is usable for Microsoft.'],
['Do falling Hammond/AAON backlogs prove a demand peak?','No. Conversion, capacity ramps and lumpy awards can explain it. The timing warning remains an explicit hypothesis to monitor.'],
['Does coordination advance mainly through administrative rationing?','Unsupported as a sector-wide share. The evidence includes software, physical networks, contracts and institutions.'],
['Does gold prove that society is repricing trust?','No unique attribution. Gold stays in the asset analysis without carrying the infrastructure conclusion.'],
['Do equipment firms necessarily beat contractors?','No. Quanta and Sterling are counterexamples. Pricing, contracts, execution and entry valuation matter.'],
['Can the civilization framework itself be established from market data?','No. It is an interpretation; specific deployment, profit and scarcity mechanisms can be tested.']],[240,260])
p('One interpretation remains explicitly open: Claude’s prior is that non-AI drivers dominate grid investment outside the US; this study does not quantify that share. We agree that AI is not the only driver and that the physical coupling is real. A future year with falling AI capex and sustained grid investment would help test the distinction.')
p('Numerical checks also mattered: the rupee’s USD depreciation is about 22.2%, not the 28.6% increase in USD/INR; the latest PJM procurement shortfall is 6,831 MW; Fluence’s September revision supersedes its August outlook; and EIA’s 54 GW is additional planned storage, not the future total.')
p('<b>Our shared conclusion:</b> the physical buildout is real, global and broader than Nvidia or AI. What becomes economically useful depends on the complements that deliver reliability and adoption. What becomes financially attractive also depends on price paid, financing and who captures the surplus. Agreement between two assistants is not independent proof; the linked data and falsification tests carry the argument.')

title('Data notes and reproducibility')
p('The accompanying CSVs contain the extracted values and source URLs. The project also retains raw Yahoo daily JSON, raw valuation-page text, downloaded IRENA material, BIS CSV responses, scripts and the Claude exchange. Returns and charts can be regenerated from the archived inputs. Refetching later can change vendor adjustments and revised macroeconomic observations.')
table(['File','Contents'],[
['market_prices.csv','126 usable price/quote series plus 4 explicit failures; start/end dates, local currency, price and adjusted changes, source and special warnings'],
['annual_returns.csv','Calendar-year adjusted changes, partial 2021/2026 windows and sampled maximum drawdowns; excludes the Treasury yield series'],
['valuations.csv','Current market cap, enterprise value, trailing/forward multiples and selected financial metrics; source and retrieval date'],
['property.csv','BIS nominal and real residential price indices with exact five-year comparison quarters'],
['renewable_capacity.csv','IRENA 2021–2025 end-year renewable GW and four-year compound growth'],
['company_evidence.csv','Selected primary-source revenue, earnings, orders and commissioning observations'],
['sources.json','Linked source register for the report'],
['claude_discussion.txt','Actual four-round prompts and responses, with notice that preliminary claims were corrected'],
['research_bundle.zip','The report, charts, tables, source register, dialogue and reproducibility scripts']],[139,361])
p('Important adjustments: futures quotation changes are not investment returns; ^TNX is a yield and its change is in basis points; crypto uses daily observations through the common cutoff. Rights issues at Ørsted and NKT and spinoffs at GE and Reliance require separate treatment to reconstruct a complete shareholder outcome. The report avoids calling their raw vendor changes complete total returns.')
p('BIS real property series use local CPI; “real” does not mean exchange-rate adjusted. REIT FFO and AFFO are not interchangeable with ordinary industrial-company earnings. Organic growth, reported growth and non-GAAP earnings are labelled when used. Portfolio GW, construction GW, commissioned GW, battery GWh and electricity TWh are not combined into one growth metric.')
p('Snapshot valuations are not a historical P/E panel. This report combines five-year asset-price paths, selected multi-year fundamentals and current valuation multiples. It cannot isolate all changes in historical risk premiums or reconstruct the entire private capital market. Small and medium companies are analyzed as case studies, with both favorable and unfavorable evidence.')

title('Source register')
for i,k in enumerate(used,1):
 s=S[k];p(f'<b>[{i}] {html.escape(s["title"])}</b><br/><a href="{html.escape(s["url"],quote=True)}" color="#086788">{html.escape(s["url"])}</a>',small=True)
(O/'sources.json').write_text(json.dumps({k:S[k] for k in used},indent=2,ensure_ascii=False))

def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#b9c9d2'));canvas.line(47,40,548,40);canvas.setFont('DV',7);canvas.setFillColor(colors.HexColor('#526b7b'));canvas.drawString(47,28,'Civilization, infrastructure and markets | 12 October 2026');canvas.drawRightString(548,28,str(doc.page));canvas.restoreState()
doc=SimpleDocTemplate(str(O/'civilization_infrastructure_markets_2026.pdf'),pagesize=(595.28,841.89),rightMargin=47,leftMargin=47,topMargin=48,bottomMargin=53,title='What civilization is building and scaling',author='Codex; research discussion with Claude')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Built PDF with',len(used),'linked sources')
