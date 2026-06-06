from __future__ import annotations

import csv
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.teams import HLTVTeamSearch


OUTPUT_FILE = Path(__file__).with_name("top_5_teams.csv")
HLTV_LOOKUP_LIMIT = 20
VALVE_OUTPUT_LIMIT = 5
FIELDNAMES = [
    "team_name",
    "id",
    "hltv_placement",
    "hltv_points",
    "valve_placement",
    "valve_points",
]


def fetch_top_teams(limit: int = 50) -> list[dict]:
    hltv_ranking = HLTVTeamSearch(
        top_n=max(limit, HLTV_LOOKUP_LIMIT),
        ranking_type="hltv",
    ).get_hltv_teams()
    valve_ranking = HLTVTeamSearch(top_n=limit, ranking_type="valve").get_world_ranking_teams()
    hltv_by_id = {
        str(team["id"]): {
            "hltv_placement": team["placement"],
            "hltv_points": team["hltv_points"],
        }
        for team in hltv_ranking
    }

    rows = []

    for team in valve_ranking:
        team_id = str(team["id"])
        hltv_team = hltv_by_id.get(team_id, {})

        rows.append(
            {
                "team_name": team["name"],
                "id": team_id,
                "hltv_placement": hltv_team.get("hltv_placement"),
                "hltv_points": hltv_team.get("hltv_points"),
                "valve_placement": team["placement"],
                "valve_points": team["valve_points"],
            },
        )

    return rows


def write_csv(rows: list[dict], output_file: Path = OUTPUT_FILE) -> Path:
    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    return output_file


def main() -> None:
    rows = fetch_top_teams(limit=VALVE_OUTPUT_LIMIT)
    output_file = write_csv(rows)
    print(f"saved {len(rows)} teams to {output_file}")


if __name__ == "__main__":
    main()
