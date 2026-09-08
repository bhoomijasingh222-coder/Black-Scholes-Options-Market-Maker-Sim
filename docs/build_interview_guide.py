from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / "Options_Market_Maker_Interview_Guide.pdf"

NAVY = colors.HexColor("#13233A")
BLUE = colors.HexColor("#2B6CB0")
TEAL = colors.HexColor("#168C8C")
PALE = colors.HexColor("#EDF5FA")
GOLD = colors.HexColor("#D79B2B")
INK = colors.HexColor("#243447")
MUTED = colors.HexColor("#607286")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=WHITE, alignment=TA_LEFT, spaceAfter=10))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["BodyText"], fontName="Helvetica", fontSize=11, leading=16, textColor=colors.HexColor("#D8E7F4")))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=19, leading=23, textColor=NAVY, spaceAfter=10, spaceBefore=3))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=BLUE, spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.4, leading=13.4, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=9.3, leading=13, textColor=NAVY, backColor=PALE, borderColor=colors.HexColor("#B9D8E8"), borderWidth=0.7, borderPadding=8, spaceBefore=5, spaceAfter=8))
styles.add(ParagraphStyle(name="Question", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=9.4, leading=13, textColor=TEAL, spaceBefore=6, spaceAfter=2))
styles.add(ParagraphStyle(name="Codex", parent=styles["Code"], fontName="Courier", fontSize=7.5, leading=10, textColor=INK, backColor=colors.HexColor("#F4F6F8"), borderPadding=6, spaceAfter=7))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8E1E8"))
    canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 9.5 * mm, "Options Pricing and Market-Making Simulator")
    canvas.drawRightString(192 * mm, 9.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(str(PDF), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="standard", frames=[frame], onPage=footer)])
story = []


def h1(text): story.append(Paragraph(text, styles["H1x"]))
def h2(text): story.append(Paragraph(text, styles["H2x"]))
def p(text, style="Bodyx"): story.append(Paragraph(text, styles[style]))
def bullets(items):
    for item in items:
        story.append(Paragraph(f"- {item}", styles["Bodyx"]))
def page(): story.append(PageBreak())
def callout(text): story.append(Paragraph(text, styles["Callout"]))


# Cover
cover = Table([[Paragraph("OPTIONS PRICING AND<br/>MARKET-MAKING SIMULATOR", styles["CoverTitle"])],
               [Paragraph("A child-simple, interview-deep guide to the maths, code, experiments and honest limitations", styles["CoverSub"])],
               [Spacer(1, 58 * mm)],
               [Paragraph("Python  |  NumPy  |  pandas  |  Black-Scholes  |  Greeks  |  Monte Carlo", styles["CoverSub"])]],
              colWidths=[174 * mm], rowHeights=[38 * mm, 24 * mm, 68 * mm, 18 * mm])
cover.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY), ("BOX", (0,0), (-1,-1), 0, NAVY), ("LEFTPADDING", (0,0), (-1,-1), 13 * mm), ("RIGHTPADDING", (0,0), (-1,-1), 13 * mm), ("TOPPADDING", (0,0), (-1,0), 15 * mm), ("VALIGN", (0,0), (-1,-1), "TOP")]))
story += [Spacer(1, 15 * mm), cover, Spacer(1, 8 * mm)]
p("Built as an educational research simulator. It is not a live trading system and it does not claim real-market profitability.", "Smallx")
page()

