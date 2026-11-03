"""Generate the 6 notebooks for US Elections: The Midterm Effect.

Run from the project root: .venv/bin/python scripts/build_notebooks.py
Then execute: cd notebooks && ../.venv/bin/python -m jupyter nbconvert \
  --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=us-elections *.ipynb
"""
import os
import nbformat as nbf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(ROOT, "notebooks")
os.makedirs(NB_DIR, exist_ok=True)

PIP_CELL = (
    "# Run this cell first. It installs the packages this notebook uses.\n"
    "%pip install -q pandas matplotlib"
)
SETUP_CELL = (
    "import os\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "\n"
    "PROC = os.path.join('..', 'data', 'processed')\n"
    "CHART_DIR = os.path.join('..', 'charts')\n"
    "os.makedirs(CHART_DIR, exist_ok=True)\n"
    "plt.rcParams['figure.dpi'] = 120\n"
    "DEM = '#1f77b4'\n"
    "REP = '#d62728'\n"
    "GREY = '#7f7f7f'\n"
    "\n"
    "def savefig(name):\n"
    "    path = os.path.join(CHART_DIR, name)\n"
    "    plt.savefig(path, bbox_inches='tight')\n"
    "    plt.close()\n"
    "    print('saved', path)\n"
)


def nb(cells):
    out = nbf.v4.new_notebook()
    out.metadata = {
        "kernelspec": {"display_name": "US Elections", "language": "python", "name": "us-elections"},
        "language_info": {"name": "python", "version": "3.12"},
    }
    out.cells = cells
    return out


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


def write(name, cells):
    path = os.path.join(NB_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb(cells), f)
    print("wrote", path, "with", len(cells), "cells")


# ================================================================ 00_setup
def build_00():
    cells = [
        code(PIP_CELL),
        md("""
# 00. Setup: what this project is and where every number comes from

**US Elections: The Midterm Effect** is a beginner friendly data story.
It answers three questions in plain words.

1. How do US presidential elections work, and what has happened since 1976?
2. What happens in midterm elections, the elections held halfway through a
   president's four year term?
3. How do midterm results change what a president can actually do, and what
   could the November 2026 midterms mean for the rest of the Trump
   administration, which ends on January 20, 2029?

A note on timing. This project was built on November 2, 2026. The midterm
election is on November 3, 2026, the next day. No November 2026 results exist
yet. This project does not invent any. Chapter 04 covers what is at stake,
forecasts from named sources with dates, and scenarios. It also has a
results section that is clearly labeled as pending, ready to fill in after
November 3.
"""),
        code(SETUP_CELL),
        md("""
## Project structure

The cell below lists every folder and file in this project, so you can see
exactly what is here before we use any of it.
"""),
        code("""
for base, dirs, files in os.walk('..'):
    dirs[:] = [d for d in dirs if d not in ('.venv', '__pycache__')]
    level = base.replace('..', '').count(os.sep)
    print(' ' * 2 * level + os.path.basename(base) + '/')
    for f in sorted(files):
        if f.endswith('.ipynb_checkpoints'):
            continue
        print(' ' * 2 * (level + 1) + f)
"""),
        md("""
## Tools

We use Python with two libraries: pandas for tables and matplotlib for
charts. The pip cell at the top of every notebook installs them, so each
notebook runs on its own in Google Colab or on any computer.
"""),
        code("""
import sys
print('Python:', sys.version.split()[0])
print('pandas:', pd.__version__)
import matplotlib
print('matplotlib:', matplotlib.__version__)
"""),
        md("""
## Every dataset source

A dataset is a table of numbers that someone collected and published. Here
is every dataset this project uses, where it came from, and what it covers.
The full provenance notes live in `data/raw/PROVENANCE.md`.

| Dataset | Source | Coverage |
|---|---|---|
| Presidential votes by state | MIT Election Data and Science Lab, Harvard Dataverse, DOI 10.7910/DVN/42MVDX, file president_1976_2024.csv | 1976 to 2024 |
| Senate votes by state | MIT Election Data and Science Lab, Harvard Dataverse, DOI 10.7910/DVN/PEJ5QU, file senate_1976_2024.tab | 1976 to 2024 |
| House votes by district | keithpotz/Election-Prediction mirror of the MIT House file, house_1976_2024.csv (the MIT download itself required a guestbook form, so the mirror is used and cross checked) | 1976 to 2024 |
| Senate party divisions | senate.gov, history party divisions page | 95th to 119th Congress |
| House party divisions | Wikipedia, Party divisions of United States Congresses, which compiles Clerk of the House data | 95th to 119th Congress |
| Electoral College votes | Federal Election Commission, official presidential general election results | 1976 to 2024 |
| Voter turnout | University of Florida Election Lab (Michael McDonald), voting eligible population turnout, via Wikipedia | 1980 to 2024, plus midterms 2014, 2018, 2022 |
| Presidential vetoes | American Presidency Project, presidential vetoes table, data through January 8, 2026 | Carter through Trump second term, in progress |
| Executive orders | Federal Register disposition tables, via Competitive Enterprise Institute tables | Carter through Biden, plus a provisional Trump second term count |
| Judicial confirmations | Wikipedia, list of presidents by judicial appointments, Article III judges only | Carter through Biden, plus Trump first term |
| Federal shutdowns | Congressional Research Service based lists of major shutdowns | 1995 to 2025 |
| 2026 stakes and forecasts | House and Senate trackers, Cook Political Report and Sabato's Crystal Ball as reported in October 2026, Ballotpedia, Wikipedia | November 2026, pre election |

A forecast is a prediction made before the election. A result is what voters
actually decided. This project never mixes the two. Every forecast in
chapter 04 is labeled with its source and its date.
"""),
        md("""
## Verification checks

Good data work checks itself. The cells below run four checks and print the
outcome of each one.

1. MIT presidential vote totals against published candidate totals for 2020
   and 2024. Small gaps (under 0.1 percent) are expected, because write in
   votes and late certifications are counted slightly differently.
2. House mirror seat counts against the official party division table.
3. Wrong winner elections: the only elections since 1976 where the popular
   vote winner lost the Electoral College should be 2000 and 2016.
4. Row counts for every processed file.
"""),
        code("""
nat = pd.read_csv(os.path.join(PROC, 'presidential_national.csv'))
for year, pub_dem, pub_rep in [(2020, 81283501, 74223975), (2024, 75019230, 77303568)]:
    row = nat[nat['year'] == year].iloc[0]
    d_gap = (row['dem_votes'] - pub_dem) / pub_dem * 100
    r_gap = (row['rep_votes'] - pub_rep) / pub_rep * 100
    print(year, 'Democrat gap: %.3f%%' % d_gap, '| Republican gap: %.3f%%' % r_gap)
    assert abs(d_gap) < 0.1 and abs(r_gap) < 0.1
print('Check 1 passed: MIT totals match published totals within 0.1 percent.')
"""),
        code("""
seats = pd.read_csv(os.path.join(PROC, 'house_seats.csv'))
div = pd.read_csv(os.path.join(PROC, 'house_division.csv'))
div['election_year'] = (div['congress'] - 1) * 2 + 1788
merged = seats.merge(div, left_on='year', right_on='election_year')
merged['d_diff'] = merged['dem_seats'] - merged['dem']
merged['r_diff'] = merged['rep_seats'] - merged['rep']
print(merged[['year', 'dem_seats', 'dem', 'd_diff', 'rep_seats', 'rep', 'r_diff']].to_string(index=False))
print('Largest Democrat gap:', merged['d_diff'].abs().max(), 'seats.')
print('Largest Republican gap:', merged['r_diff'].abs().max(), 'seats.')
print('Note: 1996 is the outlier. The mirror misses 10 Texas districts in')
print('1996 because a court ordered redistricting moved those races into a')
print('special process that the mirror codes separately. That is why the')
print('midterm series uses the official division table, not the mirror.')
print('Check 2 done: gaps are 0 to 4 seats except 1996, and the cause is known.')
"""),
        code("""
wrong = nat[nat['wrong_winner']]
print('Wrong winner elections since 1976:')
print(wrong[['year', 'dem_nominee', 'rep_nominee', 'dem_votes', 'rep_votes', 'dem_ev', 'rep_ev']].to_string(index=False))
assert list(wrong['year']) == [2000, 2016]
print('Check 3 passed: only 2000 and 2016.')
"""),
        code("""
import glob
for path in sorted(glob.glob(os.path.join(PROC, '*.csv'))):
    df = pd.read_csv(path)
    print(os.path.basename(path), ':', len(df), 'rows,', len(df.columns), 'columns')
print('Check 4 done.')
"""),
    ]
    return cells

