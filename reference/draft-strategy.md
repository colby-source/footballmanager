# Draft Strategy — Archetypes, Slot Plans, Format Adjustments

Strategy is chosen AFTER the league audit, never before. The format dictates
the archetype; the archetype dictates the plan; the room dictates the pivots.

## Archetypes (pick one primary + one pivot)

| Archetype | Shape | When it wins | When to avoid |
|---|---|---|---|
| **Hero RB** | 1 elite RB rd 1, then WR/TE flood until rd 6+, RB dart throws late | Half-PPR/PPR 12-team; balanced default; the modern consensus play | Superflex (QBs eat rds 1–2) |
| **Zero RB** | WR/WR/WR/TE(elite) first 4–5; RBs = volume darts + handcuffs rounds 6+ | Full PPR, big benches, active waivers (you'll hit the RB lottery in-season) | Standard scoring, shallow bench, lazy-waiver leagues |
| **Robust RB** | RB/RB (maybe RB/RB/RB) to start; WR value later | Standard/half-PPR, 8–10 teams (WR replacement is strong), homogeneous WR-heavy rooms | Full PPR 12+ teams |
| **Late-round QB** | Ignore QB until rounds 9+; stream if needed | 1-QB any size — QB replacement is always high | Superflex/2QB (NEVER late-QB there) |
| **Elite TE** | Top-2 TE in rounds 1–3 for weekly positional +6–8 pt edge | TE-premium scoring, or when the tier-1 TE falls past cost | If the elite tier is gone, punt TE to rd 10+, stream |

Default recommendation absent other info: **Hero RB + late-round QB + punt K/DST
to the last two rounds.** Kickers/DSTs before the final 2 rounds are donated
value — streaming beats drafting at both positions.

## Format multipliers (from league-audit)

- **Superflex/2QB**: QBs are RB1s. Take 2 QBs in the first 4 rounds, a third
  by round 10. This overrides everything.
- **TE premium (+0.5–1.0 PPR to TE)**: elite TEs jump 1–2 rounds; the streaming
  floor also rises — mid TEs become startable.
- **Points-per-first-down**: boosts grinder RBs and possession WRs vs air-yard
  deep threats.
- **Big-play bonuses (40+ yd TD etc.)**: boosts field-stretchers and boom
  RBs; variance is your friend at the pick, so lean ceiling.
- **6-pt passing TD**: compresses QB scarcity even more — go later at QB.
- **Deep rosters / IR slots**: stash injured discounts (players out weeks 1–6)
  and rookie lottery tickets.

## Slot plans (12-team snake)

- **Picks 1–3**: take the consensus top back/WR, then you're at the 24/25 turn
  — plan pairs. Usually best-WR + best-RB available; avoid double-same-position
  unless a tier cliff forces it.
- **Picks 4–8**: most flexible. Let the board come to you; this is where Hero
  RB is cleanest.
- **Picks 9–12**: turn drafting. Pairs at 12/13 and 36/37. Zero RB and
  double-WR starts play well here; reach a half-round on tier-enders because
  the wheel is 23 picks away.

## Room-reading (live adjustments)

- **Run detection**: 3 same-position picks in the last 5 → the room is running.
  Never chase a run mid-panic; take the value the run is leaving behind, and
  START runs at scarce positions when you own the turn.
- **Next-picker modeling**: before your pick, check the 2–4 rosters picking
  between you and your next pick. If none of them need a TE, your TE target
  survives — take the RB instead. draft_engine.py `--top 8` output plus their
  roster needs answers this in seconds.
- **ESPN casual rooms** follow the default ESPN rank list; **Sleeper rooms**
  skew sharper and RB-frugal; **Yahoo** rooms over-draft QBs. Calibrate ADP
  trust accordingly.

## Rules of discipline

1. Draft from YOUR tiered board, not from memory or vibes.
2. Bye weeks are a tiebreaker only — never pass value for a bye.
3. Handcuffs: only cuff YOUR fragile elite RB (and only if the cuff is a
   true standalone-if-starter-goes-down back); never cuff other people's RBs
   before round 12.
4. Rookies: pay for opportunity (draft capital + depth chart), not highlight
   reels. Fresh beat-writer camp news within 72h of the draft is mandatory.
5. Last 2 picks: K + DST (best week-1 matchup DST, not best "season" DST).
   If the league starts neither, take two more lottery darts.
6. Never leave the draft without: 5+ RB/WR bench darts ranked by your board,
   your week-1 lineup startable, and no roster hole that waivers can't fix.

## Mock protocol (`mock` subcommand)

Simulate opponents picking by platform ADP + positional-need nudge; user picks
from engine recommendations. Run 2–3 mocks from the user's real slot before
draft day; log which archetype produced the strongest roster (sum of starter
VBD + bench upside score) into `draft/plan.md`.