h1("1. The whole project in one minute")
p("Imagine a shop selling umbrellas. The shopkeeper must choose two prices: a lower price at which the shop will buy an umbrella, and a higher price at which it will sell one. Options market making is similar, except the object is a financial contract whose value keeps changing.")
callout("One-sentence description: I built a seeded simulator that values a European option with Black-Scholes, changes two-sided quotes according to volatility, inventory and adverse-selection risk, delta-hedges the resulting position, and compares P&L and drawdown across market regimes.")
h2("The loop")
flow = [["1. Move stock", "2. Price option", "3. Set bid / ask"], ["6. Measure P&L", "5. Delta hedge", "4. Simulate trade"]]
t = Table(flow, colWidths=[55 * mm] * 3, rowHeights=[18 * mm] * 2)
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), PALE), ("GRID", (0,0), (-1,-1), 0.7, colors.HexColor("#A8C8DA")), ("TEXTCOLOR", (0,0), (-1,-1), NAVY), ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 9), ("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0,0), (-1,-1), "MIDDLE")]))
story += [t, Spacer(1, 7 * mm)]
h2("What each tool does")
data = [["Tool", "Plain-English job"], ["Python", "Controls the experiment and joins all pieces together."], ["NumPy", "Generates seeded random stock moves and performs numerical work."], ["pandas", "Stores every step in tables and aggregates results."], ["Matplotlib", "Turns P&L and inventory into a chart."], ["unittest", "Checks important facts automatically."]]
t = Table(data, colWidths=[37 * mm, 128 * mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), WHITE), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#CCD7E0")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 8.5), ("LEADING", (0,0), (-1,-1), 11), ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, colors.HexColor("#F7F9FA")]), ("PADDING", (0,0), (-1,-1), 6)]))
story.append(t)
page()

h1("2. What is an option?")
p("A call option is a ticket that gives its owner the right, but not the obligation, to buy a stock at a fixed price before or at a fixed date. This project uses a European call, so it can be exercised only at expiry.")
h2("The five basic words")
bullets(["<b>Spot (S):</b> the stock price now.", "<b>Strike (K):</b> the fixed purchase price written on the ticket.", "<b>Expiry (T):</b> how much time remains.", "<b>Volatility (sigma):</b> how violently the stock tends to move.", "<b>Risk-free rate (r):</b> the interest rate used to compare money now with money later."])
h2("Tiny example")
p("Suppose the strike is $100. At expiry, if the stock is $112, the call is worth $12 because it lets you buy at $100 and the market value is $112. If the stock is $94, you ignore the ticket and its payoff is $0. The payoff is therefore max(S - K, 0).")
callout("Important distinction: payoff is the value at expiry. Price is what the option is worth before expiry, when there is still uncertainty and time remaining.")
h2("Why the option can be valuable before expiry")
p("Even if the stock is below $100 today, it could rise above $100 later. More time and more uncertainty usually increase the chance of a valuable outcome. Black-Scholes turns that idea into a formula under strict assumptions.")
page()

h1("3. Black-Scholes without fear")
p("The project implements the formula directly rather than calling a ready-made pricing function. For a European call with no dividends:")
formula = [[Paragraph("C = S N(d1) - K e<super>-rT</super> N(d2)", styles["Callout"])], [Paragraph("d1 = [ln(S/K) + (r + sigma<super>2</super>/2)T] / [sigma sqrt(T)]", styles["Bodyx"])], [Paragraph("d2 = d1 - sigma sqrt(T)", styles["Bodyx"])]]
t = Table(formula, colWidths=[165 * mm])
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F7FAFC")), ("BOX", (0,0), (-1,-1), 0.7, colors.HexColor("#C6D5DF")), ("PADDING", (0,0), (-1,-1), 8)]))
story += [t, Spacer(1, 4 * mm)]
p("N(d) means the normal cumulative distribution: roughly, it translates a standardised score into a probability-like weight. The first term values receiving the stock; the second values paying the discounted strike.")
h2("Assumptions you must say out loud")
bullets(["The stock follows geometric Brownian motion, so log returns are normally distributed.", "Volatility and the risk-free rate stay constant inside a regime.", "There are no dividends in this version.", "The option is European.", "The textbook model assumes frictionless trading; this simulator separately adds simplified transaction costs."])
h2("Tests that defend the implementation")
bullets(["A standard S=100, K=100, T=1, r=5%, sigma=20% call returns about $10.4506.", "Put-call parity is checked to ten decimal places.", "At expiry, the code returns the exact intrinsic payoff.", "Invalid negative or zero inputs are rejected where appropriate."])
callout("Interview line: Black-Scholes is my model fair value, not a statement that the real market must trade there.")
page()

h1("4. Greeks: the option's sensitivity dials")
data = [["Greek", "Child-simple meaning", "Risk question"], ["Delta", "How much option value changes for a $1 stock move.", "How many shares roughly hedge the option?"], ["Gamma", "How quickly delta itself changes.", "How unstable is my hedge?"], ["Vega", "How much value changes when volatility changes by 1.00.", "Am I exposed to volatility?"], ["Theta", "How much value changes as a year of time passes, all else equal.", "How much time value is decaying?"], ["Rho", "How much value changes when the rate changes by 1.00.", "How sensitive am I to interest rates?"]]
t = Table(data, colWidths=[20 * mm, 75 * mm, 70 * mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), WHITE), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("GRID", (0,0), (-1,-1), 0.45, colors.HexColor("#CAD5DE")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 8), ("LEADING", (0,0), (-1,-1), 10.5), ("PADDING", (0,0), (-1,-1), 5)]))
story.append(t)
h2("Delta hedge example")
p("One call contract controls 100 shares. If the market maker is long 3 calls and each call has delta 0.60, the option position behaves roughly like +180 shares: 3 x 0.60 x 100. The simulator targets -180 shares to reduce small stock-move risk.")
callout("Delta hedging removes only first-order spot exposure at that instant. Delta changes when spot and time change, so the hedge must be rebalanced. Gamma, volatility jumps, discrete hedging and costs leave residual risk.")
h2("Unit trap")
p("The code reports vega and rho per full 1.00 change, not per one percentage point. To interpret a 1 percentage-point volatility rise, divide vega by 100. Theta is per year, so a one-day approximation is theta / 365 or theta / 252 depending on the time convention being discussed.")
page()

