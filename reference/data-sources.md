# Data Sources Atlas — What to Pull, From Where, How Fresh

Rule: rankings older than 48h (draft season) or same-day (in-season) are dead.
Always stamp pull date into the CSV/file name or header.

## Projections & rankings (draft + weekly)

| Source | What | Access |
|---|---|---|
| FantasyPros | Consensus rankings/projections (aggregates 100+ analysts), weekly start-sit, ADP | firecrawl scrape: fantasypros.com/nfl/rankings/<pos>.php, /projections/<pos>.php?week=; respects scoring param (PPR/HALF/STD) |
| Boris Chen | Tier clusters on FP consensus, updated daily in-season | borischen.co (per-scoring pages) |
| FFCalculator | Live mock/real ADP by format + team count | fantasyfootballcalculator.com/adp (has JSON API: /api/v1/adp/<format>?teams=N) |
| Sleeper API | Platform ADP (via draft picks), trending adds/drops, player meta/injury status | api.sleeper.app (open, no auth) |
| nflverse (GitHub) | Play-by-play, snap counts, depth charts, injuries — free CSVs | github.com/nflverse/nflverse-data releases |
| DynastyProcess | Free values/ecr CSVs on GitHub | github.com/dynastyprocess/data |
| FantasyCalc | Live trade values (redraft + dynasty), API | api.fantasycalc.com/values/current?isDynasty=false&ppr=... |
| KeepTradeCut | Dynasty/redraft crowd values | keeptradecut.com (scrape) |
| Subvertadown | DST/K streaming projections (best-in-class niche) | subvertadown.com |
| ESPN kona_player_info | ESPN's own projections (predicts casual-room behavior) | ESPN API view |

Paid (use only if user has subs — ask once, store in league settings):
Establish The Run, 4for4, FootballGuys, PFF, RotoViz.

## News & injuries (freshness critical)

- WebSearch: "<player> injury news" restricted to last 24–72h; prefer beat
  writers and official team reports over aggregators.
- nflverse injuries CSV (official report designations: DNP/LP/FP).
- Sleeper `/players/nfl` injury_status field (fast-updating).
- Sunday inactives: ~90 min pre-kickoff, WebSearch "week N inactives".

## Vegas / matchup context

- Game totals + spreads: WebSearch "nfl week N odds" or scrape
  vegasinsider/actionnetwork via firecrawl. Implied team total = total/2 ±
  spread/2. Start players on teams implied 24+; fade implied <17.
- Pace/pass-rate + defensive splits vs position: fantasypros points-allowed
  pages, nflverse pbp aggregates.

## Weather

WebSearch "week N nfl weather" (nflweather.com). Only wind ≥20mph and
snow/monsoon matter. Dome games: ATL, DAL, DET, HOU, IND, LV, LA(2), MIN, NO,
ARI(retractable), and cold-weather December outdoor games for kickers.

## Community signal (contrarian + consensus checks)

- Sleeper trending adds (crowd waiver wisdom, quantified).
- r/fantasyfootball daily threads via WebSearch/firecrawl — sentiment only,
  never as a primary source.
- `yt-research` skill for "week N sleepers/rankings" video sweeps ONLY when
  doing deep prep (draft weekend), not weekly.

## Standard pull recipes

**Draft-prep pull (spawn 3 parallel agents):**
1. Projections agent → FantasyPros projections per position for the league's
   exact scoring → normalize to `draft/projections.csv`
   (columns: player,pos,team,bye,proj_pts,adp).
2. ADP agent → platform-native ADP + FFCalculator for the format/size → merge.
3. News agent → last-72h injury/depth-chart changes for top-150 → flags column.

**Weekly pull (2 agents):** weekly projections + start-sit consensus; Vegas +
weather + inactives.

Cache policy: `players` DBs cache 24h; everything else re-pull per use.
