# footballmanager — repo guide

Claude Code skill: fantasy football general manager (draft prep, live-draft
copilot, in-season ops). Canonical install location is
`~/.claude/skills/footballmanager/`; this repo is the source of truth —
sync changes here first, then copy to the skills dir.

## Stack
- Markdown skill files (SKILL.md + reference/*)
- Python 3.12, stdlib only (`scripts/draft_engine.py`) — no dependencies

## Conventions
- SKILL.md stays lean (orchestration); depth lives in reference/ files
- No league data, credentials, or personal state in this repo — league state
  lives at `~/Personal/fantasy-football/<league-slug>/`, creds in that
  folder's `.env`
- Engine stays stdlib-only and immutable-style (build new structures, never
  mutate inputs)

## Validation
```
python scripts/draft_engine.py --settings templates/league-settings.template.json --projections <sample.csv>
```
(no lint/build step; test the engine against a small sample CSV before commit)

## Sync to live skill
```
cp -r ./* ~/.claude/skills/footballmanager/
```