h1("5. What a market maker actually does")
p("A market maker continuously shows a bid and an ask. If a customer sells, the maker buys at the bid. If a customer buys, the maker sells at the ask. The spread is compensation for providing immediacy and taking risk; it is not guaranteed profit.")
h2("Quote construction in this project")
p("First, Black-Scholes gives a fair value. Then the program shifts that value to create a reservation price:")
callout("reservation price = fair value - inventory_skew x option inventory")
p("If inventory is positive, the maker owns too many options. Lowering both quotes makes buying more less attractive and selling to customers more attractive. If inventory is negative, the reverse happens.")
p("Next, it builds a risk-sensitive half-spread:")
callout("half-spread = base spread + value scale x (volatility factor x volatility + adverse factor x adverse risk)")
p("Finally: bid = reservation price - half-spread, and ask = reservation price + half-spread. The bid is floored at zero and the ask stays at least one cent above the bid.")
h2("Inventory limits")
p("The default hard limit is 20 contracts. At the positive limit the maker refuses to bid, so it cannot buy more. At the negative limit it refuses to offer, so it cannot sell more. The tests verify that simulated inventory never breaks the limit.")
page()

h1("6. Volatility, inventory and adverse selection")
h2("Volatility risk")
p("When the underlying moves faster, option value and delta can change faster. The quote therefore widens with volatility. A wider spread demands more compensation, but it also makes customers less likely to trade.")
h2("Inventory risk")
p("An unbalanced option position carries delta, gamma, vega and time risk. The quote is skewed against the inventory, and the stock hedge reduces delta. These are different controls: skew tries to change future order flow, while hedging changes today's portfolio exposure.")
h2("Adverse selection")
p("Adverse selection means the customer may know more than the market maker. A simple example: a customer buys just before the fair value rises. The maker sold at an old, too-low price. In the simulation, higher adverse risk makes buy flow more likely before an upward stock move and sell flow more likely before a downward move.")
callout("This uses the next simulated stock move only to generate toxic customer behaviour. The market maker's quote never sees that future move. If the quoting rule used it, that would be look-ahead bias.")
h2("Why the model widens in an adverse regime")
p("The maker cannot identify each informed trader. Instead it charges more compensation on average by widening the spread. That lowers fills and may protect P&L, but it can also sacrifice business. This trade-off is central to market making.")
page()

h1("7. How the artificial market is generated")
p("The stock follows geometric Brownian motion:")
callout("S(next) = S(now) x exp[(mu - sigma^2/2)dt + sigma sqrt(dt) Z], where Z is a standard normal random draw.")
p("The exponential keeps the stock positive. The drift mu controls average direction, sigma controls movement size, dt is a small time step, and Z supplies randomness. A fixed seed makes the same Z values appear again, so results can be reproduced.")
h2("Three regimes")
data = [["Regime", "Volatility", "Adverse risk", "Arrival chance / step"], ["Calm", "14%", "0.10", "0.20"], ["Volatile", "38%", "0.35", "0.28"], ["Adverse", "28%", "0.85", "0.30"]]
t = Table(data, colWidths=[38 * mm, 38 * mm, 42 * mm, 47 * mm])
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), WHITE), ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#C9D5DE")), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("ALIGN", (1,1), (-1,-1), "CENTER"), ("FONTSIZE", (0,0), (-1,-1), 8.5), ("PADDING", (0,0), (-1,-1), 6)]))
story.append(t)
h2("Fill probability")
p("A customer is less likely to accept a quote far from fair value. The simulator applies an exponential decay: base arrival probability x exp(-sensitivity x quote distance). This is a deliberately simple reduced-form order-flow model, not an estimated model from exchange data.")
h2("Time convention")
p("A run contains 500 steps over 20 trading days, while the option begins with 30/252 years to expiry. The simulated period therefore ends before contractual expiry. Remaining positions are liquidated at the final model value so every run ends flat and can be compared consistently.")
page()