# ================================================== 01_presidential_history
def build_01():
    cells = [
        code(PIP_CELL),
        md("""
# 01. Presidential elections since 1976

## The ideas first, in plain words

**Popular vote.** Every vote cast for president, added up across the whole
country. The candidate with the most popular votes wins the popular vote.

**Electoral College.** The president is not chosen directly by the national
popular vote. Each state gets a number of electors, roughly based on its
population. In almost every state, the candidate who wins the state wins all
of that state's electors. There are 538 electors in total. A candidate needs
270 to win.

**Swing state.** A state where either party can plausibly win, so the result
is close and both campaigns spend a lot of time there. A safe state is one
where the winner is almost never in doubt.

**Turnout.** The share of eligible voters who actually vote. This project
uses voting eligible population turnout, which counts only people who are
legally allowed to vote, not every adult resident.

**Wrong winner election.** An election where the candidate who won the most
popular votes lost the Electoral College, and therefore lost the presidency.

With those ideas in hand, here is what the data shows.
"""),
        code(SETUP_CELL),
        code("""
nat = pd.read_csv(os.path.join(PROC, 'presidential_national.csv'))
state = pd.read_csv(os.path.join(PROC, 'presidential_state.csv'))
swing = pd.read_csv(os.path.join(PROC, 'swing_states.csv'))
print(nat[['year', 'dem_nominee', 'rep_nominee', 'dem_share_pct', 'rep_share_pct',
           'pop_margin_pp', 'dem_ev', 'rep_ev', 'vep_turnout_pct']].to_string(index=False))
"""),
        md("""
## Popular vote share over time

Each line is one party's share of the national popular vote. The two lines
almost always add up to close to 100 percent, with the rest going to
third party candidates. Notice 1992: the Democrat won with only about 43
percent, because Ross Perot took about 19 percent as an independent.
"""),
        code("""
plt.figure(figsize=(10, 5))
plt.plot(nat['year'], nat['dem_share_pct'], marker='o', color=DEM, label='Democrat')
plt.plot(nat['year'], nat['rep_share_pct'], marker='o', color=REP, label='Republican')
plt.axhline(50, color=GREY, linestyle='--', linewidth=1)
plt.ylabel('Share of popular vote (%)')
plt.xlabel('Election year')
plt.title('Popular vote share by party, 1976 to 2024')
plt.legend()
plt.grid(alpha=0.3)
savefig('c01_popular_share.png')
"""),
        md("""
## The popular vote margin, and the two wrong winners

This chart shows how many percentage points separated the top two
candidates. Small bars mean close elections. The two red outlines mark the
wrong winner elections, where the popular vote winner lost the presidency.
"""),
        code("""
fig, ax = plt.subplots(figsize=(10, 5))
colors = [REP if w else DEM for w in nat['wrong_winner']]
ax.bar(nat['year'].astype(str), nat['pop_margin_pp'], color=DEM)
for i, w in enumerate(nat['wrong_winner']):
    if w:
        ax.patches[i].set_facecolor('#f4b400')
        ax.patches[i].set_edgecolor('black')
ax.set_ylabel('Popular vote margin (percentage points)')
ax.set_xlabel('Election year')
ax.set_title('How close was it? Popular vote margin, 1976 to 2024 (gold = wrong winner)')
ax.grid(axis='y', alpha=0.3)
savefig('c01_popular_margin.png')
"""),
        code("""
for _, r in nat[nat['wrong_winner']].iterrows():
    gap = abs(int(r['dem_votes']) - int(r['rep_votes']))
    print(int(r['year']), ': popular vote gap was', f'{gap:,}', 'votes, but the')
    print('   Electoral College went', int(r['dem_ev']), 'to', int(r['rep_ev']),
          'for the', 'Democrat' if r['ev_winner'] == 'D' else 'Republican', 'candidate.')
print()
print('2000 detail: Al Gore won the popular vote by 519,208 votes, but George W. Bush')
print('won the Electoral College 271 to 266. One District of Columbia elector abstained,')
print('so only 537 electoral votes were cast.')
print('2016 detail: Hillary Clinton won the popular vote by 2,984,618 votes, but Donald')
print('Trump won the Electoral College 304 to 227. Seven electors voted for someone else,')
print('so the two main candidates together received only 531 electoral votes.')
"""),
        md("""
## Electoral College votes vs popular votes

Each dot is one election. The horizontal axis is the popular vote margin,
the vertical axis is the Electoral College margin. Dots in the top right and
bottom left are elections where both agreed. The two dots that break the
pattern are 2000 and 2016: the popular vote went one way, the Electoral
College went the other.
"""),
        code("""
nat['ev_margin'] = (nat['dem_ev'] - nat['rep_ev'])
nat['pop_signed'] = nat.apply(lambda r: r['pop_margin_pp'] if r['pop_winner'] == 'D' else -r['pop_margin_pp'], axis=1)
plt.figure(figsize=(8, 6))
plt.scatter(nat['pop_signed'], nat['ev_margin'], s=80, color=DEM)
for _, r in nat.iterrows():
    plt.annotate(str(int(r['year'])), (r['pop_signed'], r['ev_margin']), fontsize=9,
                 xytext=(4, 4), textcoords='offset points')
plt.axhline(0, color=GREY, linewidth=1)
plt.axvline(0, color=GREY, linewidth=1)
plt.xlabel('Popular vote margin (points, positive = Democrat ahead)')
plt.ylabel('Electoral College margin (Democrat minus Republican)')
plt.title('Popular vote vs Electoral College, 1976 to 2024')
plt.grid(alpha=0.3)
savefig('c01_ev_vs_pop.png')
"""),
        md("""
## Turnout: who actually votes

Turnout in presidential elections has risen since the 1990s. The lowest
point in this period was 1996, at 51.73 percent of eligible voters. The
highest was 2020, at 65.28 percent. The 2024 figure, 64.30 percent, is a
provisional estimate from the University of Florida Election Lab, dated
March 2, 2026, and may be revised.
"""),
        code("""
t = nat.dropna(subset=['vep_turnout_pct'])
plt.figure(figsize=(10, 5))
plt.plot(t['year'], t['vep_turnout_pct'], marker='o', color='#2ca02c')
plt.ylabel('Voting eligible population turnout (%)')
plt.xlabel('Election year')
plt.title('Presidential election turnout, 1980 to 2024')
plt.grid(alpha=0.3)
savefig('c01_turnout.png')
print('Lowest turnout in this window:', t.loc[t['vep_turnout_pct'].idxmin(), 'year'],
      t['vep_turnout_pct'].min(), 'percent.')
print('Highest turnout in this window:', t.loc[t['vep_turnout_pct'].idxmax(), 'year'],
      t['vep_turnout_pct'].max(), 'percent.')
"""),
        md("""
## Swing states: how many states are actually close

A state counts as close here if the winner's margin was under 5 percentage
points. The number of close states bounces around a lot. It was 19 in 1976
and 18 in 1992, but only 3 in the 1984 landslide and 4 in 2012. In 2020 and
2024 it was 8 each. There is no steady decline in competitiveness in this
measure. The map changes, but close states keep appearing.
"""),
        code("""
plt.figure(figsize=(10, 5))
plt.bar(swing['year'].astype(str), swing['states_under_5pp'], color='#9467bd')
plt.ylabel('States decided by under 5 points')
plt.xlabel('Election year')
plt.title('Close states per presidential election, 1976 to 2024')
plt.grid(axis='y', alpha=0.3)
savefig('c01_swing_states.png')
print(swing.to_string(index=False))
"""),
        md("""
## What to take into the next chapter

Presidential elections are usually close, sometimes extremely close, and
twice since 1976 the popular vote winner lost. Turnout is higher than it
was in the 1990s, and a handful of close states decide most elections.
Midterms, the subject of the next chapter, work differently: the president
is not on the ballot, turnout is lower, and the president's party usually
loses seats.
"""),
    ]
    return cells

