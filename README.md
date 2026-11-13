# US Elections: The Midterm Effect

**Read the story site:** https://jwavalosq.github.io/us-elections-midterm-effect/

I built this project the day before an election, on November 2, 2026. The midterm election is on November 3, 2026. I wanted to answer a question I kept hearing: what do midterms actually do to a president, and what is really at stake this time?

## Read this first: no November 2026 results exist yet

This project was built on November 2, 2026. The midterm election is on November 3, 2026, the next day. No results exist yet, and I do not invent any. Chapter 04 covers what is at stake, forecasts from named sources with dates, and scenarios for each outcome. It also has a results section that is clearly labeled as pending, ready to fill in after November 3. No scenario in this project is presented as a prediction, and I take no partisan position.

## The question I started with

Every four years, Americans elect a president. Every two years, halfway through a president's term, they elect a new House of Representatives and about a third of the Senate. Those midterm elections almost always cost the president's party seats, and that loss changes what the president can actually do: fewer of their bills pass, their nominees wait longer, and the budget becomes a negotiation with the other party. In 2026 the starting point is unusually tight, so a small shift decides who controls each chamber. I wanted to measure how big that shift usually is, and what it changes in practice.

## Why it matters

Midterms decide whether a president governs with a friendly Congress or against a hostile one. That is not abstract. It decides whether judges get confirmed, whether vetoes fly, whether the government shuts down, and whether the last two years of a term are spent passing laws or fighting over them. If you have never studied American elections, you can still follow this project. I explain every concept in plain words, and every number traces to a named source.

## What I did

I built this in six notebooks, each one runnable on its own in Google Colab, and I executed all six end to end with zero cell errors.

1. **I mapped presidential history, 1976 to 2024.** Popular vote, Electoral College, turnout, and swing states, 13 elections.
2. **I mapped midterm history, 1978 to 2022.** Seat changes for the president's party in the House and the Senate, 12 midterms, plus who held a trifecta and who lost it.
3. **I measured what a midterm changes.** Vetoes, executive orders, judicial confirmations, and shutdowns, and I said plainly where the numbers stop proving cause.
4. **I laid out November 2026 before it happened.** The starting House and Senate, the governorships on the ballot, attributed forecasts with source and date, and neutral scenarios for each outcome.
5. **I built a watch list.** Chapter 05 is a checklist for reading the results when they land, and for updating the project honestly afterward.
6. **I kept the pre-election record clean.** The October 2026 forecasts stay untouched, so the project remains an honest record of what was known before the vote.

## What I found

**Presidential elections, 1976 to 2024.** The popular vote winner lost the presidency twice. In 2000, Al Gore won the popular vote by 519,208 votes but lost the Electoral College 271 to 266. In 2016, Hillary Clinton won the popular vote by 2,984,618 votes but lost the Electoral College 304 to 227. Turnout of eligible voters rose from 51.73 percent in 1996 to 65.28 percent in 2020, with 2024 provisionally estimated at 64.30 percent. The number of states decided by under 5 points bounced between 3 (1984) and 19 (1976), with 8 each in 2020 and 2024. There is no steady decline in competitiveness in this measure.

**Midterms, 1978 to 2022.** The president's party lost House seats in 10 of 12 midterms, by an average of 21.2 seats and a median of 14 seats. The exceptions were 1998 (Democrats gained 5) and 2002 (Republicans gained 8). In the Senate, the president's party gained seats in 3 midterms (1982, 2002, 2018), broke even in 2 (1998, 2022), and lost seats in 7, for an average loss of 3.25 seats. Six presidents entered a midterm holding a trifecta, and five of the six lost it. The exception was Jimmy Carter in 1978. The only midterm that created a trifecta was 2002.

**What a midterm changes.** Presidents veto more when Congress is controlled by the other party: Ronald Reagan vetoed 78 bills and George H. W. Bush 44, while George W. Bush and Barack Obama vetoed 12 each. Executive orders are the workaround presidents use when Congress will not act, but they can be reversed by the next president. Federal judges need Senate confirmation, so losing the Senate slows confirmations. There have been six major shutdowns since 1995, totaling 123 days, and two of them happened under a unified government, which shows shutdowns are not only a divided government phenomenon.