h1("8. Cash, hedging and P&L bookkeeping")
h2("When the maker buys an option")
p("Trade size is +1. Inventory rises by one. Cash falls by bid x 100 plus the option fee.")
h2("When the maker sells an option")
p("Trade size is -1. Inventory falls by one. Cash rises by ask x 100 minus the option fee.")
h2("When the hedge changes")
p("The target shares equal -option inventory x delta x 100. Buying stock reduces cash; selling stock increases cash. Either direction pays a proportional hedge transaction cost.")
h2("Mark-to-market P&L")
callout("P&L = cash + option inventory x fair option value x 100 + hedge shares x stock price")
p("This asks: if we value every open item now, what is the whole portfolio worth? It separates economic performance from cash alone. Cash can look very negative after buying assets even though the assets still have value.")
h2("Maximum drawdown")
p("At each step, remember the best P&L seen so far. Drawdown is that best value minus current P&L. Maximum drawdown is the worst of those falls. It measures the nastiest peak-to-trough pain inside the run, not the worst single trade.")
h2("Why costs matter")
p("Frequent delta rebalancing can reduce risk but increase costs. This is one reason real hedging is an optimisation problem rather than a command to become perfectly delta-neutral after every tiny move.")
page()

h1("9. What the experiment found")
summary = pd.read_csv(ROOT / "outputs" / "regime_summary.csv")
summary = summary[["regime", "mean_pnl", "pnl_std", "mean_max_drawdown", "mean_trades", "mean_costs", "worst_inventory"]]
rows = [["Regime", "Mean P&L", "P&L SD", "Mean MDD", "Trades", "Costs", "Worst inv."]]
for _, r in summary.iterrows():
    rows.append([r.regime.title(), f"${r.mean_pnl:,.0f}", f"${r.pnl_std:,.0f}", f"${r.mean_max_drawdown:,.1f}", f"{r.mean_trades:.1f}", f"${r.mean_costs:,.1f}", f"{int(r.worst_inventory)}"])
t = Table(rows, colWidths=[27*mm, 28*mm, 25*mm, 26*mm, 19*mm, 22*mm, 20*mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), WHITE), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("ALIGN", (1,1), (-1,-1), "RIGHT"), ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#C9D5DE")), ("FONTSIZE", (0,0), (-1,-1), 7.8), ("PADDING", (0,0), (-1,-1), 5)]))
story += [t, Spacer(1, 5 * mm)]
p("These are averages across 50 seeded runs per regime. In this particular synthetic calibration, all three average P&Ls were positive. Calm markets produced the most trades. The adverse regime produced the highest average P&L because its wider spreads and calibrated flow more than offset simplified toxic-flow losses. That is a property of this toy calibration, not evidence that adverse selection is profitable in reality.")
img = ROOT / "outputs" / "performance.png"
if img.exists():
    story.append(Image(str(img), width=160 * mm, height=112 * mm))
p("The chart shows one representative seeded path per regime, not the 50-run average. Never use one attractive path as proof of robustness.", "Smallx")
page()

