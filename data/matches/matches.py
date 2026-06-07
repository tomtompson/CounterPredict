from __future__ import annotations

import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.teams import HLTVTeamResults


TEAMS_FILE = PROJECT_ROOT / "data" / "teams" / "top_50_teams.csv"
OUTPUT_FILE = Path(__file__).with_name("top_50_team_matches.csv")
MATCH_LIMIT_PER_TEAM = 50

FIELDNAMES = [
    "match_id",
    "team_1_id",
    "team_1",
    "team_score",
    "team_2_id",
    "team_2",
    "team2_score",
    "team_1_winner",
    "match_date",
    "event_name",
]


def load_teams(teams_file: Path = TEAMS_FILE) -> list[dict]:
    with teams_file.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader if row.get("id")]


def load_team_ids(teams_file: Path = TEAMS_FILE) -> list[str]:
    return [row["id"] for row in load_teams(teams_file)]


def load_team_name_to_id(teams_file: Path = TEAMS_FILE) -> dict[str, str]:
    return {
        row["team_name"]: row["id"]
        for row in load_teams(teams_file)
        if row.get("team_name") and row.get("id")
    }


def fetch_unique_matches(
    team_ids: list[str],
    team_name_to_id: dict[str, str],
) -> list[dict]:
    matches_by_id: dict[int, dict] = {}
    team_names = set(team_name_to_id.keys())

    for team_id in team_ids:
        service = HLTVTeamResults(team_id=team_id)
        results = service.get_team_results().get("results", [])
        accepted_matches = 0

        for match in results:
            if accepted_matches >= MATCH_LIMIT_PER_TEAM:
                break

            team_1 = match.get("team1_name")
            team_2 = match.get("team2_name")

            # Only keep matches where both teams are in your top_50_teams.csv
            if team_1 not in team_names or team_2 not in team_names:
                continue

            match_id = match.get("match_id")
            if match_id is None or match_id in matches_by_id:
                continue

            team1_score = match.get("team1_score") or 0
            team2_score = match.get("team2_score") or 0

            matches_by_id[match_id] = {
                "match_id": match_id,
                "team_1_id": team_name_to_id.get(team_1),
                "team_1": team_1,
                "team_score": team1_score,
                "team_2_id": team_name_to_id.get(team_2),
                "team_2": team_2,
                "team2_score": team2_score,
                "team_1_winner": team1_score > team2_score,
                "match_date": match.get("match_date"),
                "event_name": match.get("event_name"),
            }

            accepted_matches += 1

    return list(matches_by_id.values())


def write_csv(rows: list[dict], output_file: Path = OUTPUT_FILE) -> Path:
    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    return output_file


def main() -> None:
    team_ids = load_team_ids()
    team_name_to_id = load_team_name_to_id()

    rows = fetch_unique_matches(team_ids, team_name_to_id)
    output_file = write_csv(rows)

    print(f"saved {len(rows)} unique matches to {output_file}")


if __name__ == "__main__":
    main()