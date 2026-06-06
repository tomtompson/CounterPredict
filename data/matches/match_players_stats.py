from __future__ import annotations

import csv
import sys
from pathlib import Path

from fastapi import HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.matches import HLTVMatchPastPlayersStats


MATCHES_FILE_CANDIDATES = (
    PROJECT_ROOT / "data" / "matches" / "top_5_team_matches.csv",
    PROJECT_ROOT / "data" / "matches" / "top_5_team_matches.csv",
)
OUTPUT_FILE = Path(__file__).with_name("top_5_team_match_player_stats.csv")
ROLE_SECTIONS = (
    "firepower",
    "entrying",
    "trading",
    "opening",
    "clutching",
    "sniping",
    "utility",
)
BASE_FIELDNAMES = [
    "match_id",
    "match_date",
    "event_name",
    "team_1",
    "team_2",
    "player_id",
    "player_name",
]


def resolve_matches_file() -> Path:
    for candidate in MATCHES_FILE_CANDIDATES:
        if candidate.exists():
            return candidate

    searched_paths = ", ".join(str(path) for path in MATCHES_FILE_CANDIDATES)
    raise FileNotFoundError(f"could not find matches csv; looked for: {searched_paths}")


def load_matches(matches_file: Path | None = None) -> list[dict]:
    resolved_file = matches_file or resolve_matches_file()
    with resolved_file.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader if row.get("match_id")]


def flatten_player_stats(match_row: dict, player_row: dict) -> dict:
    stats = player_row.get("stats") or {}
    summary = stats.get("summary") or {}
    roles = stats.get("roles") or {}

    flattened = {
        "match_id": match_row.get("match_id"),
        "match_date": match_row.get("match_date"),
        "event_name": match_row.get("event_name"),
        "team_1": match_row.get("team_1"),
        "team_2": match_row.get("team_2"),
        "player_id": player_row.get("id"),
        "player_name": player_row.get("name"),
    }

    flattened.update(summary)

    for role_name in ROLE_SECTIONS:
        role_data = roles.get(role_name) or {}
        combined = role_data.get("combined") or {}
        flattened[f"{role_name}_combined_score"] = combined.get("score")

    return flattened


def fetch_match_player_stats(matches: list[dict]) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    summary_keys: set[str] = set()

    for match in matches:
        match_id_raw = match.get("match_id")
        if not match_id_raw:
            continue

        try:
            service = HLTVMatchPastPlayersStats(match_id=int(match_id_raw))
            response = service.get_past_players_stats()
        except HTTPException as exc:
            print(f"skipping match {match_id_raw}: {exc.detail}")
            continue

        players = response.get("players", [])

        for player in players:
            row = flatten_player_stats(match, player)
            summary_keys.update(
                key
                for key in row
                if key not in BASE_FIELDNAMES
                and not key.endswith("_combined_score")
            )
            rows.append(row)

    fieldnames = (
        BASE_FIELDNAMES
        + sorted(summary_keys)
        + [f"{role_name}_combined_score" for role_name in ROLE_SECTIONS]
    )
    return rows, fieldnames


def write_csv(
    rows: list[dict],
    fieldnames: list[str],
    output_file: Path = OUTPUT_FILE,
) -> Path:
    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_file


def main() -> None:
    matches = load_matches()
    rows, fieldnames = fetch_match_player_stats(matches)
    output_file = write_csv(rows, fieldnames)
    print(f"saved {len(rows)} player stats rows to {output_file}")


if __name__ == "__main__":
    main()
