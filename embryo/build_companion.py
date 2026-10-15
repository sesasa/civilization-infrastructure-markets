from pathlib import Path
import sys, json, html, csv, zipfile
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R.parent))
from report_sources import S

extra = {
 'staging': ('Human Developmental Biology Resource: morphological staging and age conventions', 'https://hdbratlas.org/protocols.html'),
 'cleavage': ('Virtual Human Embryo: Carnegie stage 2 specimen and cleavage description', 'https://virtualhumanembryo.lsuhsc.edu/demos/Stage2/Intro_pg/Intro.htm'),
 'gastrulation': ('Tyser et al. (2021): single-cell transcriptomic characterization of a gastrulating human embryo', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7615353/'),
 'placenta': ('Hempstock et al. (2004): endometrial glands as a source of nutrients, growth factors and cytokines during the first trimester', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC493283/'),
 'flow': ('Lucitti et al. (2007): vascular remodeling of the mouse yolk sac requires hemodynamic force', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4260474/'),
 'pattern': ('Warmflash et al. (2014): early embryonic spatial patterning in human embryonic stem-cell cultures', 'https://www.nature.com/articles/nmeth.3016'),
 'nerves': ('Mukouyama et al. (2002): sensory nerves determine arterial differentiation and branching in embryonic mouse skin', 'https://pubmed.ncbi.nlm.nih.gov/12086669/'),
 'atlas': ('de Bakker et al. (2016): interactive three-dimensional atlas of human development', 'https://pubmed.ncbi.nlm.nih.gov/27884980/'),
 'nerc': ('NERC (8 January 2025): incident review of simultaneous voltage-sensitive load reductions', 'https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_large_load_loss.pdf'),
 'ocp': ('Open Compute Project: solid-state transformer specification, revision 0.3.0, effective 22 June 2026', 'https://www.opencompute.org/documents/ocp-sst-design-specification-v0-3-final-pdf'),
 'emr': ('Emerson Q3 FY2026 earnings, quarter ended June 30, 2026', 'https://ir.emerson.com/news-events/press-releases/detail/642/emerson-reports-third-quarter-2026-results-raises-2026-outlook'),
 'rok': ('Rockwell Automation Q3 FY2026 earnings, quarter ended June 30, 2026', 'https://www.rockwellautomation.com/en-se/company/news/press-releases/Rockwell-Automation-Reports-Third-Quarter-2026-Results.html'),
 'iot': ('Samsara Q2 FY2027 earnings, quarter ended August 1, 2026', 'https://www.sec.gov/Archives/edgar/data/1642896/000162828026060438/samsaraepr-q22027.htm'),
 'xyl': ('Xylem Q2 2026 earnings, released July 28, 2026', 'https://www.xylem.com/en-us/about-xylem/newsroom/press-releases/xylem-reports-second-quarter-2026-results/'),
}
for key, (label, url) in extra.items(): S[key] = {'title': label, 'url': url}
for sym in ['emr', 'rok', 'iot', 'xyl', 'itri']:
 S['value_'+sym] = {'title': sym.upper()+' valuation snapshot, retrieved October 12, 2026; archived in accompanying data', 'url': f'https://stockanalysis.com/stocks/{sym}/statistics/'}

for name, file in [('DV','DejaVuSans.ttf'), ('DV-Bold','DejaVuSans-Bold.ttf'), ('DV-Italic','DejaVuSans-Oblique.ttf')]:
 pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-Bold', italic='DV-Italic', boldItalic='DV-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='B', fontName='DV', fontSize=9.1, leading=13.6, spaceAfter=9, textColor=colors.HexColor('#263d49')))
styles.add(ParagraphStyle(name='T', fontName='DV-Bold', fontSize=25, leading=30, spaceAfter=18, textColor=colors.HexColor('#14374a')))
styles.add(ParagraphStyle(name='L', fontName='DV-Bold', fontSize=15, leading=20, spaceAfter=14, textColor=colors.HexColor('#14374a')))
styles.add(ParagraphStyle(name='C', fontName='DV', fontSize=8, leading=11.2, textColor=colors.HexColor('#263d49')))
styles.add(ParagraphStyle(name='H', fontName='DV-Bold', fontSize=8, leading=11.2, textColor=colors.white))
styles.add(ParagraphStyle(name='S', fontName='DV', fontSize=7.5, leading=10.6, spaceAfter=7, textColor=colors.HexColor('#506571')))
story=[]; used=[]
def cite(*keys):
 out=[]
 for k in keys:
  if k not in used: used.append(k)
  out.append(f'<a href="{html.escape(S[k]["url"], quote=True)}" color="#087384">[{used.index(k)+1}]</a>')
 return ' '+', '.join(out) if out else ''
def p(text, *keys, small=False): story.append(Paragraph(text+cite(*keys), styles['S' if small else 'B']))
def lead(text, new=True):
 if new: story.append(PageBreak())
 story.append(Paragraph(text, styles['L']))
def table(head, rows, widths):
 data=[[Paragraph(html.escape(x), styles['H']) for x in head]]
 data += [[Paragraph(str(x), styles['C']) for x in row] for row in rows]
 t=Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#14374a')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#edf4f5'),colors.white])]))
 story.append(t);story.append(Spacer(1,10))

story.append(Paragraph('Civilization and<br/>embryonic development', styles['T']))
p('<b>What the comparison explains—and what it cannot predict</b><br/>Companion to the global infrastructure and market study<br/>12 October 2026 | Actual discussion with Claude: three additional rounds')
p('<b>Our joint conclusion:</b> the closest comparison for 2021–2026 is the overlapping work of <b>specialization, vascularization and functional integration</b>. Civilization is adding dense new functions—especially computation and electrified production—while enlarging and adapting the systems that supply, connect and regulate them.')
p('This is a recurring process within an already developed civilization. There is no defensible conversion from centuries to gestational weeks, no single global developmental clock, and no evidence here that humanity is becoming one organism.')
story.append(Image(str(R/'development_function_map.png'), width=500, height=500*5.6/11))
p('The next investment problem is therefore broader than adding capacity: turn installed equipment into dependable, useful services. Supply, signaling, control, maintenance and rules at interfaces must develop together. Existing earnings and deployment data support this direction; embryology does not independently validate it.')
p('The earlier 25-page study remains the cross-asset foundation, including oil, gold, equities, indices and property. This companion adds biological research, operating-interface evidence, and four company price histories with current valuation snapshots. The actual questions, disagreements and corrections with Claude are preserved separately.', small=True)

lead('Development scales organized function, not just size')
p('Your intuition is productive if “scaling energy capture” means acquiring and using more externally supplied chemical energy, and “scaling information” includes signaling, interpretation and coordinated action. An embryo acquires nutrients through changing maternal interfaces. It does not independently harvest primary energy as agriculture or a power station does. Maternal exchange and the embryo’s own circulation are distinct systems.')
table(['Approximate human sequence','What develops','Useful comparison'],[
 ['First days: cleavage','More, smaller cells; initial division does not produce proportionate bulk growth.','Replication, subdivision and rising organization can precede rising material throughput.'],
 ['Early weeks: implantation and nutritive interfaces','Access to maternal resources and exchange structures develops and changes.','New activity needs a dependable resource interface.'],
 ['Third week: gastrulation','Cell populations acquire different roles and spatial organization.','Specialization makes differentiated inputs, connections and coordination necessary.'],
 ['Overlapping weeks 3–8: organ formation, vessels and neural structures','Tissues and their delivery and signaling systems form together; early function influences further formation.','Factories and compute require power, cooling, networks and operating rules together.'],
 ['After eight post-conception weeks: fetal growth and continuing maturation','Growth and functional development continue; organs are not all finished or mature at this boundary.','Capability expands through integration, improvement and maintenance as well as new construction.'],
 ],[125,187,188])
p('These dates orient the biology only. HDBR stages samples by morphology and measurements; post-conception age differs from conventional obstetric gestational age by approximately two weeks. The sequence is overlapping, and stage boundaries do not supply an economic timetable.','staging','cleavage','gastrulation','atlas')
p('A human first-trimester tissue study documented uterine-gland contributions to nutrition and signaling during development of placental exchange. That supports the importance of changing supply interfaces. It does not mean that the embryo has no internal circulation until maternal blood exchange is established.','placenta')
p('<b>Information is active from the beginning.</b> Development depends on gene regulation, cell state, position, chemical and mechanical signals. A later-forming brain does not introduce coordination into an otherwise uncoordinated organism. Correspondingly, human cognition, language and social learning long precede industrial power and AI. “First energy, then information” is an inaccurate sequence for both comparisons.')

lead('The strongest mechanisms, and the history map')
p('<b>Function reshapes structure.</b> In mouse yolk-sac experiments, changing blood-flow mechanics altered vascular remodeling; restoring viscosity rescued aspects of remodeling. The lesson we borrow is to observe how a network works while it forms, then adapt it. This is evidence about mouse development, not direct evidence about an electricity market.','flow')
p('<b>Coordination need not wait for a central controller.</b> Human embryonic stem-cell cultures can form spatial patterns under controlled geometry and signaling conditions. These cultures model aspects of early patterning, not an entire human embryo. The engineering inference is that shared interfaces, local rules and feedback can coordinate many participants without a single master planner.','pattern')
p('<b>Delivery and signaling can be co-designed.</b> A mouse embryonic skin study found local relationships between sensory nerves and arterial differentiation and branching. This is a specific tissue mechanism, not a claim that all vessels follow nerves. It motivates looking at power, sensing and communication together.','nerves')
table(['Civilization change','Developmental parallel','Strength and boundary'],[
 ['Foraging societies','A starting embryo or zygote','Poor. Foragers already possess complex cognition, institutions and skills. There is no equivalent reset to one cell.'],
 ['Farming and dependable surpluses','A more dependable nutritive interface','Partial. Farming modifies ecosystems; embryos obtain resources from a mother.'],
 ['Cities, professions and institutions','Differentiation of roles and spatial organization','Partial. People choose and change roles; they are not cells assigned a fate.'],
 ['Industrial transport, water and electricity networks','Circulation and distribution to specialized tissues','Strongest functional analogy. Economics, ownership and multiple resource networks remain different.'],
 ['Telegraph, computing, internet and AI','Signaling and information processing','Partial. Human beings already provide cognition; AI augments and automates some functions.'],
 ['Recent compute and electrification buildout','New specialized tissue plus vascular expansion and integration','Useful process analogy. Multiple technologies and regions occupy different commercial phases.'],
 ],[140,160,200])
p('There is no one-to-one ladder from foraging to farming to industry to AI that reproduces embryogenesis. The useful unit of comparison is a recurring functional problem: specialization increases the need for delivery, coordination and adaptation.')

lead('What the last five years actually show')
p('The earlier market study covered roughly 11 October 2021 to 9 October 2026. Physical series end at their latest reported year or quarter. A five-year study does not turn end-2021 to end-2025 capacity data into five growth intervals; that comparison contains four.')
table(['Observed or estimated quantity','Pace','What it supports'],[
 ['World renewable nameplate capacity, end-2021 → end-2025','3,077 → 5,149 GW; +67%; 13.7% compound annual growth','Actual expansion of energy-conversion hardware, not generation output or firm capacity.'],
 ['Grid investment, 2026 IEA estimate','About $550bn; about +20% year on year','Spending is expanding in the delivery network. This remains an annual estimate.'],
 ['Primary North American data-center markets, H1 2026','10,903 MW; +33.7% year on year; 1.4% vacancy','Fast growth in the sampled property markets. Leased capacity does not establish GPU utilization or customer returns.'],
 ['US battery storage','43.6 GW at end-2025; about 52 GW by June 2026','Deployment of a flexibility resource. Power ratings do not measure energy duration.'],
 ['Powell, Q3 FY2026','Sales $312m, +9%; orders $934m; backlog $2.4bn, +69%','Electrical integration demand appears well below megacap scale; orders are not yet revenue.'],
 ['Hammond, Q2 2026','Sales C$325m, +44.7%; annual sales C$380m in 2021 → C$898m in 2025','Transformer production is expanding. Nominal company sales also reflect mix, prices and business changes.'],
 ],[190,150,160])
p('Primary evidence for the table. These quantities should not be added together: they mix installed stocks, spending flows, market samples and company results.','irena','iea','cbre','storage','powl','hps','hpshist',small=True)
p('<b>Closest developmental process:</b> dense new functions are being supplied and made operational. “Vascularization” captures the connection problem; “organogenesis” captures new specialized functions; “maturation” captures reliability and useful performance. They occur together. Calling this “week eight” or “the fetal brain-growth stage” would create precision unsupported by either the biology or the market data.')
p('The phase also differs by industry. Electrical equipment has strong orders; some solar manufacturing is commoditized; storage deployment and supplier profitability diverge; AI customer economics are still being established. An investment slowdown can interrupt energization even when the longer-term engineering need remains.')

lead('The regions are connecting complementary capabilities')
table(['Region','Concrete evidence from the earlier study','Interpretation; not a fixed “organ”'],[
 ['United States','Fast data-center construction, US storage about 52 GW by June 2026, electrical-equipment order growth.','Compute demand is meeting grid, delivery, cooling and operational constraints.'],
 ['Europe','EU renewable capacity 514.7 → 779.4 GW, end-2021 to end-2025; cable and electrification suppliers feature in the prior earnings study.','More generation requires connections, flexible demand and integration across networks.'],
 ['China','Renewables 1,017.9 → 2,258.0 GW over the same interval. State Grid reported over CNY310bn H1 2026 investment, +12.6%.','Large manufacturing and grid programs combine energy conversion, storage and delivery.'],
 ['India','Renewables 147.4 → 250.5 GW. L&T order book INR7.79trn, +27%; 52% international, of which 71% Middle East.','Domestic expansion and export of engineering/construction capacity connect Indian activity to Gulf investment.'],
 ['GCC','Renewables 3.8 → 23.9 GW, from a small base. ACWA reported commissioning 0.8 GWh of storage and 0.9 million cubic metres/day of water capacity in H1 2026.','Power, water, finance and construction develop together; hydrocarbons remain part of the system.'],
 ],[65,263,172])
p('Sources and definitions: renewable figures are operational nameplate capacity; company portfolio totals that include development are not substituted for commissioned capacity. L&T’s Middle East share is about 37% of its total order book (52% × 71%), not 71% of the entire book.','irena','sgcc','lt','acwa','storage')
p('What these regions are scaling together is the ability to convert resources into controllable, tradable services: electricity, computation, manufactured output, transport and water. Equipment supply, engineering, investment and demand cross borders, even as security policy duplicates parts of the system. This is an interpretation of complementary investments, not proof of a coordinated global project.')
p('Do not map China to a liver, America to a brain, or the Gulf to a placenta. All regions contain production, cognition, finance, consumption and political agency. Their roles change; people are ends in themselves, not components of a higher organism.')
p('An embryo inherits a largely shared genome and an evolved developmental program, with maternal support. Civilization has no equivalent common genome, parent organism or specified adult form. Competing human purposes, politics and invention make its trajectory open-ended. The analogy describes some coordination problems; it does not establish an organism, an inevitable destination or a biological imperative to grow.')
p('Market signals here are shaped by regulated utilities, state-owned companies, public investment, subsidies and security policies. They reveal commitments under existing institutions, not an experiment in unregulated allocation. Oil, gold and property prices also respond to rates, supply shocks, currencies and risk; they do not all measure one developmental transition.')

lead('New evidence: the interfaces can become the constraint')
p('NERC documented a July 2024 disturbance in which customer protection systems transferred approximately 1,500 MW of data-center load to backup power. The interaction with transmission-line reclosing was not anticipated. It caused no significant grid operating issues at that location and time, but exposed a mechanism whose risk can rise with concentrated loads. NERC recommends better dynamic models, monitoring, protection coordination and agreed reconnection behavior. This is evidence about control interactions, not an analysis of generation adequacy.','nerc')
p('The implication is that sufficient annual energy and sufficient installed generating capacity do not by themselves establish safe dynamic behavior. Grid equipment, UPS systems, cooling, power electronics and computing loads must respond compatibly to disturbances. A locally sensible protective action can create a large simultaneous change elsewhere.')
p('A concrete coordination artifact already exists: Google, Microsoft and Nvidia authored an Open Compute Project solid-state-transformer specification for medium-voltage conversion to 800 VDC, revision 0.3.0 effective June 2026. It includes ride-through and state-transition behavior. This documents interface work, not a measured commercial deployment share or a requirement that every facility adopt this voltage.','ocp')
p('Google also reported signing agreements for 1 GW of data-center demand response. Signed flexibility is not the same as a continuously delivered 1 GW resource; dispatch performance and workload constraints remain relevant. It nonetheless shows contracts beginning to connect computing operations with power-system needs.','google')
table(['What must work','Immediate engineering or institutional task','Evidence to ask for'],[
 ['Delivery','Complete substations, transformers, switchgear, connections and site distribution.','Energized MW and commissioning dates, not just announced MW.'],
 ['Disturbance handling','Test how customer and utility protection interact; agree load return rates.','Conformance results, incident frequency and recovery time.'],
 ['Thermal and water management','Match cooling and water arrangements to actual density and local constraints.','Reliability, water use and cooling energy per useful service.'],
 ['Flexible operation','Connect telemetry, workload scheduling, storage and contracts.','Verified dispatch, availability and net customer savings.'],
 ['Accountable action','Set identities, permissions, audit trails and human intervention for automation.','Measured task success, controlled failure and attributable decisions.'],
 ],[105,205,190])
p('This is the most useful addition to our earlier conclusion: connection alone is insufficient. Systems also need boundaries that contain failures, buffers, and tested ways of starting, stopping and reconnecting. The analogy prompted this search; finding an earlier incident afterward is consistency, not a successful advance prediction.')

lead('Do sensing, controls and water companies corroborate it?')
p('The answer is mixed—which matters. We added Emerson, Rockwell, Samsara and Xylem to the price and valuation study and revisited smaller Itron. These are exposures to parts of integration, not a pure basket of embryo-inspired investments.')
new={x['symbol']:x for x in json.loads((R/'supplemental_markets.json').read_text())}
oldp={x['symbol']:x for x in json.loads((R.parent/'output/market_prices.json').read_text()) if 'error' not in x}
oldv={x['symbol']:x for x in json.loads((R.parent/'output/valuations.json').read_text()) if 'error' not in x}
rows=[]
for sym,label in [('EMR','Emerson'),('ROK','Rockwell'),('IOT','Samsara*'),('XYL','Xylem'),('ITRI','Itron')]:
 x=new.get(sym,oldp.get(sym));v=new.get(sym,oldv.get(sym))
 rows.append([label, f"{x['price_change_pct']:+.1f}%", '$'+v['Market Cap'],v['Forward PE']+'×'])
table(['Company','Share-price change','Equity value','Forward P/E'],rows,[165,105,120,110])
p('Prices: 11 October 2021 to 9 October 2026; *Samsara starts at its 15 December 2021 IPO. USD, split-adjusted, excluding dividends. Valuation snapshots retrieved 12 October 2026 can have different quote timestamps; forward P/E uses vendor analyst estimates. Acquisitions, divestitures, rates and starting valuations affect comparisons. Individual source URLs and adjusted-return alternatives are in supplemental_markets.csv and the original dataset.','value_emr','value_rok','value_iot','value_xyl','value_itri',small=True)
table(['Operating evidence','What we can infer'],[
 ['Emerson Q3 FY2026: underlying sales +6%; Control Systems & Software +7% in the quarter, but +2% over nine months.','Demand is present; the longer period does not establish an exceptional sector-wide boom.'],
 ['Rockwell Q3 FY2026: total organic sales +10%; Software & Control +18% organic, with 34.8% segment operating margin.','A stronger pocket of controls demand. It spans many industrial applications and cannot be attributed entirely to AI.'],
 ['Samsara Q2 FY2027: revenue $508.4m, +30%; ARR $2.125bn, +30%; fourth consecutive GAAP-profitable quarter.','Strong monetization of sensing and workflows in physical operations, not proof of autonomous physical control.'],
 ['Xylem Q2 2026: organic orders +41%, organic sales +1%; full-year organic revenue guidance narrowed to 2–3%.','Orders exceed current delivery growth. Water infrastructure importance has not ensured a strong five-year share return.'],
 ['Itron Q2 2026: revenue $563m, −7%; ARR $417m, +21%; Outcomes revenue +13%.','Recurring integration-related activity can grow while total company revenue declines.'],
 ],[292,208])
p('Company earnings sources. Fiscal labels differ: these are mainly June quarters, while Samsara ended August 1.','emr','rok','iot','xyl','itron',small=True)
p('<b>Functional necessity and investor profit are separate questions.</b> Integration may come from configuration, embedded software, standards or governance rather than a new spending boom. Equally, rapid vendor sales do not prove customer productivity. Expensive valuations can already assume considerable success.')

lead('A conditional outlook for the next year and five years')
table(['Horizon and priority','Why the evidence points here','What would verify progress'],[
 ['Now–October 2027: energize usable capacity','Existing construction and electrical-equipment orders create pressure to complete connections, substations, distribution, cooling and installation.','Delivered and energized capacity; backlog conversion; lead times; cash collection.'],
 ['Now–October 2027: make interfaces behave predictably','Large-load events and published interface work make protection, ride-through, telemetry and reconnection practical priorities.','Interoperability tests, fewer avoidable incidents, faster recovery and verified flexibility.'],
 ['Now–October 2027: commission in stages and measure actual use','Uncertain customer returns and expensive capital favor checking service quality and utilization before scaling each project.','Cost per successful task/service, utilization and paying-customer retention.'],
 ['2027–2031: expand trunks and local delivery together','Generation, storage and compute require both major networks and usable connections at the point of demand.','Operating capacity and throughput, including bottleneck removal—not reservations alone.'],
 ['2027–2031: integrate sensing, decisions and physical work','Controls and operational-data companies provide some commercial evidence; wider adoption depends on customer economics.','Lower downtime, defects and operating cost with durable customer margins.'],
 ['2027–2031: improve maintenance, resource efficiency and recovery','More installed assets create a larger operating task. Modularity, repair, recycling and failure containment are plausible priorities.','Longer asset life and more useful output per unit of energy, water and capital.'],
 ],[145,190,165])
p('<b>Confidence:</b> high that delivery and operational integration are necessary to realize the announced buildout; moderate that they will attract broadly rising spending; lower on exact timing, vendor winners and a broad autonomous-operations wave. Projects can be delayed or cancelled, and capital spending can pause before integration matures.')
p('An external pace check comes from the IEA: data-center electricity use is projected to increase from roughly 485 TWh in 2025 to 950 TWh in 2030, about 14.4% annually. That is a forecast, not a biological growth rate or guaranteed demand. At roughly 3% of global electricity in 2030, it also cannot explain every grid investment.','ai')
p('The biological inspiration is to build capabilities that can operate while improving, with feedback from actual use. It does not justify waiting for demand before every trunk investment: networks require forward planning, validated scenarios and financing. Nor can it decide that compute deserves access ahead of households, hospitals or other public priorities.')

lead('What changed after the discussion with Claude')
table(['Earlier conclusion','Effect of this comparison'],[
 ['Energy and information infrastructure are complements.','Retained. Development offers a useful example of co-development, not independent economic proof.'],
 ['The buildout is in installation and integration, with different sector cycles.','Retained. Added a stronger distinction between installed capacity and stable, useful operation.'],
 ['Grid, cooling, storage, networks and institutions are necessary complements.','Retained. Sharpened attention to interfaces, local feedback, protection and failure containment.'],
 ['Controls and automation could gain importance.','Qualified. Their function can be essential without exceptional vendor revenue or stock returns.'],
 ['Physical progress and investment returns can diverge.','Retained. The Xylem/Itron evidence reinforces the need to track both separately.'],
 ['No reliable date for one civilizational phase transition.','Retained. No developmental week, inevitable global brain or single geopolitical body map.'],
 ],[245,255])
p('Across three actual rounds, Claude proposed a vascularization interpretation and several more literal extensions. I challenged age labels, the “information comes last” sequence, comparisons between adult-brain energy shares and data-center electricity, and biological arguments for a fixed gas-retirement date. Claude withdrew these. We also corrected the idea that a necessary control function must command scarce-resource profits.')
p('Claude’s final response accepted the resulting framework and reported no remaining claim-level disagreement. It retained uncertainty about adoption, costs, customer economics and whether integration spending will accelerate. Agreement here means agreement on the bounded interpretation and the unknowns; it is not evidence that two independently calibrated forecasting systems validated a prediction.')
p('<b>Prospective tests:</b> track functional outcomes—utilization, successful service cost, downtime, recovery and conformance—separately from commercial outcomes—orders, sales, margins, free cash flow and valuation. Compare otherwise similar projects with different integration practices where possible. Better outcomes can have several causes; a time trend alone will not establish that the proposed practice caused them.')
p('<b>What could weaken the forecast:</b> persistent low utilization; customer spending failing to cover full operating and capital cost; cancelled orders; easy integration that requires little incremental spending; or better technology that removes a presumed bottleneck. Widespread progress without the proposed interventions would weaken claims that those interventions were binding constraints.')
p('Civilization is building a larger range of capabilities that can work together. Energy acquisition and information processing are inputs; reliable, useful and accountable action is the outcome. Embryology helps us notice the difference between more components and a functioning system. It cannot tell us what society ought to value, guarantee growth, or choose investments for us.')

lead('Source register and research boundary')
p('All web sources were checked during this study or its immediately preceding market study. This register identifies biological research, original operating reports, company earnings, physical data and price/valuation providers separately by title. The report’s civilization mappings and forecasts are explicitly our inferences. Biological experiments are labeled human, mouse or culture-model evidence in the text.',small=True)
for i,k in enumerate(used,1):
 u=html.escape(S[k]['url'],quote=True)
 p(f'<b>[{i}] {html.escape(S[k]["title"])}</b><br/><a href="{u}" color="#087384">{html.escape(S[k]["url"])}</a>',small=True)
p('Files: civilization_embryo_comparison_2026.pdf; claude_embryo_discussion.txt; supplemental_markets.csv/json; development_function_map.png/svg; source_register.json. The source code and original prompt/response text are in the accompanying ZIP. The separate earlier report supplies the wider asset universe and raw historical data.',small=True)

def footer(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#b7cbd1'));canvas.line(48,39,548,39)
 canvas.setFont('DV',7);canvas.setFillColor(colors.HexColor('#506571'))
 canvas.drawString(48,26,'Civilization, development and infrastructure | 12 October 2026')
 canvas.drawRightString(548,26,str(doc.page))

pdf=R/'civilization_embryo_comparison_2026.pdf'
SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),leftMargin=48,rightMargin=47.28,topMargin=47,bottomMargin=53,title='Civilization and embryonic development',author='Codex; discussion with Claude').build(story,onFirstPage=footer,onLaterPages=footer)
(R/'source_register.json').write_text(json.dumps({k:S[k] for k in used},indent=2))
transcript=['ACTUAL CLAUDE DISCUSSION — CIVILIZATION AND EMBRYONIC DEVELOPMENT\n12 October 2026\n\nThree additional rounds continuing the prior market-study session.\nThis is the actual prompt/response text, not a reconstructed conversation. Earlier proposals contain claims later corrected or withdrawn; the final response and companion report state the accepted assessment. Agreement does not remove the uncertainties identified.\n']
for i in range(1,4):
 transcript.extend([f'\n\nROUND {i} — CODEX TO CLAUDE\n\n',(R/f'round{i}_prompt.txt').read_text(),f'\n\nROUND {i} — CLAUDE RESPONSE\n\n',(R/f'round{i}_response.txt').read_text()])
(R/'claude_embryo_discussion.txt').write_text(''.join(transcript))
with zipfile.ZipFile(R/'embryo_research_bundle.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['civilization_embryo_comparison_2026.pdf','claude_embryo_discussion.txt','supplemental_markets.csv','supplemental_markets.json','source_register.json','development_function_map.png','development_function_map.svg','build_companion.py','build_visual.py','fetch_supplement.py']:
  z.write(R/name,name)
 for i in range(1,4):
  for kind in ['prompt','response']:z.write(R/f'round{i}_{kind}.txt',f'discussion/round{i}_{kind}.txt')
 for sym in ['EMR','ROK','XYL','IOT']:
  z.write(R/f'{sym}_valuation.txt',f'raw/{sym}_valuation.txt')
  z.write(R.parent/'raw'/f'{sym}.json',f'raw/{sym}.json')
 z.write(R.parent/'report_sources.py','report_sources.py')
print(pdf)
print('Sources:',len(used))
