#!/usr/bin/env python3
"""footballmanager draft engine: VBD, tiers, ADP arbitrage, live best-available.

Stdlib only. Immutable-style: builds new structures, never mutates inputs.

Usage:
  python draft_engine.py --settings league-settings.json --projections proj.csv
      [--drafted drafted.txt] [--mine "Player A,Player B"] [--top 8]
      [--out board.csv]

projections.csv columns (header required, case-insensitive):
  player,pos,team,bye,proj_pts,adp        (bye/adp optional)
drafted.txt: one player name per line (names matched case/space-insensitively).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from typing import NamedTuple

FLEX_SHARE_PPR = {"RB": 0.45, "WR": 0.50, "TE": 0.05}
FLEX_SHARE_STD = {"RB": 0.60, "WR": 0.38, "TE": 0.02}
TIER_GAP_FRAC = 0.06  # gap > 6% of tier mean starts a new tier
POSITIONS = ("QB", "RB", "WR", "TE", "K", "DST")


class Player(NamedTuple):
    name: str
    pos: str
    team: str
    bye: str
    proj: float
    adp: float | None


def norm(name: str) -> str:
    return " ".join(name.lower().replace(".", "").replace("'", "").split())


def load_settings(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        s = json.load(f)
    for key in ("teams", "roster", "scoring"):
        if key not in s:
            sys.exit(f"settings missing required key: {key}")
    return s


def load_projections(path: str) -> list[Player]:
    players: list[Player] = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            sys.exit("projections csv has no header")
        cols = {c.lower().strip(): c for c in reader.fieldnames}
        for req in ("player", "pos", "proj_pts"):
            if req not in cols:
                sys.exit(f"projections csv missing column: {req}")
        for i, row in enumerate(reader, start=2):
            try:
                pos = row[cols["pos"]].upper().strip()
                pos = {"DEF": "DST", "D/ST": "DST", "PK": "K"}.get(pos, pos)
                if pos not in POSITIONS:
                    continue
                adp_raw = row.get(cols.get("adp", ""), "") if "adp" in cols else ""
                players.append(Player(
                    name=row[cols["player"]].strip(),
                    pos=pos,
                    team=(row.get(cols.get("team", ""), "") or "").strip() if "team" in cols else "",
                    bye=(row.get(cols.get("bye", ""), "") or "").strip() if "bye" in cols else "",
                    proj=float(row[cols["proj_pts"]]),
                    adp=float(adp_raw) if adp_raw not in ("", None) else None,
                ))
            except (ValueError, KeyError) as e:
                print(f"warn: skipping row {i}: {e}", file=sys.stderr)
    if not players:
        sys.exit("no valid players parsed from projections")
    return players


def replacement_ranks(settings: dict) -> dict[str, int]:
    teams = int(settings["teams"])
    r = settings["roster"]
    ppr = float(settings.get("scoring", {}).get("ppr", 0.5))
    share = FLEX_SHARE_PPR if ppr >= 0.5 else FLEX_SHARE_STD
    flex = int(r.get("FLEX", 0))
    sflex = int(r.get("SUPERFLEX", 0))
    ranks = {
        "QB": teams * (int(r.get("QB", 1)) + sflex) + 2,
        "RB": round(teams * (int(r.get("RB", 2)) + flex * share["RB"])) + 4,
        "WR": round(teams * (int(r.get("WR", 2)) + flex * share["WR"])) + 4,
        "TE": round(teams * (int(r.get("TE", 1)) + flex * share["TE"])) + 1,
        "K": teams * int(r.get("K", 1)),
        "DST": teams * int(r.get("DST", 1)),
    }
    return {p: max(1, n) for p, n in ranks.items()}


def compute_board(players: list[Player], settings: dict) -> list[dict]:
    """Returns rows sorted by VBD desc, with tier + adp_edge per player."""
    repl = replacement_ranks(settings)
    by_pos = {p: sorted((x for x in players if x.pos == p),
                        key=lambda x: -x.proj) for p in POSITIONS}
    repl_pts = {
        p: (lst[min(repl[p], len(lst)) - 1].proj if lst else 0.0)
        for p, lst in by_pos.items()
    }
    rows: list[dict] = []
    for pos, lst in by_pos.items():
        tier, prev = 1, None
        tier_projs: list[float] = []
        for rank, pl in enumerate(lst, start=1):
            if prev is not None and tier_projs:
                mean = sum(tier_projs) / len(tier_projs)
                if mean > 0 and (prev - pl.proj) > TIER_GAP_FRAC * mean:
                    tier += 1
                    tier_projs = []
            tier_projs.append(pl.proj)
            prev = pl.proj
            rows.append({
                "player": pl.name, "pos": pos, "team": pl.team, "bye": pl.bye,
                "proj": round(pl.proj, 1), "pos_rank": rank, "tier": tier,
                "vbd": round(pl.proj - repl_pts[pos], 1),
                "adp": pl.adp,
            })
    rows.sort(key=lambda r: -r["vbd"])
    for i, r in enumerate(rows, start=1):
        r["board_rank"] = i
        r["adp_edge"] = round(r["adp"] - i, 1) if r["adp"] is not None else None
    return rows


def roster_needs(settings: dict, mine: list[dict]) -> dict[str, float]:
    """Need multiplier per position: unfilled starters > flex depth > luxury."""
    r = settings["roster"]
    counts = {p: sum(1 for m in mine if m["pos"] == p) for p in POSITIONS}
    needs: dict[str, float] = {}
    for p in POSITIONS:
        starters = int(r.get(p, 0)) + (int(r.get("SUPERFLEX", 0)) if p == "QB" else 0)
        if counts[p] < starters:
            needs[p] = 1.15
        elif p in ("RB", "WR") and counts[p] < starters + int(r.get("FLEX", 0)) + 2:
            needs[p] = 1.0
        elif p in ("K", "DST"):
            needs[p] = 0.2 if counts[p] >= max(1, starters) else 0.6
        else:
            needs[p] = 0.85
    return needs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--settings", required=True)
    ap.add_argument("--projections", required=True)
    ap.add_argument("--drafted", help="file: one drafted player name per line")
    ap.add_argument("--mine", default="", help="comma-separated: my drafted players")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--out", help="write full board csv here")
    args = ap.parse_args()

    settings = load_settings(args.settings)
    board = compute_board(load_projections(args.projections), settings)

    drafted: set[str] = set()
    if args.drafted:
        with open(args.drafted, encoding="utf-8") as f:
            drafted = {norm(line) for line in f if line.strip()}
    mine_names = {norm(n) for n in args.mine.split(",") if n.strip()}
    mine = [r for r in board if norm(r["player"]) in mine_names]
    taken = drafted | mine_names
    avail = [r for r in board if norm(r["player"]) not in taken]

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(board[0].keys()))
            w.writeheader()
            w.writerows(board)
        print(f"board written: {args.out} ({len(board)} players)")

    needs = roster_needs(settings, mine)
    scored = sorted(avail, key=lambda r: -(r["vbd"] * needs[r["pos"]]))

    print(f"\n=== BEST AVAILABLE (need-adjusted) | drafted={len(taken)} ===")
    print(f"{'#':>3} {'PLAYER':<24} {'POS':<4} {'TIER':>4} {'PROJ':>6} "
          f"{'VBD':>6} {'ADP':>6} {'EDGE':>6}")
    for r in scored[:args.top]:
        adp = f"{r['adp']:.0f}" if r["adp"] is not None else "-"
        edge = f"{r['adp_edge']:+.0f}" if r["adp_edge"] is not None else "-"
        print(f"{r['board_rank']:>3} {r['player']:<24} {r['pos']:<4} "
              f"{r['tier']:>4} {r['proj']:>6} {r['vbd']:>6} {adp:>6} {edge:>6}")

    print("\n=== TIER PRESSURE (players left in current top tier) ===")
    for pos in POSITIONS:
        pos_avail = [r for r in avail if r["pos"] == pos]
        if not pos_avail:
            continue
        top_tier = pos_avail[0]["tier"]
        left = sum(1 for r in pos_avail if r["tier"] == top_tier)
        print(f"  {pos:<4} tier {top_tier}: {left} left "
              f"(next: {pos_avail[0]['player']})")

    if mine:
        print(f"\n=== MY ROSTER ({len(mine)}) ===")
        for r in sorted(mine, key=lambda x: x["board_rank"]):
            print(f"  {r['pos']:<4} {r['player']} (tier {r['tier']}, bye {r['bye'] or '-'})")


if __name__ == "__main__":
    main()