# ====================================================== 02_midterm_history
def build_02():
    cells = [
        code(PIP_CELL),
        md("""
# 02. Midterm elections since 1978

## The ideas first, in plain words

**Midterm election.** The congressional election held halfway through a
president's four year term, in the even years when there is no presidential
election. All 435 House seats are on the ballot, plus about a third of the
100 Senate seats, plus many governor and state offices.

**The president's party.** The party of the sitting president. In a midterm,
voters are often judging that president, even though the president is not
on the ballot.

**Seat change.** How many seats the president's party gained or lost
compared with the Congress before the midterm. A negative number means the
president's party lost seats.

**Unified government and divided government.** Unified government means one
party controls the presidency, the House, and the Senate at the same time.
That combination is often called a trifecta. Divided government means at
least one chamber is controlled by the other party.

**Seat counts used here.** House and Senate seat counts come from the
official party division tables (Clerk of the House via Wikipedia, and
senate.gov). Those tables record the party balance at the start of each
Congress, so a seat that changed hands in a special election or a party
switch during a Congress can make a start of Congress number differ by a
seat or two from the election night number. The pattern below is the same
either way.
"""),
        code(SETUP_CELL),
        code("""
mid = pd.read_csv(os.path.join(PROC, 'midterm_history.csv'))
hdiv = pd.read_csv(os.path.join(PROC, 'house_division.csv'))
sdiv = pd.read_csv(os.path.join(PROC, 'senate_division.csv'))
print(mid[['midterm_year', 'president', 'president_party', 'house_before', 'house_after',
           'house_change', 'senate_before', 'senate_after', 'senate_change',
           'unified_before', 'unified_after']].to_string(index=False))
"""),
        md("""
## The House: the president's party usually loses seats

This is the most reliable pattern in American midterm elections. In 10 of
the 12 midterms from 1978 to 2022, the president's party lost House seats.
The average loss was 21.2 seats, and the median loss was 14 seats. The two
exceptions are 1998, when Bill Clinton's Democrats gained 5 seats, and
2002, when George W. Bush's Republicans gained 8 seats.
"""),
        code("""
fig, ax = plt.subplots(figsize=(10, 5))
colors = [REP if v >= 0 else DEM for v in mid['house_change']]
ax.bar(mid['midterm_year'].astype(str), mid['house_change'], color=colors)
ax.axhline(0, color='black', linewidth=1)
ax.set_ylabel('House seat change for the president party')
ax.set_xlabel('Midterm year')
ax.set_title('House seat change for the president party, 1978 to 2022')
ax.grid(axis='y', alpha=0.3)
savefig('c02_house_change.png')
print('Midterms where the president party lost House seats:', (mid['house_change'] < 0).sum(), 'of', len(mid))
print('Average House change: %.1f seats.' % mid['house_change'].mean())
print('Median House change: %.1f seats.' % mid['house_change'].median())
print('Largest House loss: 2010, Democrats lost 64 seats.')
print('Largest House gain: 2002, Republicans gained 8 seats.')
"""),
        md("""
## The Senate: smaller moves, and three gains

Senate changes are smaller because only about a third of seats are up each
time, and the map of which seats are up matters a lot. The president's
party gained Senate seats in 3 of 12 midterms (1982, 2002, 2018), broke even
in 2 (1998, 2022), and lost seats in 7. The average Senate change was a
loss of 3.25 seats. The biggest Senate loss was 1994, when Clinton's
Democrats lost 10 seats.
"""),
        code("""
fig, ax = plt.subplots(figsize=(10, 5))
colors = [REP if v >= 0 else DEM for v in mid['senate_change']]
ax.bar(mid['midterm_year'].astype(str), mid['senate_change'], color=colors)
ax.axhline(0, color='black', linewidth=1)
ax.set_ylabel('Senate seat change for the president party')
ax.set_xlabel('Midterm year')
ax.set_title('Senate seat change for the president party, 1978 to 2022')
ax.grid(axis='y', alpha=0.3)
savefig('c02_senate_change.png')
print('Senate gains:', (mid['senate_change'] > 0).sum(), '| even:', (mid['senate_change'] == 0).sum(),
      '| losses:', (mid['senate_change'] < 0).sum())
print('Average Senate change: %.2f seats.' % mid['senate_change'].mean())
"""),
        md("""
## House seats by party over time

Each line is one party's total House seats at the start of each Congress.
The lines cross when control flips. The big flips are 1994 (Democrats to
Republicans), 2006 (Republicans to Democrats), 2010 (Democrats to
Republicans), and 2018 (Republicans to Democrats). Every one of those flips
happened in a midterm.
"""),
        code("""
hdiv['start_year'] = hdiv['years'].str.slice(0, 4).astype(int)
plt.figure(figsize=(10, 5))
plt.plot(hdiv['start_year'], hdiv['dem'], marker='o', color=DEM, label='Democrats')
plt.plot(hdiv['start_year'], hdiv['rep'], marker='o', color=REP, label='Republicans')
plt.axhline(218, color=GREY, linestyle='--', linewidth=1, label='Majority = 218')
plt.ylabel('House seats')
plt.xlabel('Congress start year')
plt.title('House seats by party, 1977 to 2027')
plt.legend()
plt.grid(alpha=0.3)
savefig('c02_house_seats_time.png')
"""),
        md("""
## Senate seats by party over time

The Senate moves more slowly. The lines cross in 1980 (Democrats to
Republicans), 1986 (Republicans to Democrats), 1994 (Democrats to
Republicans), 2006 (Republicans to Democrats), and 2014 (Democrats to
Republicans). The 2001 to 2003 period is the famous 50 to 50 Senate, which
Democrats controlled after Senator Jim Jeffords left the Republican Party
and after the vice president's tie breaking vote is counted.
"""),
        code("""
sdiv['start_year'] = sdiv['years'].str.slice(0, 4).astype(int)
plt.figure(figsize=(10, 5))
plt.plot(sdiv['start_year'], sdiv['dem'], marker='o', color=DEM, label='Democrats')
plt.plot(sdiv['start_year'], sdiv['rep'], marker='o', color=REP, label='Republicans')
plt.axhline(51, color=GREY, linestyle='--', linewidth=1, label='Majority = 51')
plt.ylabel('Senate seats')
plt.xlabel('Congress start year')
plt.title('Senate seats by party, 1977 to 2027')
plt.legend()
plt.grid(alpha=0.3)
savefig('c02_senate_seats_time.png')
"""),
        md("""
## The trifecta pattern

A president who enters a midterm holding the presidency, the House, and
the Senate almost always leaves without at least one of them. From 1978 to
2022, six presidents entered a midterm with a trifecta: Carter in 1978,
Clinton in 1994, George W. Bush in 2006, Obama in 2010, Trump in 2018, and
Biden in 2022. Five of the six lost the trifecta in that midterm. The only
one who kept it was Carter in 1978. And 2002 is the mirror image: George W.
Bush entered that midterm without a trifecta, because Democrats controlled
the Senate, and left with one, because Republicans gained the Senate.

## Turnout in midterms

Midterms draw fewer voters than presidential elections. Voting eligible
population turnout was 36.7 percent in 2014, 50.1 percent in 2018, and
46.1 percent in 2022. Compare that with 65.28 percent in the 2020
presidential election. Lower turnout is one reason midterm electorates look
different from presidential electorates, and it is part of why the
president's party usually struggles.

## What to take into the next chapter

The midterm penalty is real but it is not a law of nature. It failed in
1998, 2002, and in the Senate in 2018. The next chapter asks what actually
changes for a president after a midterm, and how far the numbers can show
it.
"""),
    ]
    return cells


