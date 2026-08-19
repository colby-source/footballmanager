# In-Season Operations — Waivers, Lineups, Trades, Playoff Push

The draft is ~40% of a title. The other 60% is won Tuesday-to-Sunday, every
week, by the manager who processes fresh information fastest. Weekly cadence:

| Day | Op |
|---|---|
| Mon night | Review MNF, log week result + lessons to `season-log.md` |
| Tue | **Waivers**: targets + FAAB bids before processing |
| Wed–Thu | Trade offers out (post-waiver rosters are known), injury reports open |
| Fri | Injury designations drop → preliminary lineup |
| Sat | Final news sweep; lock non-Sunday players |
| Sun AM | Inactives (~90 min before kickoff) → final start-sit; late-swap plan |

## Waivers / FAAB (`waivers`)

Every Tuesday, pull fresh: Sleeper trending adds, snap counts, target/carry
shares from last week (WebSearch/firecrawl), injury fallout. Rank claims by
**league-winner probability**, not points next week.

FAAB bid sizing (of remaining budget):
- League-winning RB handcuff promoted to starter: 40–70% (bid what it takes;
  these decide titles)
- Clear new starter, medium ceiling: 15–25%
- Streamer/matchup play: 1–5%
- Speculative stash: $0–2
Rules: never bid round numbers ($21 beats the $20 crowd), track every rival's
remaining FAAB in `opponent-profiles.md`, never drop to $0 before week 10
unless it's a true league-winner, and in rolling-priority leagues hold #1–3
priority for bell-cow promotions only.

Drop discipline: drop by rest-of-season value, not name value; check the
dropped player can't be instantly claimed by the rival who needs him most —
if he can, trade him for scraps instead of dropping.

## Start-sit (`lineup`)

Inputs, fresh every time: consensus weekly projections + expert start-sit
(FantasyPros weekly), Vegas lines (game total + implied team total — start
players in games totaling 47+, fade 6-pt underdogs' RBs), weather (wind >20mph
kills passing/kicking, rain is overrated), practice reports (LP/DNP patterns),
snap/route trends over last 3 weeks (not season averages).

Rules:
1. Studs start. Rounds 1–3 picks sit only for injury or bye — never matchup.
2. For coin-flips: favored-when-needed → if you're the better team this week,
   take floor; if underdog, take ceiling. Check opponent's likely score first.
3. Late-swap leverage: if you have Sunday-night/Monday players and the
   opponent is done, compute exactly what you need and pick floor/ceiling
   accordingly.
4. Never start a "questionable" player in the early window with a bench gap —
   game-time-decision players go in late-window slots when possible.

## Streaming

- **DST**: pick against turnover-prone/backup QBs and bottom-5 implied totals;
  2 weeks ahead, grab next week's elite stream Friday before the crowd.
- **QB (1QB leagues)**: stream vs bottom-10 pass defenses at home; rushing
  floor breaks ties.
- **TE/K**: pure matchup + red-zone share. Zero loyalty.

## Trades (`trade`)

Valuation: rest-of-season projections re-run through the VBD engine + a market
check (FantasyCalc live trade values; KeepTradeCut for dynasty). Then apply:
- **Buy-low windows**: talented players after 2–3 bad games with intact
  role/volume (volume is real, efficiency reverts); injured stars in week 4–8
  from panicking managers; good offenses with bad early schedules.
- **Sell-high windows**: TD-dependent overperformers (TD rate >1 per 12
  touches reverts), aging RBs after big games, anyone whose snap share is
  quietly declining, your surplus depth 2 weeks before the trade deadline.
- **2-for-1 rule**: the side getting the best player wins most trades; as a
  contender consolidate, as a longshot diversify.
- Package to THEIR hole (from opponent-profiles), open with a fair-plus offer
  (lowballs poison future talks), and never accept pending-trade risk across
  a waiver run.

## Injury response

Starter goes down mid-game: before the game ends, know the handcuff and have
the FAAB number ready; claims spike within the hour on daily-waiver leagues.
Your starter out: check YOUR handcuff first, then waivers, then trade for the
rival's bench redundancy.

## Playoff push (`playoffs`)

From week 10:
- Compute playoff odds + seeding scenarios (PF tiebreaker!) each week.
- Trade deadline: contenders trade bench depth for one stud; also acquire your
  playoff-week SCHEDULE — check weeks 15–17 opponents' defenses now.
- Roster-block: last bench spot on the handcuff your likely playoff opponent
  needs.
- Week 14 (if locked into seed): rest injured studs, do NOT tank PF if
  seeding tiebreaks are live.
- Championship weeks: weather report is mandatory (December), never get cute —
  studs + ceiling.

## Learning loop

Every decision logged to `season-log.md`: what, why, outcome. Monthly: review
misses — was the process wrong or the variance? Only change process for
process errors. Update `## My manager profile` on every user correction.
