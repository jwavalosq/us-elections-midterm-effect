# Data provenance

Every raw file used by this project, where it came from, and what was
done with it. Accessed November 2, 2026, unless noted otherwise.

## Downloaded files

### president_1976_2024.csv (514,108 bytes)

MIT Election Data and Science Lab, Harvard Dataverse, DOI
10.7910/DVN/42MVDX, file ID 13887042, license CC0 1.0. State level
presidential votes, 1976 to 2024. Columns include year, state, candidate,
party_detailed, party_simplified, candidatevotes, totalvotes.

Used for: national popular vote totals by party, state margins, swing
state counts, and the wrong winner check (2000 and 2016).

Verification: MIT national totals differ from published candidate totals
by under 0.1 percent (2020: Democrat gap -14,593 votes, Republican gap
-7,829 votes; 2024: Democrat gap -1,617 votes, Republican gap -988
votes). The gaps come from write in handling and certification vintages.
The analysis uses MIT totals consistently.

### senate_1976_2024.tab (632,787 bytes, 3,945 rows)

MIT Election Data and Science Lab, Harvard Dataverse, DOI
10.7910/DVN/PEJ5QU, file ID 13887039, license CC0 1.0. State level Senate
votes, 1976 to 2024, including special elections and runoffs.

Used for: Senate race winners by state and year (senate_winners.csv).
Chamber totals come from the Senate party division table below, not from
this file, because the file has no winner flag and runoff timing
complicates aggregation.

### house_1976_2024_mirror.csv (4,229,898 bytes, 33,805 rows)

Mirror of the MIT House file, from the keithpotz/Election-Prediction
GitHub repository, path src/data/polling_data/house_1976_2024.csv.
The MIT House file itself (Harvard Dataverse DOI 10.7910/DVN/IG0UN2,
file ID 13592823) could not be downloaded directly because the Dataverse
API refused the request with a guestbook response requirement (guestbook
ID 458). The partially saved error file (122 bytes) was deleted.

Quirk: every data line in the mirror is wrapped in double quotes, and
candidate names carry backslash escaped quotes and commas. Normal CSV
parsing fails on it. The build script therefore parses it by position:
fields 0 to 10 are fixed, the candidate is everything between field 11
and the last 8 fields, and the last 8 fields are fixed. Only the
candidate field can contain commas or quotes.

Used for: House seat counts by election (house_seats.csv) as a cross
check. The midterm series itself uses the official party division table
below, because the mirror misses 10 Texas districts in 1996 (a court
ordered redistricting moved those races into a special process the
mirror codes separately) and differs by up to 4 seats in 2010. Mirror vs
division table gaps are 0 to 4 seats in all other years.

## Hand verified tables (entered in scripts/build_processed.py)

### Senate party divisions

Source: senate.gov, history party divisions page
(senate.gov/history/partydiv.htm). Start of Congress counts, 95th to
119th Congress. Used for Senate before and after every midterm.

### House party divisions

Source: Wikipedia, "Party divisions of United States Congresses", which
compiles Clerk of the House data. Snapshot per Congress, 95th to 119th.
Used for House before and after every midterm. The House Clerk's own
party division page returned HTTP 403 during the build and was not
retried.

Note on the 119th Congress: the division table snapshot shows 215
Democrats, 219 Republicans, 1 vacant. The current composition used in
chapter 04 (218 seated Republicans, 214 seated Democrats, 1 independent,
2 vacant, as of November 2, 2026) comes from House trackers and reflects
later vacancies and the independent member. The two snapshots differ
because they are taken at different dates.

### Electoral College votes

Source: Federal Election Commission, official presidential general
election results, 1976 to 2024. Totals: 1976 Carter 297, Ford 240, 1
faithless; 1980 Reagan 489, Carter 49; 1984 Reagan 525, Mondale 13; 1988
Bush 426, Dukakis 111, 1 faithless; 1992 Clinton 370, Bush 168; 1996
Clinton 379, Dole 159; 2000 Bush 271, Gore 266, 1 abstention; 2004 Bush
286, Kerry 251, 1 faithless; 2008 Obama 365, McCain 173; 2012 Obama 332,
Romney 206; 2016 Trump 304, Clinton 227, 7 faithless; 2020 Biden 306,
Trump 232; 2024 Trump 312, Harris 226.

### Turnout

Source: University of Florida Election Lab (Michael McDonald), voting
eligible population turnout, via Wikipedia, "Voter turnout in United
States presidential elections". Presidential: 1980 58.49, 1984 55.25,
1988 52.76, 1992 58.22, 1996 51.73, 2000 54.24, 2004 60.13, 2008 61.60,
2012 58.05, 2016 59.18, 2020 65.28, 2024 64.30 (provisional estimate,
March 2, 2026). Midterm: 2014 36.7, 2018 50.1, 2022 46.1 (Election Lab
version 1.4 series). Vintage note: other versions of the 2020 series
report 65.99 or 66.4 percent. This project uses one series (the Wikipedia
table values) consistently and does not mix vintages.

