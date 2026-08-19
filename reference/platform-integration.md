# Platform Integration — Auth, APIs, Browser Control

Credential file: `~/Personal/fantasy-football/.env` (chmod-equivalent private;
never committed, never echoed). Source it in the same Bash call that uses it.

## Sleeper (best-in-class: open read API, no auth)

Base: `https://api.sleeper.app/v1`
- User: `/user/<username>` → user_id
- Leagues: `/user/<user_id>/leagues/nfl/2026`
- League/settings: `/league/<league_id>` (scoring_settings, roster_positions)
- Rosters: `/league/<league_id>/rosters`; Users: `/league/<league_id>/users`
- Matchups: `/league/<league_id>/matchups/<week>`
- Drafts: `/league/<league_id>/drafts` → `/draft/<draft_id>/picks` (poll this
  during live drafts — cleaner than screen-scraping; still keep browser open
  for pick submission)
- Players DB (5MB, cache 1×/day): `/players/nfl`
- Trending: `/players/nfl/trending/add?limit=50` (waiver crowd-wisdom)

Writes (pick submission, waivers) have no public API → browser via Playwright.
`.env`: `SLEEPER_USERNAME=`, `SLEEPER_LEAGUE_ID=`.

## ESPN (cookie auth for private leagues)

Read API base:
`https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2026/segments/0/leagues/<LEAGUE_ID>`
Views (append `?view=`): `mSettings` (scoring/roster/waiver rules), `mTeam`,
`mRoster`, `mMatchup`, `mDraftDetail`, `kona_player_info` (projections).

Private leagues need cookies `espn_s2` + `SWID`:
1. User logs into espn.com in Chrome; via Chrome DevTools MCP or Playwright,
   read cookies for `.espn.com` (`evaluate_script`/`browser_run_code_unsafe` →
   document.cookie won't expose HttpOnly espn_s2 — use the MCP network request
   headers or ask user to copy from DevTools → Application → Cookies).
2. Store as `ESPN_S2=` and `ESPN_SWID={...}` in `.env`.
3. curl with `-H "Cookie: espn_s2=$ESPN_S2; SWID=$ESPN_SWID"`.
espn_s2 lasts ~1 year. If 401 → re-capture.

Draft room + lineup writes: browser only.

## Yahoo

OAuth2 (client id/secret from developer.yahoo.com → app with Fantasy Sports
read/write). Token dance is heavy; for most needs, browser automation on
football.fantasysports.yahoo.com is faster to stand up. If user wants the API:
base `https://fantasysports.yahooapis.com/fantasy/v2`, resources
`league/<key>/settings|standings|scoreboard`, `team/<key>/roster`. Store
`YAHOO_CLIENT_ID/SECRET/REFRESH_TOKEN` in `.env`.

## NFL.com / CBS / MFL

Browser automation only (Playwright MCP). MFL has a real API
(`api.myfantasyleague.com/2026/export?TYPE=...`) if user is there.

## Browser control rules

- Prefer Playwright MCP (`browser_navigate`, `browser_snapshot`,
  `browser_click`, `browser_wait_for`); Chrome DevTools MCP is the fallback
  when attaching to the user's existing logged-in Chrome profile.
- Login flow: navigate → let USER type the password themselves when possible
  (2FA/CAPTCHA); persist the session, don't re-login every run.
- Never screenshot or log pages showing the password field with typed input.
- Snapshot-parse, act, verify: after any click that submits (pick, claim,
  lineup save) re-snapshot and confirm the state changed before reporting done.

## `setup` flow

1. Ask platform + league ID/URL (AskUserQuestion if interactive).
2. Pull league settings via API (Sleeper/ESPN) or browser scrape → write
   `league-settings.json` (template: templates/league-settings.template.json).
3. Verify creds work end-to-end (one authenticated read).
4. Run `league-audit` automatically after settings land.