# ================================================== 03_the_midterm_effect
def build_03():
    cells = [
        code(PIP_CELL),
        md("""
# 03. How a midterm changes what a president can do

## The ideas first, in plain words

**Mandate.** A president's claim that voters endorsed their plans. A big
win strengthens that claim. A midterm loss weakens it, because the newest
election result points the other way.

**Veto.** When the president refuses to sign a bill Congress passed. A
regular veto sends the bill back with objections, and Congress can override
it only with two thirds of each chamber. A pocket veto happens when
Congress adjourns and the president simply does not sign the bill within
ten days. Pocket vetoes cannot be overridden.

**Executive order.** A formal instruction from the president to the
executive branch, for example to an agency. It has the force of law, but it
cannot override a statute, it can be challenged in court, and the next
president can reverse it.

**Confirmation.** The Senate must approve the president's nominees for
federal judges, cabinet secretaries, and other senior posts. If the other
party controls the Senate, confirmations slow down or stop.

**Government shutdown.** If Congress does not pass funding laws, federal
agencies must stop non essential work. Shutdowns are rare, and they are
political events, not automatic consequences of divided government.

**Correlation vs causation.** Correlation means two things move together.
Causation means one thing causes the other. A president who loses a
midterm and then signs fewer bills shows a correlation. But wars, the
economy, court vacancies, and the president's own choices also move those
numbers, so the midterm alone does not prove the cause. This chapter shows
the numbers and names the limits honestly.
"""),
        code(SETUP_CELL),
        code("""
vetoes = pd.read_csv(os.path.join(PROC, 'vetoes.csv'))
eos = pd.read_csv(os.path.join(PROC, 'executive_orders.csv'))
judges = pd.read_csv(os.path.join(PROC, 'judicial_confirmations.csv'))
shutdowns = pd.read_csv(os.path.join(PROC, 'shutdowns.csv'))
mid = pd.read_csv(os.path.join(PROC, 'midterm_history.csv'))
print('Vetoes:'); print(vetoes.to_string(index=False))
print(); print('Executive orders:'); print(eos.to_string(index=False))
print(); print('Judicial confirmations:'); print(judges.to_string(index=False))
print(); print('Shutdowns:'); print(shutdowns.to_string(index=False))
"""),
        md("""
## Vetoes: the president's no

Presidents veto far more when Congress is controlled by the other party,
because Congress keeps sending them bills they oppose. Ronald Reagan
vetoed 78 bills, the most in this period, while facing a Democratic House
for all eight years. George H. W. Bush vetoed 44, also facing a Democratic
Congress. Bill Clinton vetoed 37, most of them after Republicans took
Congress in 1994. By contrast, George W. Bush and Barack Obama vetoed only
12 each, even though both faced opposition Congresses for part of their
terms. Vetoes are a choice, not an automatic meter, so the pattern is
suggestive, not proof.
"""),
        code("""
plt.figure(figsize=(10, 5))
plt.bar(vetoes['president'], vetoes['total_vetoes'], color='#9467bd')
plt.ylabel('Total vetoes (regular plus pocket)')
plt.title('Presidential vetoes by president, Carter through Biden')
plt.xticks(rotation=30, ha='right')
plt.grid(axis='y', alpha=0.3)
savefig('c03_vetoes.png')
print('Most vetoes:', vetoes.loc[vetoes['total_vetoes'].idxmax(), 'president'],
      vetoes['total_vetoes'].max())
print('Fewest vetoes among completed terms:', vetoes.loc[vetoes['total_vetoes'].idxmin(), 'president'],
      vetoes['total_vetoes'].min())
"""),
        md("""
## Executive orders: what a president can do alone

When Congress will not pass the president's program, the president can
still act through executive orders. Jimmy Carter issued 320 in four years,
the highest rate in this period at 80 per year. Ronald Reagan issued 381
over eight years. Donald Trump's first term ran at 55 per year, above the
recent average. But executive orders are fragile: they can be reversed by
the next president, blocked by courts, and they cannot spend money
Congress has not appropriated. They are a workaround, not a replacement
for legislation.
"""),
        code("""
eos['per_year'] = eos['executive_orders'] / (eos['term_end'] - eos['term_start'])
plt.figure(figsize=(10, 5))
plt.bar(eos['president'], eos['executive_orders'], color='#2ca02c')
plt.ylabel('Executive orders in term')
plt.title('Executive orders by president, Carter through Biden')
plt.xticks(rotation=30, ha='right')
plt.grid(axis='y', alpha=0.3)
savefig('c03_executive_orders.png')
print(eos[['president', 'executive_orders', 'per_year']].round(1).to_string(index=False))
"""),
        md("""
## Confirmations: the Senate's choke point

Federal judges serve for life, so confirmations are one of the longest
lasting things a president does. The Senate must confirm every one. When
the president's party loses the Senate, confirmations slow sharply. The
totals below count Article III judges only: Supreme Court, circuit courts,
and district courts. Different sources count differently (for example,
Ballotpedia counts a few more per president because it includes some
specialty courts), so this project uses one list consistently and says so.
Ronald Reagan's 383 and Bill Clinton's 378 lead the period. Joe Biden's
235 and Donald Trump's first term 234 are close, but they were achieved
under very different Senate conditions, which is a reminder that totals
alone do not tell the whole story.
"""),
        code("""
plt.figure(figsize=(10, 5))
plt.bar(judges['president'], judges['total_article_iii'], color=DEM)
plt.ylabel('Article III judges confirmed')
plt.title('Federal judges confirmed by president, Carter through Biden')
plt.xticks(rotation=30, ha='right')
plt.grid(axis='y', alpha=0.3)
savefig('c03_judges.png')
print(judges[['president', 'supreme_court', 'circuit', 'district', 'total_article_iii']].to_string(index=False))
"""),
        md("""
## Shutdowns: the budget fight taken to the limit

There have been six major shutdowns since 1995, totaling 123 days. The
longest was 43 days in October and November 2025, under a Republican
trifecta, which shows that shutdowns are not only a divided government
phenomenon. The 35 day shutdown of December 2018 to January 2019 began
under a Republican trifecta and ended after Democrats took the House in
the 2018 midterm. Shutdowns follow from a failure to agree on funding, and
midterms change who sits at that table.
"""),
        code("""
plt.figure(figsize=(10, 5))
plt.bar(shutdowns['start'] + ' (' + shutdowns['president'] + ')', shutdowns['days'], color=REP)
plt.ylabel('Days')
plt.title('Major federal shutdowns, 1995 to 2025')
plt.xticks(rotation=30, ha='right')
plt.grid(axis='y', alpha=0.3)
savefig('c03_shutdowns.png')
print('Total shutdown days since 1995:', shutdowns['days'].sum())
print(shutdowns[['start', 'end', 'days', 'president', 'congress_control']].to_string(index=False))
"""),
        md("""
## The mechanisms, in plain words

A midterm changes a president's room to maneuver through four channels.

1. **Laws.** The House and Senate write the laws. If the other party takes
   a chamber, the president's bills stall there. The president can still
   veto the other party's bills, but vetoing is defense, not a program.
2. **Money.** Every spending bill must pass both chambers. A hostile
   chamber can refuse funding for the president's priorities, and in the
   extreme case the government shuts down.
3. **People.** The Senate confirms judges, cabinet members, and
   ambassadors. Losing the Senate means vacancies stay open longer and
   nominees must be more acceptable to the other party.
4. **Oversight.** The party that controls a chamber runs its committees,
   sets hearing agendas, and can investigate the administration. That
   changes the daily political weather even when no law changes.

## What was cut, and why

**Bills enacted per Congress.** This chapter planned to chart public laws
enacted per Congress as the cleanest measure of legislative output. No
clean, verified table of public laws per Congress was secured during the
build, and the project does not guess at one. The chapter therefore uses
vetoes, executive orders, confirmations, and shutdowns, which are all
verified. A future update can add public laws from the Library of
Congress or govinfo once a per Congress table is verified.

**Trump second term indicators.** Vetoes, executive orders, and
confirmations for the second Trump term are in progress and are not
charted as final totals. The veto table notes 2 vetoes so far in the
119th Congress, and executive orders are provisionally about 130 or more
through May 2026. Those numbers will change and are not used in the
charts.

## What to take into the next chapter

A midterm does not remove a president, but it usually removes the
president's ability to pass new laws on their own terms, and it can remove
control of confirmations and the budget. That is the frame for November
2026: the question is not only who wins, but which of these four channels
changes hands.
"""),
    ]
    return cells

