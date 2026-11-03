# US Elections: The Midterm Effect

A beginner friendly data story about how American elections work, what
midterm elections do to a president, and what the November 2026 midterms
could mean for the rest of the Trump administration, which ends on
January 20, 2029.

## Read this first: no November 2026 results exist yet

This project was built on November 2, 2026. The midterm election is on
November 3, 2026, the next day. No results exist yet, and this project
does not invent any. Chapter 04 covers what is at stake, forecasts from
named sources with dates, and scenarios for each outcome. It also has a
results section that is clearly labeled as pending, ready to fill in
after November 3. No scenario in this project is presented as a
prediction, and no partisan position is taken.

## The story in one paragraph

Every four years, Americans elect a president. Every two years, halfway
through a president's term, they elect a new House of Representatives and
about a third of the Senate. Those midterm elections almost always cost
the president's party seats, and that loss changes what the president can
actually do: fewer of their bills pass, their nominees wait longer, and
the budget becomes a negotiation with the other party. In 2026 the
starting point is unusually tight, so a small shift decides who controls
each chamber.

## What you will learn

- How the popular vote and the Electoral College can disagree, and why
  that happened in 2000 and 2016.
- What a swing state is, and how many states are actually close in each
  election.
- How often the president's party loses seats in a midterm, and by how
  much.
- What unified government and divided government mean, and why a trifecta
  rarely survives a midterm.
- How a midterm changes laws, money, confirmations, and oversight, and
  where the numbers stop proving cause.
- What is at stake in November 2026, what the October 2026 forecasts
  said, and how to read the results when they land.

## Key findings, with exact numbers

**Presidential elections, 1976 to 2024.** The popular vote winner lost
the presidency twice: in 2000, Al Gore won the popular vote by 519,208
votes but lost the Electoral College 271 to 266, and in 2016, Hillary
Clinton won the popular vote by 2,984,618 votes but lost the Electoral
College 304 to 227. Turnout of eligible voters rose from 51.73 percent in
1996 to 65.28 percent in 2020, with 2024 provisionally estimated at
64.30 percent. The number of states decided by under 5 points bounced
between 3 (1984) and 19 (1976), with 8 each in 2020 and 2024. There is no
steady decline in competitiveness in this measure.

**Midterms, 1978 to 2022.** The president's party lost House seats in 10
of 12 midterms, by an average of 21.2 seats and a median of 14 seats. The
exceptions were 1998 (Democrats gained 5) and 2002 (Republicans gained 8).
In the Senate, the president's party gained seats in 3 midterms (1982,
2002, 2018), broke even in 2 (1998, 2022), and lost seats in 7, for an
average loss of 3.25 seats. Six presidents entered a midterm holding a
trifecta, and five of the six lost it. The exception was Jimmy Carter in
1978. The only midterm that created a trifecta was 2002.

**What a midterm changes.** Presidents veto more when Congress is
controlled by the other party: Ronald Reagan vetoed 78 bills and George
H. W. Bush 44, while George W. Bush and Barack Obama vetoed 12 each.
Executive orders are the workaround presidents use when Congress will
not act, but they can be reversed by the next president. Federal judges
need Senate confirmation, so losing the Senate slows confirmations.
There have been six major shutdowns since 1995, totaling 123 days, and
two of them happened under a unified government, which shows shutdowns
are not only a divided government phenomenon.

**November 2026, pre election facts.** The House has 218 seated
Republicans, 214 seated Democrats, 1 independent who caucuses with
Republicans, and 2 vacant seats, for a working margin of 219 to 214.
Democrats need a net gain of 4 seats to reach 218. Thirty five Senate
seats are up, 22 held by Republicans and 13 by Democrats, and Democrats
need a net gain of 4 for a majority. Thirty six governorships are up, 18
held by each party. The latest forecasts, all labeled with source and
date in chapter 04, include Cook Political Report House ratings of
October 30, 2026 (222 Democratic categories, 195 Republican categories,
18 toss-ups) and Cook Senate ratings of October 6, 2026 (47 Democratic
aligned, 46 Republican, 7 toss-ups).

## How to run it

You need Python 3.12 and the packages in `requirements.txt`. Each notebook
starts with a pip install cell, so each one also runs on its own in
Google Colab.

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

To rebuild from scratch, run `scripts/download_data.py` first. It fetches
the raw MIT files and the House mirror. See `data/raw/PROVENANCE.md` for
every source.

## Notebooks

| Notebook | What it covers |
|---|---|
| 00_setup | Project structure, tools, every dataset source, verification checks |
| 01_presidential_history | Presidential elections 1976 to 2024: popular vote, Electoral College, turnout, swing states, wrong winners |
| 02_midterm_history | Midterms 1978 to 2022: seat changes, the penalty pattern and its exceptions, divided vs unified government |
| 03_the_midterm_effect | How midterms change laws, money, confirmations, and oversight, with honest limits |
| 04_november_2026 | What is at stake, attributed forecasts, scenarios, and a results section labeled as pending |
| 05_what_to_watch | Conclusions, how to read the results, and what to update after November 3 |

Charts live in `charts/` (19 charts). Processed tables live in
`data/processed/`. The build scripts live in `scripts/`.

## Sources and honesty notes

Every number traces to a source listed in chapter 00 and in
`data/raw/PROVENANCE.md`. Where sources disagreed or a dataset had a
known gap, the project says so instead of smoothing it over. See
`BUILD_REPORT.md` for exactly what was used, what failed, what was
approximated, and what was cut.