### Presidential vetoes

Source: American Presidency Project, presidential vetoes table, data
through January 8, 2026. Totals (regular plus pocket, overrides in
parentheses): Carter 31 (2), Reagan 78 (9), George H. W. Bush 44 (1),
Clinton 37 (2), George W. Bush 12 (4), Obama 12 (1), Trump first term 10
(1), Biden 13 (0). Trump second term: 2 so far in the 119th Congress,
not charted as a final total.

### Executive orders

Source: Federal Register disposition tables, via Competitive Enterprise
Institute tables. Totals: Carter 320, Reagan 381, George H. W. Bush 166,
Clinton 364, George W. Bush 291, Obama 276, Trump first term 220, Biden
162 (77 in 2021, 29 in 2022, 24 in 2023, 19 in 2024, 13 in 2025). Trump
second term: about 130 or more through May 2026, provisional only, not
charted as a final total.

### Judicial confirmations

Source: Wikipedia, list of presidents by judicial appointments, Article
III judges only (Supreme Court, circuit, district). Totals: Carter 262,
Reagan 383, George H. W. Bush 193, Clinton 378, George W. Bush 327,
Obama 329, Trump first term 234, Biden 235. Counting rule note:
Ballotpedia counts differ (for example Reagan 402, Clinton 387) because
it includes some specialty courts. This project uses the Wikipedia
Article III list consistently. Trump second term: 34 confirmed as of
late March 2026, not charted as a final total.

### Federal shutdowns

Source: Congressional Research Service based lists of major shutdowns.
Episodes: November 13 to 19, 1995, 5 days, Clinton; December 15, 1995 to
January 6, 1996, 21 days, Clinton; October 1 to 16, 2013, 16 days, Obama;
January 20 to 22, 2018, 3 days, Trump first term; December 22, 2018 to
January 25, 2019, 35 days, Trump first term; October 1 to November 12,
2025, 43 days, Trump second term. The February 9, 2018 lapse (under 1
day) is noted in chapter 03 but not charted as a full day shutdown. The
December 2018 to January 2019 shutdown is commonly reported as 35 days;
CRS counts 34 full days without budget authority. This project uses 35,
the commonly reported figure, and says so.

## November 2026 stakes and forecasts

### Current composition, as of November 2, 2026

House: 218 seated Republicans, 214 seated Democrats, 1 independent
(Kevin Kiley of California, left the Republican Party in 2026, caucuses
with Republicans), 2 vacant. Working margin 219 to 214. Majority 218.
Senate: 53 Republicans, 45 Democrats, 2 independents caucusing with
Democrats, reported as 53 to 47. Majority 51, or 50 plus the vice
president (JD Vance, Republican). Senate seats up: 35 (33 Class II plus
special elections in Florida and Ohio). Republicans hold 22 of the 35,
Democrats hold 13. Governorships up: 36 (18 Republican held, 18
Democratic held). Nationally: 26 Republican governors, 24 Democratic
governors. Term limited incumbents among the 36: 15 (6 Democrats, 9
Republicans), per Ballotpedia reporting of October 28, 2026.

### Forecasts (all labeled as forecasts, not results)

Cook Political Report House ratings, as reported October 30, 2026:
222 Democratic categories, 195 Republican categories, 18 toss-ups.
Earlier Cook House snapshots: October 23, 2026: 220, 198, 17; October 16,
2026: 214, 200, 21; October 9, 2026: 213, 201, 21. Cook Senate ratings, as
reported October 6, 2026: 47 Democratic aligned, 46 Republican, 7
toss-ups. Sabato's Crystal Ball House ratings, as reported October 8,
2026: 214 at least Lean Democratic, 219 at least Lean Republican, 2
toss-ups. Attribution caution: Cook and Sabato ratings are paywalled at
the source, so these numbers come from secondary reports of those
ratings and are attributed that way in the notebooks.

Governor toss-ups: sources conflict (one summary reports 5 Cook
toss-ups, another reports 3). No single governor toss-up number is
presented.

### Polls (context, not predictions)

Silver Bulletin generic ballot average, October 28, 2026: Democrats
ahead by 8.7 points (likely voter version 9.2 points). RealClearPolling
average through October 30, 2026: Democrats 52.0 percent, Republicans
43.1 percent. NBC News poll, October 28 to 30, 2026: Democrats 52
percent, Republicans 45 percent. NPR/PBS News/Marist poll, October 19
to 20, 2026, likely voters: Democrats 52 percent, Republicans 44
percent. Trump job approval, RealClearPolitics average, October 26,
2026: 38.4 percent approve, 60.1 percent disapprove. Early voting: about
51 million early ballots cast as of November 2, 2026, per a tracker
covering 47 states.

## What was not used

- The House Clerk's own party division page: HTTP 403, not retried.
- Bills enacted (public laws) per Congress: no clean verified table was
  secured. Cut, and documented in BUILD_REPORT.md.
- Any November 2026 result: none exists as of November 2, 2026, and none
  is presented.
