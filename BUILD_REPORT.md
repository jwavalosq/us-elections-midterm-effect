# Build report

Project: US Elections: The Midterm Effect.
Built: November 2, 2026 (local build only, nothing published, pushed,
posted, or signed into).
Folder: ~/workspace/us-elections-midterm-effect/

## What was delivered

- 6 Jupyter notebooks in `notebooks/`, each with a top pip install cell,
  each executed end to end with zero cell errors, using the `us-elections`
  kernel (project virtual environment, Python 3.12, pandas, matplotlib,
  nbconvert, ipykernel).
- 19 charts in `charts/` (requirement was at least 10).
- 16 processed CSVs in `data/processed/`.
- `README.md`, this file, `requirements.txt`, `.gitignore`,
  `data/raw/PROVENANCE.md`, `scripts/build_processed.py`,
  `scripts/build_notebooks.py`, `scripts/download_data.py`.

## Files used

Raw inputs (see `data/raw/PROVENANCE.md` for full details):

- `data/raw/president_1976_2024.csv`, MIT Election Lab, 514,108 bytes.
- `data/raw/senate_1976_2024.tab`, MIT Election Lab, 632,787 bytes,
  3,945 rows.
- `data/raw/house_1976_2024_mirror.csv`, keithpotz mirror, 4,229,898
  bytes, 33,805 rows.

Processed outputs:

- `presidential_national.csv` (13 elections), `presidential_state.csv`
  (663 state-years), `swing_states.csv` (13 rows).
- `house_winners.csv`, `house_seats.csv` (mirror cross check),
  `house_division.csv`, `senate_winners.csv` (841 state-years),
  `senate_division.csv`.
- `midterm_history.csv` (12 midterms, 1978 to 2022).
- `vetoes.csv`, `executive_orders.csv`, `judicial_confirmations.csv`,
  `shutdowns.csv`.
- `stakes_2026.csv`, `forecasts_2026.csv`, `polls_2026.csv`.

Charts (19): c01_popular_share, c01_popular_margin, c01_ev_vs_pop,
c01_turnout, c01_swing_states, c02_house_change, c02_senate_change,
c02_house_seats_time, c02_senate_seats_time, c03_vetoes,
c03_executive_orders, c03_judges, c03_shutdowns, c04_house_now,
c04_senate_up, c04_governors, c04_cook_house, c04_cook_senate,
c05_history_vs_2026.

## What ran

1. `scripts/build_processed.py` ran clean and printed verification
   output (MIT vs published gaps, mirror vs division table gaps,
   wrong winner check).
2. `scripts/build_notebooks.py` generated 6 notebooks (13, 16, 13, 13,
   17, and 5 cells).
3. `jupyter nbconvert --execute --inplace` ran all 6 notebooks with the
   `us-elections` kernel. Error scan after execution: zero cell errors
   in all 6 notebooks.
4. A final grep for the em-dash character across all project files
   (excluding the virtual environment) returned zero matches.

## What failed or was approximated

1. **MIT House file download blocked.** The Dataverse API refused
   file 13592823 with a guestbook response requirement. The partially
   saved 122 byte error file was deleted. Fallback used: the
   keithpotz/Election-Prediction mirror, verified against the official
   party division table (see next item).
2. **House mirror parsing.** The mirror wraps every data line in double
   quotes with backslash escaped inner quotes, which breaks normal CSV
   parsing. The build script parses it by position instead. Only the
   candidate field can contain commas or quotes, so the parse is safe
   for seat counts.
3. **House mirror gaps.** Mirror seat counts differ from the official
   division table by 0 to 4 seats in most years, by 9 Republican seats
   in 1996, and by 4 seats in 2010. The 1996 gap is fully explained: the
   mirror holds only 20 of 30 Texas districts in 1996, because a court
   ordered redistricting moved 10 Texas races into a special process
   the mirror codes separately. Consequence: the midterm series uses
   the official division table, not the mirror. The mirror file is kept
   as a cross check.
4. **House Clerk page blocked.** clerk.house.gov/member_info/partyDiv.aspx
   returned HTTP 403. It was not retried. The Wikipedia party divisions
   table (which compiles Clerk data) was used instead for House seats.
5. **MIT totals vs published totals.** MIT national totals differ from
   published candidate totals by under 0.1 percent (2020 Democrat
   -14,593 votes, Republican -7,829 votes; 2024 Democrat -1,617 votes,
   Republican -988 votes). Cause: write in handling and certification
   vintages. The analysis uses MIT totals consistently.
6. **2020 turnout vintage.** The Wikipedia table gives 65.28 percent
   for 2020, its state table implies 65.99 percent, and another
   University of Florida series gives 66.4 percent. The project uses
   65.28 percent (the Wikipedia table value) consistently and does not
   mix vintages. The 2024 figure (64.30 percent) is a provisional
   University of Florida estimate dated March 2, 2026, and is labeled
   as provisional.
7. **Forecast attribution.** Cook and Sabato ratings are paywalled at
   the source. All Cook and Sabato numbers in this project come from
   secondary reports of those ratings and are attributed that way, with
   dates, in the notebooks. They are never presented as directly
   observed Cook or Sabato pages.
8. **Governor toss-ups.** Sources conflict (5 vs 3 Cook toss-ups). No
   single governor toss-up number is presented.
9. **Shutdown day count.** The December 2018 to January 2019 shutdown is
   charted as 35 days (the commonly reported figure). CRS counts 34
   full days without budget authority. The difference is noted in the
   provenance file.
10. **February 2018 lapse.** The February 9, 2018 funding lapse lasted
    under 1 day. It is mentioned in chapter 03 but not charted as a
    full day shutdown.
11. **Trump second term indicators.** Vetoes (2 so far), executive
    orders (about 130 or more through May 2026, provisional), and
    judicial confirmations (34 as of late March 2026) are in progress.
    They are noted in text and excluded from the completed term charts.

## What was cut, and why

1. **Bills enacted (public laws) per Congress.** Planned as the
   cleanest measure of legislative output for chapter 03. No clean,
   verified per Congress table was secured during the build. Cut rather
   than guessed. Chapter 03 uses vetoes, executive orders,
   confirmations, and shutdowns instead, and names the cut.
2. **House seat map.** No map is included. A map would need district
   shapefiles and would add little to the seat count story. The
   project never fakes a map.
3. **District level 2026 race ratings.** Chapter 04 presents aggregate
   forecast categories (for example, 18 House toss-ups) rather than a
   district by district list, because individual race ratings change
   frequently and the aggregate is what the secondary reports verified.
4. **Governor toss-up count.** Cut for the reason in item 8 above.
5. **A single 2026 prediction.** Cut by design. The project presents
   scenarios neutrally and labels the results section as pending.

## What could not be verified

- The exact Cook and Sabato rating pages (paywalled; secondary reports
  used instead, attributed as such).
- The current House composition snapshot beyond November 2, 2026
  trackers (218 Republicans seated, 214 Democrats seated, 1 independent,
  2 vacant). Later vacancies or special election results would change
  these numbers.
- Whether the 2026 Senate toss-up races named in some secondary
  summaries match Cook's own list (the project therefore reports the
  count, 7, not a definitive race list).

## Em-dash check

The em-dash character is banned from this project. Every project file
was checked before finishing. Result: zero matches (excluding the
virtual environment directory, which is not project content).
