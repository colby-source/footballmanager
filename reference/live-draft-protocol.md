# Live Draft Protocol — Real-Time Copilot

Goal: a recommendation on the user's screen within 20 seconds of every pick,
with zero missed picks. Speed beats depth; the board was built in prep, the
draft is execution.

## T-24h checklist (must all be green before draft)

- [ ] `draft/projections.csv` pulled fresh (<48h old) and re-pulled morning-of
- [ ] `draft_engine.py` run clean → `draft/board.csv` (tiers + VBD + ADP edge)
- [ ] `draft/plan.md`: primary archetype, pivot, round-by-round targets, and
      a "panic list" (safe picks per round if the clock hits 10s)
- [ ] Injury/news sweep for anyone in the top 120 (WebSearch, last 72h)
- [ ] Platform login verified in the browser (Playwright attach test)
- [ ] Pick clock length and autopick behavior confirmed from league settings

## Attach

1. `browser_navigate` to the draft room URL (user logs in beforehand or creds
   from `.env`; see platform-integration.md).
2. `browser_snapshot` → identify: pick ticker/board region, on-the-clock
   indicator, user's queue, chat (ignore).
3. Verify user's team name and draft slot against `league-settings.json`.

## Per-pick loop (runs until draft complete)

```
1. SNAPSHOT   browser_snapshot (or wait_for pick-change text)
2. DIFF       extract new picks since last loop → append to draft/drafted.txt
3. ENGINE     python draft_engine.py --settings ... --projections ...
              --drafted drafted.txt --mine "<my picks>" --top 8
4. CONTEXT    check: tier deaths pending? position run live? what do the
              managers between me and my next pick need?
5. OUTPUT     if my pick is ≤2 away: post recommendation NOW —
              "PICK: <player> — <one-line reason>. Fallback: <player2>.
               If both gone: <player3>."
              else: one-line board state ("QB run started; your WR t2 targets
              safe for 6 more picks").
6. SUBMIT     on user confirm (or auto-pick mode): click player → confirm.
              Verify pick registered on next snapshot before trusting it.
```

Loop cadence: snapshot every ~15–20s during others' picks (fast rooms) or on
each `browser_wait_for` pick-change; NEVER block > one pick interval. Do not
delegate this loop to a subagent — latency kills.

## Clock discipline

- 90s+ clocks: full loop each pick.
- 30–60s clocks: pre-compute at pick-minus-2; when on the clock only re-check
  that the target wasn't just sniped.
- <30s or user AFK risk: get explicit "auto-pick from your board" consent
  BEFORE the draft; then submit top engine pick automatically and announce it.
- Clock at 10s with no confirmation: post the panic-list pick loudly; submit
  only if auto-pick consent was granted.

## Failure modes

| Failure | Response |
|---|---|
| Snapshot can't parse picks | Screenshot fallback (`take_screenshot`, read image); if still blind, ask user to paste last picks — keep the engine loop alive on manual input |
| Browser dies mid-draft | Re-attach via navigate; picks are recoverable from the room's pick history tab |
| Engine errors | Recommend straight from `board.csv` (it's already tiered) — never go silent |
| User's target sniped 1 pick ahead | Next player in same tier; if tier died, best VBD at needed position. No tilt reaches |
| Platform autopicked for user | Log it, re-plan around it, tell them how to disable autopick |

## During-draft intel capture

Log to `opponent-profiles.md` as the draft runs: who reaches, who follows ADP
robotically, who panic-drafts QBs, who ignores their roster holes. This is
week 1–17 trade ammunition.

## Post-draft (immediately after last pick)

1. Final roster → `roster.json`.
2. Grade every team (starter VBD sum + bench upside) → post league power
   rankings to the user with their biggest hole.
3. Waiver plan v1: best undrafted per position + the handcuffs to their RBs
   that went undrafted.
4. Log archetype adherence + notable deviations to `season-log.md`.
