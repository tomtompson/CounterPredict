from __future__ import annotations

import csv
import os
import sys
from pathlib import Path
from typing import Iterable
import json
from calendar import monthrange
from datetime import datetime

from fastapi import HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.matches import HLTVMatchPastPlayersStats


MATCHES_FILE_CANDIDATES = (
    PROJECT_ROOT / "data" / "matches" / "top_50_team_matches.csv",
    PROJECT_ROOT / "data" / "matches" / "top_50_team_matches.csv",
)

OUTPUT_FILE = Path(__file__).with_name("top_50_team_match_player_stats.csv")
FAILED_FILE = Path(__file__).with_name("failed_match_player_stats.csv")

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
    "team_1_id",
    "team_1",
    "team_2_id",
    "team_2",
    "player_team_id",
    "player_team_name",
    "player_id",
    "player_name",
]

SUMMARY_FIELDNAMES = [
    "rating_3_0",
    "rating_3_0_t_rating",
    "rating_3_0_ct_rating",
    "round_swing",
    "dpr",
    "kast",
    "multi_kill",
    "adr",
    "kpr",
]


ROLE_FIELDNAMES = [
    f"{role_name}_combined_score"
    for role_name in ROLE_SECTIONS
]

FIELDNAMES = BASE_FIELDNAMES + SUMMARY_FIELDNAMES + ROLE_FIELDNAMES

FAILED_FIELDNAMES = [
    "match_id",
    "match_date",
    "event_name",
    "team_1_id",
    "team_1",
    "team_2_id",
    "team_2",
    "error",
]

class IncompleteMatchError(Exception):
    """Raised when a match does not return all 10 player rows."""

class CachedHLTVMatchPastPlayersStats(HLTVMatchPastPlayersStats):
    CACHE_DIR = PROJECT_ROOT / "data" / "matches" / "cache" / "player_stats"
    CACHE_ENABLED = True
    CACHE_MONTH_RANGE = 2

    @staticmethod
    def get_stats_date_range(match_date: str) -> tuple[str, str]:
        end_date = datetime.strptime(match_date, "%Y-%m-%d")
        month = end_date.month - 3
        year = end_date.year

        while month <= 0:
            month += 12
            year -= 1

        day = min(end_date.day, monthrange(year, month)[1])
        start_date = end_date.replace(year=year, month=month, day=day)

        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    @staticmethod
    def add_months(date: datetime, months: int) -> datetime:
        month = date.month + months
        year = date.year

        while month > 12:
            month -= 12
            year += 1

        while month <= 0:
            month += 12
            year -= 1

        day = min(date.day, monthrange(year, month)[1])
        return date.replace(year=year, month=month, day=day)

    def get_cache_file(self, player_id: str, year_month: str) -> Path:
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        return self.CACHE_DIR / f"{player_id}_{year_month}.json"

    def find_cache_file(
        self,
        player_id: str,
        match_date: str,
    ) -> Path | None:
        match_dt = datetime.strptime(match_date, "%Y-%m-%d")

        for offset in range(0, self.CACHE_MONTH_RANGE + 1):
            offsets = [offset] if offset == 0 else [offset, -offset]

            for month_offset in offsets:
                candidate_dt = self.add_months(match_dt, month_offset)
                year_month = candidate_dt.strftime("%Y-%m")
                cache_file = self.get_cache_file(player_id, year_month)

                if cache_file.exists():
                    return cache_file

        return None

    def get_write_cache_file(
        self,
        player_id: str,
        match_date: str,
    ) -> Path:
        match_dt = datetime.strptime(match_date, "%Y-%m-%d")
        year_month = match_dt.strftime("%Y-%m")
        return self.get_cache_file(player_id, year_month)

    def get_player_stats(
        self,
        player_id: str,
        player_name: str,
        match_date: str,
    ) -> dict:
        if self.CACHE_ENABLED:
            cache_file = self.find_cache_file(
                player_id=player_id,
                match_date=match_date,
            )

            if cache_file is not None:
                try:
                    with cache_file.open("r", encoding="utf-8") as file:
                        self.logger.info(
                            f"monthly cache hit for player {player_id}: {cache_file}",
                        )
                        return json.load(file)
                except Exception as exc:
                    self.logger.warning(f"failed to read cache {cache_file}: {exc}")

        stats = super().get_player_stats(
            player_id=player_id,
            player_name=player_name,
            match_date=match_date,
        )

        if self.CACHE_ENABLED:
            cache_file = self.get_write_cache_file(
                player_id=player_id,
                match_date=match_date,
            )
            temp_file = cache_file.with_suffix(".tmp")

            try:
                with temp_file.open("w", encoding="utf-8") as file:
                    json.dump(stats, file, ensure_ascii=False)

                temp_file.replace(cache_file)

                self.logger.info(
                    f"saved monthly cache for player {player_id}: {cache_file}",
                )
            except Exception as exc:
                self.logger.warning(f"failed to write cache {cache_file}: {exc}")

        return stats


def resolve_matches_file() -> Path:
    for candidate in MATCHES_FILE_CANDIDATES:
        if candidate.exists():
            return candidate

    searched_paths = ", ".join(str(path) for path in MATCHES_FILE_CANDIDATES)
    raise FileNotFoundError(f"could not find matches csv; looked for: {searched_paths}")


def iter_matches(matches_file: Path | None = None) -> Iterable[dict]:
    resolved_file = matches_file or resolve_matches_file()

    with resolved_file.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        seen_match_ids: set[str] = set()

        for row in reader:
            match_id = row.get("match_id")

            if not match_id:
                continue

            if match_id in seen_match_ids:
                continue

            seen_match_ids.add(match_id)
            yield row