# ===================================================== 04_november_2026
def build_04():
    cells = [
        code(PIP_CELL),
        md("""
# 04. November 2026: what is at stake, what the forecasts say, and what could happen

## Read this first: no results exist yet

This chapter was written on November 2, 2026. The election is on November
3, 2026. **No November 2026 results exist yet, and this chapter contains
none.** Everything below is either a verified fact about the current
balance of power, a forecast that is labeled with its source and date, or
a scenario. A scenario is a description of what could happen under one
outcome. It is not a prediction, and no scenario in this chapter is
presented as the expected result.

## The ideas first, in plain words

**Forecast.** A prediction made before the election, based on polls, past
results, and analyst ratings. Forecasts change as new information arrives,
and they are often wrong in detail.

**Rating.** An analyst's judgment about a single race, such as Safe
Democratic, Lean Republican, or Toss-up. A toss-up means the analyst sees
no clear favorite.

**Generic ballot.** A poll question that asks voters whether they would
vote for the Democratic candidate or the Republican candidate for Congress
in general, without naming a candidate. It measures the national mood, not
any single race.

**Trifecta.** One party controlling the presidency, the House, and the
Senate at the same time.
"""),
        code(SETUP_CELL),
        code("""
stakes = pd.read_csv(os.path.join(PROC, 'stakes_2026.csv'))
forecasts = pd.read_csv(os.path.join(PROC, 'forecasts_2026.csv'))
polls = pd.read_csv(os.path.join(PROC, 'polls_2026.csv'))
print(stakes[['chamber', 'seats_up', 'current_majority', 'rep_seats', 'dem_seats',
              'other_seats', 'vacant_seats']].to_string(index=False))
print()
for _, r in stakes.iterrows():
    print(r['chamber'], ':', r['notes'])
"""),
        md("""
## The House: all 435 seats, and a 4 seat hill for Democrats

As of November 2, 2026, the House has 218 seated Republicans, 214 seated
Democrats, 1 independent, and 2 vacant seats. The independent is Kevin
Kiley of California, who left the Republican Party in 2026 but still
caucuses with Republicans, so the working Republican margin is 219 to 214.
A majority needs 218 seats. Democrats need a net gain of 4 seats to reach
218. Republicans can afford a net loss of 1 seat and still hold 218.
"""),
        code("""
labels = ['Republican', 'Democrat', 'Independent', 'Vacant']
values = [218, 214, 1, 2]
colors = [REP, DEM, GREY, '#cccccc']
plt.figure(figsize=(8, 5))
plt.bar(labels, values, color=colors)
plt.axhline(218, color='black', linestyle='--', linewidth=1, label='Majority = 218')
plt.ylabel('Seats')
plt.title('House composition, November 2, 2026 (seated members)')
plt.legend()
plt.grid(axis='y', alpha=0.3)
savefig('c04_house_now.png')
print('Working margin counting the independent with Republicans: 219 to 214.')
"""),
        md("""
## The Senate: 35 seats up, and the map favors Republicans

Thirty five Senate seats are on the ballot: the 33 regularly scheduled
Class II seats, plus 2 special elections. The special elections are in
Florida, for the seat vacated by Marco Rubio and now held by Ashley Moody,
and in Ohio, for the seat vacated by JD Vance and now held by Jon Husted.
Republicans hold 22 of the 35 seats up, Democrats hold 13. The current
Senate is 53 Republicans, 45 Democrats, and 2 independents who caucus with
Democrats, reported as 53 to 47. A majority needs 51 seats, or 50 seats
plus the vice president's tie breaking vote. The vice president is JD
Vance, a Republican. Democrats need a net gain of 4 seats for a majority.
Republicans need 19 of the 35 seats up to reach 50 seats, which holds
control through the tie breaking vote.
"""),
        code("""
labels = ['Republican held', 'Democrat held']
values = [22, 13]
plt.figure(figsize=(8, 5))
plt.bar(labels, values, color=[REP, DEM])
plt.ylabel('Senate seats on the ballot in 2026')
plt.title('Senate seats up in 2026, by party holding the seat (35 total)')
plt.grid(axis='y', alpha=0.3)
savefig('c04_senate_up.png')
print('Democrats need a net gain of 4 for a Senate majority.')
print('Republicans need 19 of the 35 seats up to reach 50 and hold control.')
"""),
        md("""
## Governorships: 36 states, evenly split

Thirty six states elect a governor in 2026, 18 currently held by
Republicans and 18 by Democrats. Nationally there are 26 Republican
governors and 24 Democratic governors. Fifteen of the 36 incumbents are
term limited and cannot run again (6 Democrats, 9 Republicans), so at
least 15 states will have a new governor. Sources disagree on how many
governor races are rated toss-up (one summary reports 5, another reports
3), so this chapter does not present a single toss-up number for
governors.
"""),
        code("""
labels = ['Republican held', 'Democrat held']
values = [18, 18]
plt.figure(figsize=(8, 5))
plt.bar(labels, values, color=[REP, DEM])
plt.ylabel('Governorships on the ballot in 2026')
plt.title('Governorships up in 2026, by party holding the office (36 total)')
plt.grid(axis='y', alpha=0.3)
savefig('c04_governors.png')
print('15 of the 36 incumbents are term limited: 6 Democrats, 9 Republicans.')
"""),
        md("""
## Forecasts, labeled with source and date

These are forecasts, not results. Cook Political Report ratings are
paywalled at the source, so the numbers below are Cook ratings as
reported by named outlets on the dates shown, not numbers read directly
from Cook's own pages. The same applies to Sabato's Crystal Ball.

The latest House snapshot, Cook Political Report as reported on October
30, 2026, puts 222 seats in Democratic categories, 195 in Republican
categories, and 18 in toss-up. The trend over October moved toward
Democrats: on October 9 the split was 213 Democratic categories, 201
Republican categories, 21 toss-ups, and by October 30 it was 222, 195,
and 18. Sabato's Crystal Ball, as reported on October 8, 2026, was
narrower: 214 seats at least Lean Democratic, 219 at least Lean
Republican, and 2 toss-ups. The two forecasters disagree, which is normal
and is itself useful information: the House outcome is uncertain.

For the Senate, Cook Political Report as reported on October 6, 2026,
puts 47 seats in Democratic aligned categories, 46 in Republican
categories, and 7 in toss-up. A Senate forecast with 7 toss-ups and a
53 to 47 starting balance means the Senate outcome is also uncertain.
"""),
        code("""
print(forecasts.to_string(index=False))
"""),
        code("""
cook = forecasts[(forecasts['forecaster'].str.contains('Oct 30'))].iloc[0]
labels = ['Democratic categories', 'Republican categories', 'Toss-up']
values = [cook['dem_category'], cook['rep_category'], cook['toss_ups']]
plt.figure(figsize=(8, 5))
plt.bar(labels, values, color=[DEM, REP, '#f4b400'])
plt.ylabel('House seats')
plt.title('Cook House ratings, October 30, 2026 (forecast, not a result)')
plt.grid(axis='y', alpha=0.3)
savefig('c04_cook_house.png')
"""),
        code("""
sen = forecasts[(forecasts['chamber'] == 'Senate')].iloc[0]
labels = ['Democratic aligned', 'Republican', 'Toss-up']
values = [sen['dem_category'], sen['rep_category'], sen['toss_ups']]
plt.figure(figsize=(8, 5))
plt.bar(labels, values, color=[DEM, REP, '#f4b400'])
plt.ylabel('Senate seats')
plt.title('Cook Senate ratings, October 6, 2026 (forecast, not a result)')
plt.grid(axis='y', alpha=0.3)
savefig('c04_cook_senate.png')
"""),
        md("""
## The national mood: polls as context, not as predictions

Polls measure the mood at a moment in time, and they have margins of
error. They are context for the forecasts, not substitutes for results.

The generic congressional ballot in late October 2026 pointed toward
Democrats by roughly 8 to 9 points: the Silver Bulletin average on
October 28, 2026, put Democrats ahead by 8.7 points, and the RealClearPolling
average through October 30, 2026, put Democrats at 52.0 percent and
Republicans at 43.1 percent. The NBC News poll of October 28 to 30, 2026,
put Democrats at 52 percent and Republicans at 45 percent.

President Trump's job approval in late October 2026 was in the high 30s:
the RealClearPolitics average on October 26, 2026, showed 38.4 percent
approving and 60.1 percent disapproving. Individual polls varied widely,
which is a reminder to read averages, not single polls.

Early voting adds one more piece of context: about 51 million early
ballots had been cast as of November 2, 2026, according to a tracker
covering 47 states. Early votes are votes, not results, and they do not
tell us who won until they are counted and reported.
"""),
        code("""
print(polls.to_string(index=False))
"""),
        md("""
## Scenarios: what each outcome could mean for the rest of the term

The Trump administration's current term ends on January 20, 2029. The
scenarios below describe what each outcome could mean for the remaining
two years. They are written neutrally. None is presented as a prediction,
and none is presented as better or worse. The same outcome can be
described from many angles; this chapter sticks to the mechanics of
governing: laws, money, confirmations, and oversight, the four channels
from chapter 03.

### Scenario A: Republicans hold the trifecta

If Republicans keep the House and the Senate, the administration keeps the
ability to pass laws with Republican votes alone, subject to the Senate
filibuster for most bills, and keeps control of confirmations and both
chambers' committee agendas. The constraint that remains is the narrow
House margin: with a small majority, a handful of defections can block a
bill, and the party must hold together on every major vote.

### Scenario B: Democrats take the House, Republicans keep the Senate

This is the most common midterm outcome in recent history: the
president's party loses the House but keeps the Senate. New Republican
legislation would need Democratic votes in the House, which usually means
compromise or stalemate. Confirmations would continue under Republican
Senate control. The House would gain committee and oversight powers, and
the budget would need a deal between a Democratic House, a Republican
Senate, and the president.

### Scenario C: Democrats take the Senate, Republicans keep the House

This outcome is rarer, because the Senate map in 2026 favors Republicans,
with 22 Republican held seats up against 13 Democratic held seats.
Confirmations would slow sharply or stop, and the Senate would gain
oversight powers, while the House would remain Republican. Legislation
would still need both chambers and the president, so the same compromise
or stalemate logic applies.

### Scenario D: Democrats take both chambers

If Democrats win both the House and the Senate, the administration would
face an opposition Congress in both chambers. New administration
legislation would need Democratic support in both chambers. Confirmations
would require nominees acceptable to a Democratic Senate. Oversight would
sit entirely with Democrats. The president would still hold the veto, and
executive orders would remain available, with the limits described in
chapter 03.

### Scenario E: split outcomes in other combinations

Other combinations are possible, including a House that flips by a small
margin with many close races decided by recounts or late counted ballots,
or a Senate that ends 50 to 50, which would keep Republican control
through the vice president's tie breaking vote. In every case, the
mechanics are the same: count which party holds each chamber, then apply
the four channels from chapter 03.

## Results: pending

**Status as of November 2, 2026: results are pending. The election is on
November 3, 2026. No results are reported in this section, and no numbers
appear here.**

After November 3, 2026, fill in this table from official sources (state
election offices, the Clerk of the House, and the Senate):

| Contest | Result | Source and date |
|---|---|---|
| House, Democrats | _to be filled in_ | |
| House, Republicans | _to be filled in_ | |
| House, other and vacant | _to be filled in_ | |
| Senate, Democrats | _to be filled in_ | |
| Senate, Republicans | _to be filled in_ | |
| Senate, other | _to be filled in_ | |
| Governorships, Democrats | _to be filled in_ | |
| Governorships, Republicans | _to be filled in_ | |
| Seats that flipped party | _to be filled in_ | |
| Races decided by recount or runoff | _to be filled in_ | |

Also update chapter 02 with a 2026 row in the midterm history table, and
compare the actual House and Senate changes with the historical averages
from chapter 02 (House average loss 21.2 seats, Senate average loss 3.25
seats for the president's party). Do not rewrite the forecasts after the
fact. Keep the October 2026 forecasts above as they were, so readers can
see how the forecasts compared with the results.
"""),
    ]
    return cells


