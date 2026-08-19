# Valuation Engine — VBD, Tiers, Scarcity, Arbitrage

The core insight of every award-winning drafter: **a player's value is not his
points — it's his points above what a replacement at his position scores.**
A 350-pt QB in a 1-QB league is worth less than a 220-pt RB, because QB12
scores 320 and RB24 scores 140.

## 1. Replacement level (compute from ACTUAL league settings)

Replacement rank per position = (starters required × teams) + share of flex +
a bench-usage buffer:

```
QB:  teams × QB_slots            (+ teams if superflex)     + 2
RB:  teams × RB_slots            + teams × flex_share_RB    + 4
WR:  teams × WR_slots            + teams × flex_share_WR    + 4
TE:  teams × TE_slots            + 1
K/DST: teams × slots             (streamable — replacement ≈ starter)
```

Flex share defaults: PPR → RB 45% / WR 50% / TE 5%. Standard → RB 60% / WR 38%.
Superflex: QB replacement moves from ~QB14 to ~QB26 — QBs become first-round
picks. **This is the #1 setting people misdraft.**

## 2. VBD

`VBD = projected_points − replacement_points(position)`

Draft by VBD, not by raw points and not by position dogma. But VBD is a
baseline, not a bible — adjust for:

- **Uncertainty**: projections have position-dependent error. RB projections
  miss worst (injury + committee risk). Discount RB VBD ~8–10% for fragile
  profiles (age 27+, 300+ prior-season touches, new O-line), boost proven
  target hogs.
- **Ceiling vs floor**: in 12+ team leagues you need ceiling to win, not
  median. Prefer the higher-variance player when VBDs are within ~5%. In
  shallow (8–10 team) leagues floor matters more — replacement is strong.
- **Playoff weeks**: weight weeks 15–17 matchups/schedule ~15% in rounds 1–6
  ties. Championships are won in December.

## 3. Tiers (this is what you actually draft from)

Sort each position by projection; a tier break = gap > ~6% of the tier mean
(draft_engine.py does this). Draft rule: **when you're on the clock, ask which
position's current tier is about to die.** If 5 WRs remain in WR tier 3 but
only 1 RB in RB tier 2, take the RB even if a WR has marginally higher VBD —
you can get tier-3 WR next pick, you can't get tier-2 RB.

Cross-check tiers against Boris Chen (borischen.co — clustering on FantasyPros
consensus, updated daily in season) but rebuild from fresh projections; never
use his generic scoring if the league has quirks.

## 4. ADP arbitrage

`edge = ADP_rank − your_board_rank`. Positive edge = market discount.

- Never pick a player 2+ rounds before ADP ("he won't make it back" is how
  fish drown) — exception: your board says top-of-tier and the tier dies
  before your next pick.
- Build a **targets list**: every player your board ranks ≥12 spots above ADP.
  These are who you queue in the mid/late rounds.
- ADP source must match the platform (Sleeper ADP for Sleeper drafts, ESPN
  for ESPN) — room behavior follows the platform's default ranks. Casual ESPN
  rooms follow ESPN default rankings almost mechanically: you can predict the
  next 10 picks from that list.

## 5. Snake-pick math

Value of pick n and pick (2T+1−n) round-trip is roughly constant, but talent
cliffs aren't linear. From the turn (picks 1.12/2.01 style), you draft in
pairs — plan pairs, not picks. Middle slots (5–8) get best flexibility.
When offered pick trades: use a VBD-based pick value curve (steep through
~pick 25, flattens after pick 60). Two picks in rounds 6–8 ≈ one pick in
round 3 in value, but roster-spot cost matters in shallow benches.

## 6. Auction conversion

`$value = (player_VBD / Σ league_draftable_VBD) × (total_budget × teams − $1 × roster_spots × teams) + $1`

Auction rules: nominate players you DON'T want early (drain budgets), price-
enforce stars to 90% of value, save $ for the mid-auction dead zone where
values crater, always leave $1 more than max remaining bids you plan.

## 7. Data recency ladder

1. Season-long projections: FantasyPros consensus (aggregates 100+ analysts),
   cross-check with a sharp single source (4for4 / Establish The Run if user
   has subs).
2. ADP: platform-native first, FFCalculator + FantasyPros as tiebreak.
3. News within 72h of draft: beat writers via WebSearch, Sleeper trending
   adds (`/players/nfl/trending/add`) as a wisdom-of-crowds signal.

Full source atlas: data-sources.md.