**November 2026, pre-election facts.** The House has 218 seated Republicans, 214 seated Democrats, 1 independent who caucuses with Republicans, and 2 vacant seats, for a working margin of 219 to 214. Democrats need a net gain of 4 seats to reach 218. Thirty five Senate seats are up, 22 held by Republicans and 13 by Democrats, and Democrats need a net gain of 4 for a majority. Thirty six governorships are up, 18 held by each party. The latest forecasts, all labeled with source and date in chapter 04, include Cook Political Report House ratings of October 30, 2026 (222 Democratic categories, 195 Republican categories, 18 toss-ups) and Cook Senate ratings of October 6, 2026 (47 Democratic aligned, 46 Republican, 7 toss-ups). Cook and Sabato ratings are paywalled at the source, so these numbers come from secondary reports of those ratings and are attributed that way, with dates, in the notebooks. They are never presented as directly observed Cook or Sabato pages.

## What it means, and who it helps

History says the president's party usually loses the House in a midterm, usually by a lot, and usually loses its trifecta with it. But history also says the pattern has exceptions, and 2026 starts so close that four seats decide the House. So the honest answer to "what will happen" is that I do not know, and neither does anyone else before the votes are counted. What I can give you is the size of the usual penalty, the exceptions, the levers a midterm actually moves, and a clean way to read the results against that history when they land. That is useful whether you are a voter, a student, a journalist, or a hiring manager checking whether I can tell a straight story from messy data.

## The notebooks

| Notebook | What it covers |
|---|---|
| 00_setup | Project structure, tools, every dataset source, verification checks |
| 01_presidential_history | Presidential elections 1976 to 2024: popular vote, Electoral College, turnout, swing states, wrong winners |
| 02_midterm_history | Midterms 1978 to 2022: seat changes, the penalty pattern and its exceptions, divided vs unified government |
| 03_the_midterm_effect | How midterms change laws, money, confirmations, and oversight, with honest limits |
| 04_november_2026 | What is at stake, attributed forecasts, scenarios, and a results section labeled as pending |
| 05_what_to_watch | Conclusions, how to read the results, and what to update after November 3 |

Charts live in `charts/` (19 charts). Processed tables live in `data/processed/`. The build scripts live in `scripts/`.

## How to run it yourself

You need Python 3.12 and the packages in `requirements.txt`. Each notebook starts with a pip install cell, so each one also runs on its own in Google Colab.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name us-elections --display-name "US Elections"
.venv/bin/python scripts/build_processed.py
.venv/bin/python scripts/build_notebooks.py
cd notebooks
../.venv/bin/python -m jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.kernel_name=us-elections *.ipynb
```

To rebuild from scratch, run `scripts/download_data.py` first. It fetches the raw MIT files and the House mirror. See `data/raw/PROVENANCE.md` for every source.

## What to watch, and what I will update after November 3

When the results land, read them against this history: did the president's party lose the usual number of seats, or beat the pattern? Did a trifecta survive, or fall, as it has in five of six cases? Did the forecast categories hold, or did the toss-ups break one way? My update checklist is: fill in official results, add a 2026 row to the midterm history table, recompute the averages, and keep the October 2026 forecasts untouched so the project stays an honest pre-election record.

## What the limits are, stated honestly

Every number traces to a source listed in chapter 00 and in `data/raw/PROVENANCE.md`. Where sources disagreed or a dataset had a known gap, I say so instead of smoothing it over. The details are in `BUILD_REPORT.md`, but here are the ones I most want you to know. The MIT House file download was blocked by a guestbook requirement, so I used a public mirror, verified against the official party division table. Mirror seat counts differ from the official table by 0 to 4 seats in most years, by 9 Republican seats in 1996, and by 4 seats in 2010. The 1996 gap is fully explained: the mirror holds only 20 of 30 Texas districts in 1996, because a court ordered redistricting moved 10 Texas races into a special process the mirror codes separately. So the midterm series uses the official division table, not the mirror. MIT national totals differ from published candidate totals by under 0.1 percent, because of write-in handling and certification vintages. I use MIT totals consistently. The 2020 turnout figure, 65.28 percent, is the Wikipedia table value used consistently, and the 2024 figure, 64.30 percent, is a provisional University of Florida estimate dated March 2, 2026, labeled as provisional. Governor toss-up counts are cut, because sources conflict (5 vs 3). Bills enacted per Congress was cut: no clean, verified per Congress table was secured, so chapter 03 uses vetoes, executive orders, confirmations, and shutdowns instead. No House seat map is included, because it would need district shapefiles and add little to the seat count story. District level 2026 race ratings are presented as aggregates only, because individual race ratings change frequently.

## Sources and honesty notes

Data: MIT Election Lab, official party division tables, FEC, Clerk of the House data via published tables, and attributed October 2026 forecast reports. See `BUILD_REPORT.md` for exactly what I used, what failed, what was approximated, and what was cut.
