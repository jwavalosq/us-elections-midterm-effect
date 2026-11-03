"""Build processed CSVs for US Elections: The Midterm Effect.

Reads the raw MIT Election Lab files and the keithpotz House mirror, plus
hand-verified tables (Electoral College, party divisions, turnout, vetoes,
executive orders, judges, shutdowns, 2026 stakes and forecasts). Every
hand-entered table cites its source in data/raw/PROVENANCE.md.

Run from the project root: .venv/bin/python scripts/build_processed.py
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
PROC = os.path.join(ROOT, "data", "processed")
os.makedirs(PROC, exist_ok=True)

# ---------------------------------------------------------------- president
pres = pd.read_csv(os.path.join(RAW, "president_1976_2024.csv"), low_memory=False)
pres["candidatevotes"] = pd.to_numeric(pres["candidatevotes"], errors="coerce")
pres["totalvotes"] = pd.to_numeric(pres["totalvotes"], errors="coerce")

# National total per state-year: totalvotes is repeated on every candidate
# row, so take the first non-null value per state-year.
state_totals = (
    pres.dropna(subset=["totalvotes"])
    .sort_values(["year", "state"])
    .groupby(["year", "state"])["totalvotes"]
    .first()
    .reset_index()
)
nat_total = state_totals.groupby("year")["totalvotes"].sum()

party_votes = pres.groupby(["year", "party_simplified"])["candidatevotes"].sum().unstack(fill_value=0)
for col in ["DEMOCRAT", "REPUBLICAN"]:
    if col not in party_votes.columns:
        party_votes[col] = 0

# Nominees: highest-vote candidate per party per year.
nom = {}
for (year, party), grp in pres.groupby(["year", "party_simplified"]):
    if party in ("DEMOCRAT", "REPUBLICAN"):
        top = grp.loc[grp["candidatevotes"].idxmax(), "candidate"]
        nom[(year, party)] = top

# Electoral College votes as (Democrat, Republican, other/faithless).
# Source: FEC official presidential general election results.
EV = {
    1976: (297, 240, 1), 1980: (49, 489, 0), 1984: (13, 525, 0),
    1988: (111, 426, 1), 1992: (370, 168, 0), 1996: (379, 159, 0),
    2000: (266, 271, 0), 2004: (251, 286, 1), 2008: (365, 173, 0),
    2012: (332, 206, 0), 2016: (227, 304, 7), 2020: (306, 232, 0),
    2024: (226, 312, 0),
}
# Voting-eligible population turnout, UF Election Lab (McDonald), via
# Wikipedia "Voter turnout in United States presidential elections".
# 2024 is the UF estimate of March 2, 2026 and is provisional.
VEP = {
    1980: 58.49, 1984: 55.25, 1988: 52.76, 1992: 58.22, 1996: 51.73,
    2000: 54.24, 2004: 60.13, 2008: 61.60, 2012: 58.05, 2016: 59.18,
    2020: 65.28, 2024: 64.30,
}
MIDTERM_VEP = {2014: 36.7, 2018: 50.1, 2022: 46.1}

rows = []
for year in sorted(nat_total.index):
    year = int(year)
    total = nat_total[year]
    dv = party_votes.loc[year, "DEMOCRAT"]
    rv = party_votes.loc[year, "REPUBLICAN"]
    ov = total - dv - rv
    dem_ev, rep_ev, other_ev = EV[year]
    pop_winner = "D" if dv > rv else "R"
    ev_winner = "D" if dem_ev > rep_ev else "R"
    rows.append({
        "year": year,
        "dem_nominee": nom.get((year, "DEMOCRAT"), ""),
        "rep_nominee": nom.get((year, "REPUBLICAN"), ""),
        "dem_votes": int(dv), "rep_votes": int(rv), "other_votes": int(ov),
        "total_votes": int(total),
        "dem_share_pct": round(dv / total * 100, 2),
        "rep_share_pct": round(rv / total * 100, 2),
        "pop_margin_pp": round(abs(dv - rv) / total * 100, 2),
        "pop_winner": pop_winner,
        "dem_ev": dem_ev, "rep_ev": rep_ev, "other_ev": other_ev,
        "ev_winner": ev_winner,
        "wrong_winner": pop_winner != ev_winner,
        "vep_turnout_pct": VEP.get(year, float("nan")),
    })
pres_nat = pd.DataFrame(rows)
pres_nat.to_csv(os.path.join(PROC, "presidential_national.csv"), index=False)
print("presidential_national.csv:", len(pres_nat), "elections")
print(pres_nat[["year", "dem_votes", "rep_votes", "total_votes", "pop_winner", "ev_winner", "wrong_winner"]].to_string(index=False))

# State-level presidential results (Democrat and Republican votes only).
state_rows = []
for (year, state, po), grp in pres.groupby(["year", "state", "state_po"]):
    dv = grp.loc[grp["party_simplified"] == "DEMOCRAT", "candidatevotes"].sum()
    rv = grp.loc[grp["party_simplified"] == "REPUBLICAN", "candidatevotes"].sum()
    tot = grp["totalvotes"].dropna().iloc[0] if grp["totalvotes"].notna().any() else float("nan")
    state_rows.append({
        "year": int(year), "state": state, "state_po": po,
        "dem_votes": dv, "rep_votes": rv, "total_votes": tot,
        "dem_share_pct": round(dv / tot * 100, 2) if tot else float("nan"),
        "margin_pp": round((dv - rv) / tot * 100, 2) if tot else float("nan"),
        "winner": "D" if dv > rv else "R",
    })
pres_state = pd.DataFrame(state_rows)
pres_state.to_csv(os.path.join(PROC, "presidential_state.csv"), index=False)
print("presidential_state.csv:", len(pres_state), "state-years")

# Swing states per election: states decided by under 5 points.
swing = pres_state.assign(close=(pres_state["margin_pp"].abs() < 5)).groupby("year")["close"].sum().reset_index()
swing.columns = ["year", "states_under_5pp"]
swing.to_csv(os.path.join(PROC, "swing_states.csv"), index=False)
print(swing.to_string(index=False))

# --------------------------------------------------------------------- House
# The mirror file wraps every data line in double quotes, and candidate
# names carry escaped quotes and commas, which breaks normal CSV parsing.
# Only the candidate field can contain commas or quotes, so parse by
# position: fields 0-10 are fixed, the candidate is everything between
# field 11 and the last 8 fields, and the last 8 fields are fixed.
with open(os.path.join(RAW, "house_1976_2024_mirror.csv"), encoding="utf-8") as _f:
    _lines = _f.read().splitlines()
_house_rows = []
for _ln in _lines[1:]:
    if _ln.startswith('"') and _ln.endswith('"'):
        _ln = _ln[1:-1]
    _parts = _ln.split(",")
    if len(_parts) < 20:
        continue
    _cand = ",".join(_parts[11:-8]).strip().strip('"').replace('\\"', '"').replace("\\", "")
    _house_rows.append({
        "year": _parts[0], "state": _parts[1], "state_po": _parts[2],
        "district": _parts[7], "stage": _parts[8], "runoff": _parts[9],
        "special": _parts[10], "candidate": _cand, "party": _parts[-8],
        "writein": _parts[-7], "mode": _parts[-6],
        "candidatevotes": _parts[-5], "totalvotes": _parts[-4],
    })
house = pd.DataFrame(_house_rows)
house["candidatevotes"] = pd.to_numeric(house["candidatevotes"], errors="coerce")
house["special"] = house["special"].astype(str).str.lower().isin(["true", "1", "t"])
if "TOTAL" in house["mode"].astype(str).str.upper().unique():
    house = house[house["mode"].astype(str).str.upper() == "TOTAL"]
gen = house[~house["special"]].copy()
gen["stage_norm"] = gen["stage"].astype(str).str.lower().str.strip()
gen = gen[gen["stage_norm"].isin(["gen"]) | gen["stage_norm"].str.contains("runoff")]
print("House mirror stage values:", sorted(gen["stage_norm"].dropna().unique()))
print("House mirror party values:", sorted(gen["party"].dropna().unique()))
print("House mirror years:", sorted(gen["year"].dropna().unique())[:3],
      "...", sorted(gen["year"].dropna().unique())[-3:])

def pick_winner(df):
    """Winner per district-year: prefer runoff rows when they exist."""
    winners = []
    for (year, state, dist), grp in df.groupby(["year", "state", "district"]):
        run = grp[grp["stage_norm"].str.contains("runoff")]
        pool = run if len(run) else grp[grp["stage_norm"] == "gen"]
        if len(pool) == 0:
            pool = grp
        top = pool.loc[pool["candidatevotes"].idxmax()]
        winners.append({"year": int(year), "state": state, "district": dist,
                        "winner_party": top["party"], "winner": top["candidate"]})
    return pd.DataFrame(winners)

house_win = pick_winner(gen)
house_win.to_csv(os.path.join(PROC, "house_winners.csv"), index=False)
DEM_SET = {"DEMOCRAT", "DEMOCRATIC", "DEMOCRATIC-FARMER-LABOR",
           "DEMOCRATIC-FARM-LABOR", "DEMOCRATIC-NPL",
           "DEMOCRATIC-NONPARTISAN LEAGUE"}
def _simple(party):
    p = str(party).strip().upper()
    if p in DEM_SET:
        return "D"
    if p == "REPUBLICAN":
        return "R"
    return "Other"
house_win["party_simple"] = house_win["winner_party"].map(_simple)
seats = house_win.groupby(["year", "party_simple"]).size().unstack(fill_value=0)
for col in ["D", "R", "Other"]:
    if col not in seats.columns:
        seats[col] = 0
seats = seats[["D", "R", "Other"]].reset_index()
seats.columns = ["year", "dem_seats", "rep_seats", "other_seats"]
seats.to_csv(os.path.join(PROC, "house_seats.csv"), index=False)
print("house_seats.csv:")
print(seats.to_string(index=False))

# -------------------------------------------------------------------- Senate
sen = pd.read_csv(os.path.join(RAW, "senate_1976_2024.tab"), sep="\t", low_memory=False)
sen["candidatevotes"] = pd.to_numeric(sen["candidatevotes"], errors="coerce")
sen["stage_norm"] = sen["stage"].astype(str).str.lower().str.strip()
sen_gen = sen[sen["stage_norm"].isin(["gen", "gen runoff", "runoff"])].copy()
sen_winners = []
for (year, state), grp in sen_gen.groupby(["year", "state"]):
    run = grp[grp["stage_norm"].str.contains("runoff")]
    pool = run if len(run) else grp
    top = pool.loc[pool["candidatevotes"].idxmax()]
    sen_winners.append({"year": int(year), "state": state,
                        "special": bool(top["special"]),
                        "winner": top["candidate"],
                        "winner_party": top["party_simplified"]})
sen_win = pd.DataFrame(sen_winners)
sen_win.to_csv(os.path.join(PROC, "senate_winners.csv"), index=False)
print("senate_winners.csv:", len(sen_win), "state-years")

# Senate party divisions, senate.gov/history/partydiv.htm (start of Congress).
sen_div = pd.DataFrame([
    (95, "1977-1979", 61, 38, 1, 0, "D"), (96, "1979-1981", 58, 41, 1, 0, "D"),
    (97, "1981-1983", 46, 53, 1, 0, "R"), (98, "1983-1985", 46, 54, 0, 0, "R"),
    (99, "1985-1987", 47, 53, 0, 0, "R"), (100, "1987-1989", 55, 45, 0, 0, "D"),
    (101, "1989-1991", 55, 45, 0, 0, "D"), (102, "1991-1993", 56, 44, 0, 0, "D"),
    (103, "1993-1995", 57, 43, 0, 0, "D"), (104, "1995-1997", 47, 53, 0, 0, "R"),
    (105, "1997-1999", 45, 55, 0, 0, "R"), (106, "1999-2001", 45, 55, 0, 0, "R"),
    (107, "2001-2003", 50, 50, 0, 0, "Split, then D"),
    (108, "2003-2005", 48, 51, 1, 0, "R"), (109, "2005-2007", 44, 55, 1, 0, "R"),
    (110, "2007-2009", 49, 49, 2, 0, "D (caucus)"),
    (111, "2009-2011", 56, 41, 2, 1, "D"), (112, "2011-2013", 51, 47, 2, 0, "D"),
    (113, "2013-2015", 53, 45, 2, 0, "D"), (114, "2015-2017", 44, 54, 2, 0, "R"),
    (115, "2017-2019", 46, 52, 2, 0, "R"), (116, "2019-2021", 45, 53, 2, 0, "R"),
    (117, "2021-2023", 48, 50, 2, 0, "D (VP tiebreak)"),
    (118, "2023-2025", 48, 49, 3, 0, "D (caucus)"),
    (119, "2025-2027", 45, 53, 2, 0, "R"),
], columns=["congress", "years", "dem", "rep", "other", "vacant", "majority"])
sen_div.to_csv(os.path.join(PROC, "senate_division.csv"), index=False)

# House party divisions, Wikipedia "Party divisions of United States
# Congresses" (compiles Clerk of the House data; snapshot per Congress).
house_div = pd.DataFrame([
    (95, "1977-1979", 292, 143, 0, 0, "D"), (96, "1979-1981", 277, 157, 1, 0, "D"),
    (97, "1981-1983", 242, 192, 1, 0, "D"), (98, "1983-1985", 269, 165, 1, 0, "D"),
    (99, "1985-1987", 253, 181, 1, 0, "D"), (100, "1987-1989", 258, 177, 0, 0, "D"),
    (101, "1989-1991", 260, 175, 0, 0, "D"), (102, "1991-1993", 267, 167, 1, 0, "D"),
    (103, "1993-1995", 258, 176, 1, 0, "D"), (104, "1995-1997", 204, 230, 1, 0, "R"),
    (105, "1997-1999", 206, 227, 2, 0, "R"), (106, "1999-2001", 211, 223, 1, 0, "R"),
    (107, "2001-2003", 212, 221, 2, 0, "R"), (108, "2003-2005", 205, 229, 1, 0, "R"),
    (109, "2005-2007", 202, 232, 1, 0, "R"), (110, "2007-2009", 233, 202, 0, 0, "D"),
    (111, "2009-2011", 257, 178, 0, 0, "D"), (112, "2011-2013", 193, 242, 0, 0, "R"),
    (113, "2013-2015", 201, 234, 0, 0, "R"), (114, "2015-2017", 188, 247, 0, 0, "R"),
    (115, "2017-2019", 194, 241, 0, 0, "R"), (116, "2019-2021", 235, 199, 1, 0, "D"),
    (117, "2021-2023", 222, 213, 0, 0, "D"), (118, "2023-2025", 212, 222, 0, 1, "R"),
    (119, "2025-2027", 215, 219, 0, 1, "R"),
], columns=["congress", "years", "dem", "rep", "other", "vacant", "majority"])
house_div.to_csv(os.path.join(PROC, "house_division.csv"), index=False)

# ------------------------------------------------------------- midterm table
# Presidents and their party at each midterm (1978 to 2022).
PRES = {1978: ("Jimmy Carter", "D"), 1982: ("Ronald Reagan", "R"),
        1986: ("Ronald Reagan", "R"), 1990: ("George H. W. Bush", "R"),
        1994: ("Bill Clinton", "D"), 1998: ("Bill Clinton", "D"),
        2002: ("George W. Bush", "R"), 2006: ("George W. Bush", "R"),
        2010: ("Barack Obama", "D"), 2014: ("Barack Obama", "D"),
        2018: ("Donald Trump", "R"), 2022: ("Joe Biden", "D")}
# Congress number for the Congress seated after a November election year.
# Election year Y seats the Congress that begins the following January.
def congress_after(election_year):
    return (election_year - 1788) // 2 + 1

house_idx = seats.set_index("year")
sen_idx = sen_div.set_index("congress")
house_div_idx = house_div.set_index("congress")
# House before/after use the official party-division table (Clerk of the
# House via Wikipedia), not the mirror aggregation, because the mirror
# misses 10 seats in 1996 and differs by up to 4 seats in 2010. The mirror
# file is kept as a cross-check (see house_seats.csv and BUILD_REPORT).
mid_rows = []
for year, (name, party) in sorted(PRES.items()):
    c_before = congress_after(year) - 1
    c_after = congress_after(year)
    h_col = "dem" if party == "D" else "rep"
    h_before = house_div_idx.loc[c_before, h_col]
    h_after = house_div_idx.loc[c_after, h_col]
    s_before = sen_idx.loc[c_before, "dem" if party == "D" else "rep"]
    s_after = sen_idx.loc[c_after, "dem" if party == "D" else "rep"]
    h_maj_before = house_div_idx.loc[c_before, "majority"]
    h_maj_after = house_div_idx.loc[c_after, "majority"]
    s_maj_before = sen_idx.loc[c_before, "majority"]
    s_maj_after = sen_idx.loc[c_after, "majority"]
    def is_unified(h_maj, s_maj, party):
        h_ok = h_maj.startswith(party)
        s_ok = s_maj.startswith(party) or (party == "D" and "D" in s_maj)
        return bool(h_ok and s_ok)
    mid_rows.append({
        "midterm_year": year, "president": name, "president_party": party,
        "house_before": int(h_before), "house_after": int(h_after),
        "house_change": int(h_after - h_before),
        "senate_before": int(s_before), "senate_after": int(s_after),
        "senate_change": int(s_after - s_before),
        "unified_before": is_unified(h_maj_before, s_maj_before, party),
        "unified_after": is_unified(h_maj_after, s_maj_after, party),
        "vep_turnout_pct": MIDTERM_VEP.get(year, float("nan")),
    })
mid = pd.DataFrame(mid_rows)
mid.to_csv(os.path.join(PROC, "midterm_history.csv"), index=False)
print(mid.to_string(index=False))

# ------------------------------------------------------- chapter 3 indicators
vetoes = pd.DataFrame([
    ("Jimmy Carter", 1977, 1981, 31, 13, 18, 2),
    ("Ronald Reagan", 1981, 1989, 78, 39, 39, 9),
    ("George H. W. Bush", 1989, 1993, 44, 29, 15, 1),
    ("Bill Clinton", 1993, 2001, 37, 36, 1, 2),
    ("George W. Bush", 2001, 2009, 12, 12, 0, 4),
    ("Barack Obama", 2009, 2017, 12, 12, 0, 1),
    ("Donald Trump (first term)", 2017, 2021, 10, 10, 0, 1),
    ("Joe Biden", 2021, 2025, 13, 13, 0, 0),
], columns=["president", "term_start", "term_end", "total_vetoes",
            "regular_vetoes", "pocket_vetoes", "overrides"])
vetoes.to_csv(os.path.join(PROC, "vetoes.csv"), index=False)

eos = pd.DataFrame([
    ("Jimmy Carter", 1977, 1981, 320), ("Ronald Reagan", 1981, 1989, 381),
    ("George H. W. Bush", 1989, 1993, 166), ("Bill Clinton", 1993, 2001, 364),
    ("George W. Bush", 2001, 2009, 291), ("Barack Obama", 2009, 2017, 276),
    ("Donald Trump (first term)", 2017, 2021, 220), ("Joe Biden", 2021, 2025, 162),
], columns=["president", "term_start", "term_end", "executive_orders"])
eos.to_csv(os.path.join(PROC, "executive_orders.csv"), index=False)

judges = pd.DataFrame([
    ("Jimmy Carter", 1977, 1981, 0, 56, 206, 262),
    ("Ronald Reagan", 1981, 1989, 4, 83, 296, 383),
    ("George H. W. Bush", 1989, 1993, 2, 42, 149, 193),
    ("Bill Clinton", 1993, 2001, 2, 66, 310, 378),
    ("George W. Bush", 2001, 2009, 2, 62, 263, 327),
    ("Barack Obama", 2009, 2017, 2, 55, 272, 329),
    ("Donald Trump (first term)", 2017, 2021, 3, 54, 174, 234),
    ("Joe Biden", 2021, 2025, 1, 45, 189, 235),
], columns=["president", "term_start", "term_end", "supreme_court",
            "circuit", "district", "total_article_iii"])
judges.to_csv(os.path.join(PROC, "judicial_confirmations.csv"), index=False)

shutdowns = pd.DataFrame([
    ("1995-11-13", "1995-11-19", 5, "Bill Clinton", "Republican House and Senate",
     "Budget and spending fight"),
    ("1995-12-15", "1996-01-06", 21, "Bill Clinton", "Republican House and Senate",
     "Budget, Medicare, and spending fight"),
    ("2013-10-01", "2013-10-16", 16, "Barack Obama", "Republican House, Democratic Senate",
     "Affordable Care Act funding fight"),
    ("2018-01-20", "2018-01-22", 3, "Donald Trump", "Republican House and Senate",
     "Immigration and spending fight"),
    ("2018-12-22", "2019-01-25", 35, "Donald Trump", "Republican Senate, Democratic House from Jan 2019",
     "Border wall funding fight"),
    ("2025-10-01", "2025-11-12", 43, "Donald Trump", "Republican House and Senate",
     "Spending and health care subsidy fight"),
], columns=["start", "end", "days", "president", "congress_control", "cause"])
shutdowns.to_csv(os.path.join(PROC, "shutdowns.csv"), index=False)

# ------------------------------------------------------------------ 2026 data
stakes = pd.DataFrame([
    ("House", 435, "Republican", 218, 214, 1, 2,
     "Democrats need a net gain of 4 seats to reach 218. Republicans can afford a net loss of 1 seat and still hold 218. The 1 independent, Kevin Kiley of California, caucuses with Republicans, giving a working Republican margin of 219 to 214."),
    ("Senate", 35, "Republican", 53, 45, 2, 0,
     "22 of the 35 seats up are held by Republicans, 13 by Democrats. Democrats need a net gain of 4 for a majority. Republicans need 19 of the 35 seats up to reach 50, which holds control because the Republican vice president breaks ties."),
    ("Governorships", 36, "Republican", 26, 24, 0, 0,
     "36 states elect a governor in 2026, 18 currently held by Republicans and 18 by Democrats. Nationally there are 26 Republican governors and 24 Democratic governors. 15 of the 36 incumbents are term-limited (6 Democrats, 9 Republicans)."),
], columns=["chamber", "seats_up", "current_majority", "rep_seats", "dem_seats",
            "other_seats", "vacant_seats", "notes"])
stakes.to_csv(os.path.join(PROC, "stakes_2026.csv"), index=False)

forecasts = pd.DataFrame([
    ("Cook Political Report (as reported Oct 30, 2026)", "2026-10-30", "House", 222, 195, 18,
     "Seats in Democratic categories, Republican categories, and toss-ups."),
    ("Cook Political Report (as reported Oct 23, 2026)", "2026-10-23", "House", 220, 198, 17, ""),
    ("Cook Political Report (as reported Oct 16, 2026)", "2026-10-16", "House", 214, 200, 21, ""),
    ("Cook Political Report (as reported Oct 9, 2026)", "2026-10-09", "House", 213, 201, 21, ""),
    ("Sabato's Crystal Ball (as reported Oct 8, 2026)", "2026-10-08", "House", 214, 219, 2,
     "Seats at least Lean Democratic, at least Lean Republican, and toss-ups."),
    ("Cook Political Report (as reported Oct 6, 2026)", "2026-10-06", "Senate", 47, 46, 7,
     "Seats in Democratic-aligned, Republican, and toss-up categories."),
], columns=["forecaster", "date", "chamber", "dem_category", "rep_category",
            "toss_ups", "notes"])
forecasts.to_csv(os.path.join(PROC, "forecasts_2026.csv"), index=False)

polls = pd.DataFrame([
    ("Silver Bulletin average", "2026-10-28", "Generic ballot", 51.0, 42.3, 8.7,
     "Lead reported as 8.7 points for Democrats; likely voter version 9.2 points."),
    ("RealClearPolling average", "2026-10-30", "Generic ballot", 52.0, 43.1, 8.9,
     "Through Oct 30, 2026, as reported in press coverage."),
    ("NBC News poll", "2026-10-30", "Generic ballot", 52.0, 45.0, 7.0,
     "Oct 28 to 30, 2026."),
    ("NPR/PBS News/Marist poll", "2026-10-20", "Generic ballot", 52.0, 44.0, 8.0,
     "Likely voters, Oct 19 to 20, 2026."),
    ("RealClearPolitics average", "2026-10-26", "Trump job approval", 38.4, 60.1, -21.7,
     "Approve 38.4 percent, disapprove 60.1 percent."),
    ("Silver Bulletin average", "2026-10-28", "Trump job approval", 37.4, 60.0, -22.6,
     "Approximate average, late October 2026."),
], columns=["source", "date", "measure", "dem_or_approve", "rep_or_disapprove",
            "lead", "notes"])
polls.to_csv(os.path.join(PROC, "polls_2026.csv"), index=False)

# -------------------------------------------------------------- verification
print("\n--- verification: MIT national totals vs published totals ---")
for year, pub_dem, pub_rep in [(2020, 81283501, 74223975), (2024, 75019230, 77303568)]:
    row = pres_nat[pres_nat["year"] == year].iloc[0]
    print(year, "MIT dem:", row["dem_votes"], "published dem:", pub_dem,
          "diff:", int(row["dem_votes"]) - pub_dem,
          "| MIT rep:", row["rep_votes"], "published rep:", pub_rep,
          "diff:", int(row["rep_votes"]) - pub_rep,
          "| MIT total votes for president:", row["total_votes"])
print("\n--- verification: House mirror seats vs division table ---")
merged = seats.merge(house_div[["congress", "years", "dem", "rep"]],
                     left_on=seats["year"].map(congress_after), right_on="congress",
                     how="left", suffixes=("_mirror", "_div"))
merged["d_diff"] = merged["dem_seats"] - merged["dem"]
merged["r_diff"] = merged["rep_seats"] - merged["rep"]
print(merged[["year", "dem_seats", "dem", "d_diff", "rep_seats", "rep", "r_diff"]].to_string(index=False))
print("\nDone. Files written to", PROC)
