# footballmanager

A Claude Code skill that acts as a full-season fantasy football general manager:
league rules audit, fresh-data draft prep (VBD + tiers + ADP arbitrage), a
real-time live-draft copilot that attaches to your draft room via browser MCP,
and in-season operations (waivers, start-sit, streaming, trades, playoff push).

## What it does

- **League audit** — parses your league's full rulebook and finds the scoring
  and roster quirks the other managers ignore
- **Draft prep** — pulls fresh multi-source projections + platform-native ADP
  at runtime (never stale data), blends them into a consensus, and builds a
  tiered value-based draft board with a round-by-round plan
- **Live draft copilot** — attaches to the draft room (Playwright MCP), tracks
  every pick, and recommends pick + reason + fallback before you're on the clock
- **In-season ops** — weekly waiver targets, FAAB/priority bid sizing,
  start-sit with Vegas/weather/inactives, trade construction, playoff
  optimization
- **Opponent profiling** — reads draft behavior and transaction history to
  predict and exploit the other managers

Platforms: Sleeper (open API), ESPN (cookie auth), Yahoo (browser), NFL/MFL/CBS
(browser).

## Install

Copy this repo into your Claude Code skills directory:

```
git clone https://github.com/colby-source/footballmanager ~/.claude/skills/footballmanager
```

Then in any Claude Code session: `/footballmanager setup`

## Layout

```
SKILL.md                    # orchestrator: subcommands, state layout, rules
reference/
  valuation-engine.md       # VBD math, replacement levels, tiers, auction $
  draft-strategy.md         # archetypes, slot plans, format multipliers
  live-draft-protocol.md    # the per-pick loop, clock discipline, failure modes
  platform-integration.md   # Sleeper/ESPN/Yahoo auth + API endpoints
  league-exploitation.md    # rules-audit checklist, opponent profiling
  in-season-ops.md          # waivers, streaming, trades, playoff push
  data-sources.md           # projections/ADP/news source atlas + pull recipes
scripts/draft_engine.py     # stdlib-only VBD/tier/best-available engine
templates/league-settings.template.json
```

## Engine usage

```
python scripts/draft_engine.py --settings league-settings.json \
  --projections projections.csv [--drafted drafted.txt] \
  [--mine "Player A,Player B"] [--top 8] [--out board.csv]
```

`projections.csv` columns: `player,pos,team,bye,proj_pts,adp` (bye/adp optional).

## Principles

1. Never draft from stale rankings — all projections/ADP/news are fetched fresh
   at runtime
2. League state and credentials live outside the skill (in `~/Personal/`),
   never in this repo
3. The user confirms every pick/claim submission unless auto-pick consent is
   explicitly given
4. No guarantees — this maximizes expected value and process quality; variance
   is real

## License

MIT