h1("10. How to interpret results honestly")
h2("What you may claim")
bullets(["The code produced deterministic results for any fixed seed.", "The Black-Scholes implementation passed a known-value test and put-call parity.", "Inventory remained inside the hard limit in tested runs.", "The experiment compared P&L, costs, drawdown, trades and inventory across explicit synthetic regimes.", "Quote width and skew responded mechanically to the named risks."])
h2("What you must not claim")
bullets(["Do not say the strategy is profitable in real markets.", "Do not call synthetic order flow historical backtesting.", "Do not claim the chosen parameters were fitted to exchange data.", "Do not call the Sharpe-like diagnostic a real annualised Sharpe ratio.", "Do not say delta hedging removes all risk."])
h2("Why the P&L is large")
p("The simulator quotes one contract at a time with a 100-share multiplier, uses stylised customer arrivals, and allows spread capture without exchange queue competition. The model fair value is also the maker's value. These choices make the experiment useful for mechanism learning, but they can make profits look cleaner and larger than a realistic market would permit.")
callout("Strong interview behaviour: volunteer the limitation before the interviewer has to catch it. That shows research maturity, not weakness.")
page()

h1("11. Code map: know where everything lives")
data = [["File", "Responsibility"], ["black_scholes.py", "Normal CDF/PDF, option price, delta, gamma, vega, theta and rho."], ["market_maker.py", "Quote object, dynamic spread, inventory skew and hard limits."], ["simulation.py", "Regimes, GBM stock path, customer flow, trades, hedging and accounting."], ["metrics.py", "Maximum drawdown and summary performance statistics."], ["cli.py", "Runs 50 seeds per regime, exports CSVs and creates the chart."], ["run.py", "Simple entry point so the project runs without installation."], ["tests/", "Known price, parity, expiry payoff, reproducibility, inventory and metric checks."], ["outputs/", "Step data, run summaries, regime summary and performance chart."]]
t = Table(data, colWidths=[43 * mm, 122 * mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), WHITE), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#CAD5DE")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 8.2), ("LEADING", (0,0), (-1,-1), 11), ("PADDING", (0,0), (-1,-1), 5)]))
story.append(t)
h2("Commands")
p("Run experiment:<br/><font name='Courier'>python run.py --runs 50 --output outputs</font>", "Codex")
p("Run tests:<br/><font name='Courier'>PYTHONPATH=src python -m unittest discover -s tests -v</font>", "Codex")
h2("Why separate modules?")
p("Pricing, quoting, simulation and evaluation answer different questions. Separation makes each piece easier to test, explain and replace. For example, a future version could replace Black-Scholes with another volatility model without rewriting drawdown calculation.")
page()

h1("12. Interview questions and strong answers")
qas = [
    ("Why did you build this?", "I wanted to connect option theory with the actual decisions a market maker faces. Pricing alone gives a fair value, but quoting adds inventory, fill probability, adverse selection, hedging costs and risk limits."),
    ("Why Black-Scholes?", "It gives a transparent baseline and analytical Greeks. Its assumptions are restrictive, which is useful because I can clearly identify what the simulation includes and what a more realistic version should relax."),
    ("How does inventory skew work?", "I subtract a multiple of inventory from fair value. If I am long, both quotes move lower, discouraging further purchases and encouraging sales. If short, both move higher."),
    ("Why widen spreads in high volatility?", "Fair value and delta can move more quickly, so stale-quote and hedging risk rise. A wider spread demands more compensation, although it reduces fill probability."),
    ("What is adverse selection here?", "The customer's direction is tilted toward the next stock move, while my quoting rule cannot see that move. It models customers being more likely to trade when the quote is about to become unfavourable to me."),
    ("How did you validate it?", "I used a known Black-Scholes benchmark, put-call parity, expiry payoff checks, deterministic seed equality, inventory-limit checks, quote-skew checks and non-negative risk/cost checks."),
    ("Why 50 seeds?", "One random path can flatter or punish the strategy by chance. Multiple seeds provide a distribution and allow mean performance and variability to be compared."),
    ("What would you improve first?", "I would calibrate order arrivals and price impact to real quote/trade data, model an implied-volatility surface, add jumps and stochastic volatility, and optimise hedging frequency rather than hedge every step."),
]
for q, a in qas:
    story.append(KeepTogether([Paragraph(q, styles["Question"]), Paragraph(a, styles["Bodyx"])]))
page()

