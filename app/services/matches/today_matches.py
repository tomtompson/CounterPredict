# app/services/today_matches.py

import contextlib
from dataclasses import dataclass
from datetime import datetime

import pytz
from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import (
    convert_timestamp_to_user_timezone,
    extract_date_from_headline,
)
from app.utils.xpath import Matches


@dataclass
class HLTVTodayMatches(HLTVBase):
    """class for getting today's matches from HLTV with timezone conversion and filtering."""

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Load matches page and set URL."""
        super().__post_init__()
        self.URL = "https://www.hltv.org/matches"
        self.logger.info("loading matches page")
        self.page = self.request_url_page()
        self.logger.info("matches page loaded successfully")

    # ==================== PRIVATE METHODS ====================

    def __parse_match_data(
        self,
        match_element,
        fallback_timestamp: float | None = None,
    ) -> dict | None:
        """Parse a single match element into a dictionary.

        Args:
            match_element: lxml element of the match wrapper
            fallback_timestamp: timestamp from section if not found in match

        Returns:
            dict with match data or None

        """
        try:
            match_id = match_element.get("data-match-id")

            team1_name = (
                self.get_text_by_xpath(
                    Matches.TodayMatches.TEAM_NAME,
                    element=match_element,
                )
                or "TBD"
            )
            team2_name = (
                self.get_text_by_xpath(
                    Matches.TodayMatches.TEAM_NAME,
                    pos=1,
                    element=match_element,
                )
                or "TBD"
            )

            team1_id = match_element.get("team1") or ""
            team2_id = match_element.get("team2") or ""

            team1_logo = self.get_text_by_xpath(
                Matches.TodayMatches.TEAM_LOGO,
                element=match_element,
            )
            team2_logo = self.get_text_by_xpath(
                Matches.TodayMatches.TEAM_LOGO,
                pos=1,
                element=match_element,
            )

            tournament_name = self.get_text_by_xpath(
                Matches.TodayMatches.TOURNAMENT_NAME,
                element=match_element,
            )
            tournament_id = match_element.get("data-event-id")
            tournament_logo = self.get_text_by_xpath(
                Matches.TodayMatches.TOURNAMENT_LOGO,
                element=match_element,
            )

            match_timestamp = None
            time_div = match_element.xpath(".//div[contains(@class, 'match-time')]")
            if time_div:
                unix_attr = time_div[0].get("data-unix")
                if unix_attr:
                    match_timestamp = float(unix_attr)

            if not match_timestamp and fallback_timestamp:
                match_timestamp = fallback_timestamp

            if not match_timestamp:
                match_timestamp_attr = self.get_text_by_xpath(
                    Matches.TodayMatches.MATCH_TIMESTAMP,
                    element=match_element,
                )
                if match_timestamp_attr:
                    with contextlib.suppress(ValueError, TypeError):
                        match_timestamp = float(match_timestamp_attr)

            match_type = self.get_text_by_xpath(
                Matches.TodayMatches.MATCH_TYPE,
                element=match_element,
            )
            time_text = self.get_text_by_xpath(
                Matches.TodayMatches.MATCH_TIME,
                element=match_element,
            )

            match_url = self.get_text_by_xpath(
                Matches.TodayMatches.MATCH_URL,
                element=match_element,
            )
            if match_url and not match_url.startswith("http"):
                match_url = f"https://www.hltv.org{match_url}"

            is_tbd = not (
                team1_id and team2_id and team1_name != "TBD" and team2_name != "TBD"
            )

            self.logger.debug(
                f"match {match_id}: {team1_name} vs {team2_name} -> timestamp: {match_timestamp}",
            )

            return {
                "match_id": match_id,
                "match_url": match_url,
                "team1_name": team1_name,
                "team1_id": team1_id,
                "team1_logo": team1_logo,
                "team2_name": team2_name,
                "team2_id": team2_id,
                "team2_logo": team2_logo,
                "tournament_name": tournament_name,
                "tournament_id": tournament_id,
                "tournament_logo": tournament_logo,
                "match_timestamp": match_timestamp,
                "match_type": match_type,
                "display_time": time_text,
                "display_date": None,
                "is_tbd": is_tbd,
                "match_status": "tbd" if is_tbd else "scheduled",
            }

        except Exception as e:
            self.logger.exception(
                f"error parsing match {match_id if 'match_id' in locals() else 'unknown'}: {e}",
            )
            return None

    def __parse_section(self, section_element) -> list[dict]:
        """Parse a single day section and return list of matches.

        Args:
            section_element: lxml element of the section

        Returns:
            list of match dictionaries

        """
        matches = []
        match_zones = section_element.xpath(
            ".//div[contains(@class, 'match-zone-wrapper')]",
        )
        self.logger.info(f"section contains {len(match_zones)} match zone wrappers")

        for zone in match_zones:
            section_timestamp = zone.get("data-zonedgrouping-entry-unix")
            section_timestamp = float(section_timestamp) if section_timestamp else None

            match_wrappers = zone.xpath(".//div[contains(@class, 'match-wrapper')]")
            for match_wrapper in match_wrappers:
                match_data = self.__parse_match_data(
                    match_wrapper,
                    fallback_timestamp=section_timestamp,
                )
                if match_data:
                    matches.append(match_data)
                else:
                    self.logger.warning(
                        f"failed to parse match {match_wrapper.get('data-match-id', 'unknown id')}",
                    )
        return matches

    # ==================== PUBLIC METHODS ====================

    def get_today_matches(self, user_timezone: str = "UTC") -> dict:
        """Get matches from the first two sections (today and tomorrow in HLTV timezone),
        convert times to the user's timezone, and filter only matches that fall on the current day
        (based on that timezone).

        Args:
            user_timezone: IANA timezone name (e.g., "America/Sao_Paulo", "America/New_York").

        Returns:
            dict with keys: matches (list) and match_count (int)

        """
        try:
            self.logger.info(f"using timezone: {user_timezone}")

            xpath_sections = (
                "//div[contains(@class, 'matches-list-section') and @match-container]"
            )
            all_sections = self.get_elements_by_xpath(xpath_sections)

            if not all_sections:
                self.logger.warning("no match sections found")
                self.response["matches"] = []
                self.response["match_count"] = 0
                return self.response

            sections_to_parse = all_sections[:2]
            self.logger.info(
                f"processing {len(sections_to_parse)} day sections (today and tomorrow)",
            )

            all_matches = []
            for idx, section in enumerate(sections_to_parse):
                section_date = extract_date_from_headline(
                    section,
                    self.get_text_by_xpath,
                )
                self.logger.info(f"section {idx + 1} - date: {section_date}")
                section_matches = self.__parse_section(section)
                all_matches.extend(section_matches)
                self.logger.info(
                    f"section {idx + 1} yielded {len(section_matches)} matches",
                )

            for match in all_matches:
                local_info = convert_timestamp_to_user_timezone(
                    match["match_timestamp"],
                    user_timezone,
                    logger=self.logger,
                )
                if local_info:
                    match["local_date"] = local_info["date_str"]
                    match["local_time"] = local_info["time_str"]
                    match["local_weekday"] = local_info["weekday"]
                    match["local_timezone"] = local_info["timezone"]
                else:
                    match["local_date"] = None
                    match["local_time"] = None
                    match["local_weekday"] = None
                    match["local_timezone"] = user_timezone

            tz = pytz.timezone(user_timezone)
            today_local_str = datetime.now(tz).strftime("%Y-%m-%d")
            filtered_matches = [
                m for m in all_matches if m.get("local_date") == today_local_str
            ]

            self.response["matches"] = filtered_matches
            self.response["match_count"] = len(filtered_matches)
            self.logger.info(
                f"total matches parsed: {len(all_matches)}, filtered for today ({today_local_str} with timezone {user_timezone}): {len(filtered_matches)}",
            )

        except Exception as e:
            self.logger.exception(f"error in get_today_matches: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        return self.response