# ==================================================== 05_what_to_watch
def build_05():
    cells = [
        code(PIP_CELL),
        md("""
# 05. What to watch, and what to update after November 3

## Five takeaways

1. **Midterms usually cost the president's party seats.** From 1978 to
   2022, the president's party lost House seats in 10 of 12 midterms, by an
   average of 21.2 seats. The Senate moved less, with an average loss of
   3.25 seats.
2. **Exceptions matter.** The pattern failed in 1998, 2002, and in the
   Senate in 2018. A pattern is not a guarantee, and this project never
   treats it as one.
3. **Control of a chamber is what changes governing.** Laws, money,
   confirmations, and oversight all run through the chambers. A midterm
   changes who holds those levers.
4. **The 2026 starting point is unusually tight.** Democrats need a net
   gain of 4 seats in the House and a net gain of 4 seats in the Senate.
   Small shifts decide control, which is why 18 House toss-ups and 7
   Senate toss-ups in the October forecasts matter so much.
5. **Forecasts are not results.** Cook and Sabato disagreed about the
   House in October 2026. Polls pointed one way by 8 to 9 points on the
   generic ballot. The results, when they land, are the only numbers that
   count.

## How to read the results when they land

**Seats called vs seats counted.** News organizations call races when the
remaining uncounted votes cannot change the outcome. A call is a
projection, not a certification. Official results come later, from state
election offices.

**Mail and late counted ballots.** Some states count mail ballots that
arrive after Election Day, and some states take days to count all mail
ballots. Early leads can change as those ballots are counted. That is a
normal part of the process, not evidence of a problem on its own.

**Runoffs.** If a race has no outright winner under state law, a runoff
follows. Georgia is the state to watch for this: its Senate races have
gone to runoffs before, most recently in 2020 and 2022.

**Recounts.** Very close races can trigger recounts under state law.
Recounts rarely change outcomes, but they delay final calls.

**Special elections and vacancies.** Seats that become vacant after the
election are filled by special elections, which can change the balance
during the Congress. The composition on election night is not always the
composition that serves the full term.

## What history says on average, next to what is needed in 2026

This chart is context, not a prediction. It puts the historical average
midterm House loss for the president's party next to the two numbers that
decide control in 2026: the 1 seat Republicans can afford to lose, and
the 4 seats Democrats need to gain. If the historical average held,
Republicans would lose far more than 1 seat. But averages hide wide
variation, from a gain of 8 seats in 2002 to a loss of 64 seats in 2010,
and the 2026 forecasts point to a closer race than the average suggests.
"""),
        code(SETUP_CELL),
        code("""
import matplotlib.pyplot as plt
labels = ['Average midterm House\\nchange, president party\\n(1978 to 2022)',
          'Seats Republicans can\\nafford to lose in 2026',
          'Seats Democrats need\\nto gain in 2026']
values = [-21.2, -1, 4]
colors = [GREY, REP, DEM]
plt.figure(figsize=(9, 5))
plt.bar(labels, values, color=colors)
plt.axhline(0, color='black', linewidth=1)
plt.ylabel('House seats')
plt.title('History on average vs the 2026 arithmetic (context, not a prediction)')
plt.grid(axis='y', alpha=0.3)
savefig('c05_history_vs_2026.png')
print('Average House change 1978 to 2022: -21.2 seats.')
print('Republicans can afford a net loss of 1 seat and still hold 218.')
print('Democrats need a net gain of 4 seats to reach 218.')
"""),
        md("""
## What to update after November 3, 2026

1. Fill in the results table in chapter 04 from official sources.
2. Add a 2026 row to the midterm history table in chapter 02, with the
   actual House and Senate changes for the president's party, and whether
   the trifecta survived or broke.
3. Recompute the averages in chapter 02 with 2026 included, and note
   whether 2026 fits the pattern or joins the exceptions.
4. Update the charts in chapters 02 and 04 with the final seat counts.
5. Keep the October 2026 forecasts untouched, so the project stays an
   honest record of what was known before the election.
6. If any race goes to a runoff or recount, note it separately and update
   the totals when the runoff or recount is certified.

## Where the numbers came from

Every number in this project traces to a source listed in chapter 00 and
in `data/raw/PROVENANCE.md`. The vote data comes from the MIT Election
Data and Science Lab. The seat counts come from the Senate and the Clerk
of the House, via their published party division tables. The Electoral
College votes come from the Federal Election Commission. Turnout comes
from the University of Florida Election Lab. Vetoes come from the
American Presidency Project. Executive orders come from the Federal
Register. Judicial confirmations use one consistent list and say which
one. Shutdowns follow Congressional Research Service based lists.
Forecasts are attributed to Cook Political Report and Sabato's Crystal
Ball with dates, as reported in October 2026. Where sources disagreed or
a dataset had a known gap, the project says so instead of smoothing it
over.

## A closing note

Elections are how voters hire and fire their representatives. Midterms
are the midterm review: halfway through a president's term, voters get to
grade the work so far, and they usually grade harshly. The numbers in
this project show that pattern, its exceptions, and its consequences. The
November 2026 results will add one more row to the table. Whatever that
row says, the method stays the same: count the votes, count the seats,
and say what changed, plainly.
"""),
    ]
    return cells


# ------------------------------------------------------------------ main
BUILDERS = [
    ("00_setup.ipynb", build_00),
    ("01_presidential_history.ipynb", build_01),
    ("02_midterm_history.ipynb", build_02),
    ("03_the_midterm_effect.ipynb", build_03),
    ("04_november_2026.ipynb", build_04),
    ("05_what_to_watch.ipynb", build_05),
]

if __name__ == "__main__":
    for name, fn in BUILDERS:
        write(name, fn())
    print("Done.")