h1("13. Harder follow-ups")
hard = [
    ("Why geometric Brownian motion?", "It keeps prices positive and is consistent with the Black-Scholes baseline. But it misses jumps, volatility clustering, skew and fat tails."),
    ("Is your customer-flow model structural?", "No. It is reduced-form: arrival chance decays exponentially with quote distance and is tilted by future direction in toxic regimes. It is chosen for interpretability, not estimated from limit-order-book data."),
    ("Does the market maker know the true volatility?", "Yes, in this baseline the simulator and pricer use the same regime volatility. That removes estimation error. A stronger extension would price with estimated volatility while the true path follows a different process."),
    ("Why liquidate at model fair value?", "It makes terminal comparisons flat and prevents hidden open risk. It is optimistic because real liquidation crosses a spread and may have impact; I would add a liquidation penalty in a production study."),
    ("Why is maximum drawdown small relative to final P&L?", "The stylised spread-capture mechanism and frequent mark-to-model valuation make P&L unusually smooth. That is a warning that the simulated microstructure is generous, not evidence of exceptional risk-adjusted performance."),
    ("What is the difference between risk-neutral pricing and real drift?", "Black-Scholes discounts expected payoff under a risk-neutral measure using r. The stock simulation can have a real-world drift mu. I set mu to zero to focus the experiment on quoting and risk rather than directional forecasting."),
    ("Can delta hedging lock in the spread?", "No. Discrete rehedging, gamma, volatility changes, transaction costs, jumps and model error mean realised P&L can differ from quoted spread."),
]
for q, a in hard:
    story.append(KeepTogether([Paragraph(q, styles["Question"]), Paragraph(a, styles["Bodyx"])]))
page()

h1("14. A confident explanation you can practise")
h2("30-second version")
callout("I built a Python simulator linking Black-Scholes option pricing to market-making decisions. At each seeded time step it simulates the stock, recalculates the option price and Greeks, sets a bid and ask that widen with risk and skew against inventory, simulates customer flow, delta-hedges in the stock, and records marked-to-market P&L, costs and drawdown. I then compare 50 runs across calm, volatile and adverse-selection regimes. The main value is understanding the mechanisms; it is deliberately not presented as a live profitable strategy.")
h2("Two-minute structure")
bullets(["<b>Motivation:</b> move beyond calculating an option price to managing a quoted portfolio.", "<b>Pricing:</b> implement Black-Scholes and analytical Greeks from the formulas.", "<b>Quoting:</b> fair value becomes a reservation price, then a risk-dependent spread creates bid and ask.", "<b>Execution:</b> customer acceptance falls with quote distance; adverse flow is tilted toward the next move.", "<b>Risk:</b> inventory limits stop runaway exposure and a stock hedge offsets current delta.", "<b>Evaluation:</b> 50 seeds per regime, with P&L, variability, drawdown, costs, trades and inventory.", "<b>Judgement:</b> explain why synthetic profits are not market evidence and name the next realism upgrades."])
h2("If you freeze")
p("Return to the six verbs: <b>simulate, price, quote, trade, hedge, measure.</b> That is the entire project. Explain one verb at a time.")
page()

h1("15. Revision card")
data = [["Remember", "Answer"], ["Call payoff", "max(S - K, 0)"], ["Bid", "Price where the maker buys"], ["Ask", "Price where the maker sells"], ["Inventory skew", "Move both quotes against current inventory"], ["Delta hedge", "Target shares = -contracts x delta x 100"], ["P&L", "Cash + marked option value + marked stock hedge"], ["Drawdown", "Fall from previous P&L peak"], ["Adverse selection", "Customer tends to trade before the quote worsens for maker"], ["Seed", "Makes randomness reproducible"], ["Best limitation", "Synthetic uncalibrated microstructure, not a live backtest"], ["Six verbs", "Simulate, price, quote, trade, hedge, measure"]]
t = Table(data, colWidths=[48 * mm, 117 * mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), WHITE), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("GRID", (0,0), (-1,-1), 0.45, colors.HexColor("#C9D5DE")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 8.5), ("PADDING", (0,0), (-1,-1), 6), ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, colors.HexColor("#F7F9FA")])]))
story.append(t)
h2("Final checklist before an interview")
bullets(["Run the tests and know what each one proves.", "Open regime_summary.csv and remember the results are averages over 50 seeds.", "Explain why the adverse result does not establish real profitability.", "Practise the 30-second answer aloud until it sounds like your natural speech.", "Be able to draw the six-step loop on paper.", "Name at least three extensions: data calibration, volatility surface, stochastic volatility/jumps, queue position, price impact, and optimal hedging frequency."])
callout("Deep understanding is not memorising every line of code. It is knowing what question each component answers, what assumption makes it possible, and what could make its conclusion wrong.")

doc.build(story)
print(PDF)