def load_completed_match_ids(output_file: Path = OUTPUT_FILE) -> set[str]:
    if not output_file.exists():
        return set()

    completed_match_ids: set[str] = set()

    with output_file.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            match_id = row.get("match_id")
            if match_id:
                completed_match_ids.add(match_id)

    return completed_match_ids


def load_failed_match_ids(failed_file: Path = FAILED_FILE) -> set[str]:
    if not failed_file.exists():
        return set()

    failed_match_ids: set[str] = set()

    with failed_file.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            match_id = row.get("match_id")
            if match_id:
                failed_match_ids.add(match_id)

    return failed_match_ids


def get_player_team_name(player_row: dict) -> str | None:
    return (
        player_row.get("team_name")
        or player_row.get("team")
        or player_row.get("teamName")
    )


def get_player_team_id(match_row: dict, player_team_name: str | None) -> str | None:
    if not player_team_name:
        return None

    if player_team_name == match_row.get("team_1"):
        return match_row.get("team_1_id")

    if player_team_name == match_row.get("team_2"):
        return match_row.get("team_2_id")

    return None


def flatten_player_stats(match_row: dict, player_row: dict, player_index: int) -> dict:
    stats = player_row.get("stats") or {}
    summary = stats.get("summary") or {}
    roles = stats.get("roles") or {}

    if player_index < 5:
        player_team_id = match_row.get("team_2_id")
        player_team_name = match_row.get("team_2")
    else:
        player_team_id = match_row.get("team_1_id")
        player_team_name = match_row.get("team_1")

    flattened = {
        "match_id": match_row.get("match_id"),
        "match_date": match_row.get("match_date"),
        "event_name": match_row.get("event_name"),
        "team_1_id": match_row.get("team_1_id"),
        "team_1": match_row.get("team_1"),
        "team_2_id": match_row.get("team_2_id"),
        "team_2": match_row.get("team_2"),
        "player_team_id": player_team_id,
        "player_team_name": player_team_name,
        "player_id": player_row.get("id"),
        "player_name": player_row.get("name"),
    }

    flattened.update(summary)

    for role_name in ROLE_SECTIONS:
        role_data = roles.get(role_name) or {}
        combined = role_data.get("combined") or {}
        flattened[f"{role_name}_combined_score"] = combined.get("score")

    return flattened


def fetch_single_match_player_stats(match: dict) -> list[dict]:
    match_id_raw = match.get("match_id")

    if not match_id_raw:
        return []

    service = CachedHLTVMatchPastPlayersStats(match_id=int(match_id_raw))
    response = service.get_past_players_stats()
    players = response.get("players", [])

    if len(players) != 10:
        raise IncompleteMatchError(
            f"expected 10 players, got {len(players)}"
        )

    return [
        flatten_player_stats(match, player, index)
        for index, player in enumerate(players)
    ]

def append_rows(rows: list[dict], output_file: Path = OUTPUT_FILE) -> None:
    file_has_content = output_file.exists() and output_file.stat().st_size > 0

    with output_file.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=FIELDNAMES,
            extrasaction="ignore",
        )

        if not file_has_content:
            writer.writeheader()

        writer.writerows(rows)
        csv_file.flush()
        os.fsync(csv_file.fileno())


def append_failed_match(
    match: dict,
    error: str,
    failed_file: Path = FAILED_FILE,
) -> None:
    file_has_content = failed_file.exists() and failed_file.stat().st_size > 0

    with failed_file.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FAILED_FIELDNAMES)

        if not file_has_content:
            writer.writeheader()

        writer.writerow(
            {
                "match_id": match.get("match_id"),
                "match_date": match.get("match_date"),
                "event_name": match.get("event_name"),
                "team_1_id": match.get("team_1_id"),
                "team_1": match.get("team_1"),
                "team_2_id": match.get("team_2_id"),
                "team_2": match.get("team_2"),
                "error": error,
            }
        )

        csv_file.flush()
        os.fsync(csv_file.fileno())


def main() -> None:
    completed_match_ids = load_completed_match_ids()
    failed_match_ids = load_failed_match_ids()

    total_player_rows = 0
    processed_matches = 0
    skipped_completed = 0
    skipped_failed = 0
    newly_failed = 0

    for match in iter_matches():
        match_id = str(match.get("match_id"))

        if match_id in completed_match_ids:
            skipped_completed += 1
            continue

        if match_id in failed_match_ids:
            skipped_failed += 1
            continue

        try:
            rows = fetch_single_match_player_stats(match)
        except HTTPException as exc:
            error = str(exc.detail)
            print(f"failed match {match_id}: {error}")
            append_failed_match(match, error)
            failed_match_ids.add(match_id)
            newly_failed += 1
            continue
        except IncompleteMatchError as exc:
            error = str(exc)
            print(f"failed match {match_id}: {error}")
            append_failed_match(match, error)
            failed_match_ids.add(match_id)
            newly_failed += 1
            continue
        except Exception as exc:
            error = str(exc)
            print(f"failed match {match_id}: {error}")
            append_failed_match(match, error)
            failed_match_ids.add(match_id)
            newly_failed += 1
            continue

        if rows:
            append_rows(rows)
            total_player_rows += len(rows)

        completed_match_ids.add(match_id)
        processed_matches += 1

        print(
            f"saved match {match_id} "
            f"({len(rows)} player rows) | "
            f"processed={processed_matches} "
            f"completed_skipped={skipped_completed} "
            f"failed_skipped={skipped_failed} "
            f"new_failed={newly_failed}"
        )

    print(
        f"done. added {total_player_rows} player rows to {OUTPUT_FILE}. "
        f"processed={processed_matches}, "
        f"completed_skipped={skipped_completed}, "
        f"failed_skipped={skipped_failed}, "
        f"new_failed={newly_failed}"
    )


if __name__ == "__main__":
    main()