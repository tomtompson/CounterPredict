# app/services/upcoming_matches.py

import contextlib
from dataclasses import dataclass
from datetime import datetime
import re

import pytz
from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import (
    convert_timestamp_to_user_timezone,
)
from app.xpaths import Events


@dataclass
class HLTVEventsUpcomingMatches(HLTVBase):
    """class for getting upcoming matches from HLTV with timezone conversion and filtering."""

    event_id : str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Load matches page and set URL."""
        super().__post_init__()
        self.URL = f"https://www.hltv.org/events/{self.event_id}/matches"
        self.response["event_id"] = self.event_id
        self.logger.info("loading matches page")
        self.page = self.request_url_page()
        self.logger.info("matches page loaded successfully")

    # ==================== PRIVATE METHODS ====================

    def __parse_match_data(
        self,
        match_element,
        fallback_timestamp: float | None = None,
        section_date: str | None = None,
    ) -> dict | None:
        """
        Parse a upcoming event match element into a dictionary.

        Args:
            match_element (_type_): lxml element of the match wrapper.
            fallback_timestamp (float | None, optional): timestamp from section used when not found in the match element. Defaults to None.

        Returns:
            dict | None: match data dict, or None on error.
        """
        try:
            match_id = match_element.get("data-match-id")

            team1_name = (
                self.get_text_by_xpath(
                    Events.EventMatches.TEAM_NAME,
                    element=match_element,
                )
                or "TBD"
            )
            team2_name = (
                self.get_text_by_xpath(
                    Events.EventMatches.TEAM_NAME,
                    pos=1,
                    element=match_element,
                )
                or "TBD"
            )

            team1_id = match_element.get("team1") or ""
            team2_id = match_element.get("team2") or ""

            team1_logo = self.get_text_by_xpath(
                Events.EventMatches.TEAM_LOGO,
                element=match_element,
            )
            team2_logo = self.get_text_by_xpath(
                Events.EventMatches.TEAM_LOGO,
                pos=1,
                element=match_element,
            )

            event_name = self.get_text_by_xpath(
                Events.EventMatches.EVENT_NAME,
                element=match_element,
            )
            event_id = match_element.get("data-event-id")

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
                    Events.EventMatches.MATCH_TIMESTAMP,
                    element=match_element,
                )
                if match_timestamp_attr:
                    with contextlib.suppress(ValueError, TypeError):
                        match_timestamp = float(match_timestamp_attr)

            match_type = self.get_text_by_xpath(
                Events.EventMatches.MATCH_TYPE,
                element=match_element,
            )
            time_text = self.get_text_by_xpath(
                Events.EventMatches.MATCH_TIME,
                element=match_element,
            )

            match_url = self.get_text_by_xpath(
                Events.EventMatches.MATCH_URL,
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
                "event_name": event_name,
                "event_id": event_id,
                "match_timestamp": match_timestamp,
                "match_type": match_type,
                "display_time": time_text,
                "display_date": section_date,
                "is_tbd": is_tbd,
                "match_status": "tbd" if is_tbd else "scheduled",
            }

        except Exception as e:
            self.logger.exception(
                f"error parsing match {match_id if 'match_id' in locals() else 'unknown'}: {e}",
            )
            return None

    def __parse_section(self, section_element) -> list[dict]:
        """
        Parse a single day section and return list of matches.

        Args:
            section_element (_type_): lxml element of the section.

        Returns:
            list[dict]: match dictionaries.
        """
        matches = []
        match_wrappers = self.get_elements_by_xpath(
            Events.EventMatches.MATCH_WRAPPER,
            element=section_element,
        )
        self.logger.info(f"section contains {len(match_wrappers)} match wrappers")

        section_timestamp = section_element.get("data-zonedgrouping-entry-unix")
        section_timestamp = float(section_timestamp) if section_timestamp else None
        section_date = self.get_text_by_xpath(
            Events.EventMatches.DAY_HEADLINE,
            element=section_element,
        )
        if not section_date:
            section_date = self.get_text_by_xpath(
                Events.EventMatches.DAY_HEADLINE_ALT,
                element=section_element,
            )
        if section_date:
            match = re.search(r"(\d{4}-\d{2}-\d{2})", section_date)
            if match:
                section_date = match.group(1)

        for match_wrapper in match_wrappers:
            match_data = self.__parse_match_data(
                match_wrapper,
                fallback_timestamp=section_timestamp,
                section_date=section_date,
            )
            if match_data:
                matches.append(match_data)
            else:
                self.logger.warning(
                    f"failed to parse match {match_wrapper.get('data-match-id', 'unknown id')}",
                )
        return matches

    # ==================== PUBLIC METHODS ====================

    def get_upcoming_matches(self, user_timezone: str = "UTC") -> dict:
        """
        Get upcoming matches converted to the user's timezone.

        Args:
            user_timezone (str, optional): IANA timezone name. Defaults to "UTC".

        Returns:
            dict: matches list and match_count.
        """
        try:
            self.logger.info(f"using timezone: {user_timezone}")

            all_sections = self.get_elements_by_xpath(Events.EventMatches.DAY_SECTION)

            if not all_sections:
                self.logger.warning("no match sections found")
                self.response["event_id"] = self.event_id
                self.response["matches"] = []
                self.response["match_count"] = 0
                self.response["timezone"] = user_timezone
                return self.response


            all_matches = []
            for idx, section in enumerate(all_sections):
                section_date = self.get_text_by_xpath(
                    Events.EventMatches.DAY_HEADLINE,
                    element=section,
                )
                if section_date:
                    match = re.search(r"(\d{4}-\d{2}-\d{2})", section_date)
                    if match:
                        section_date =  match.group(1)
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
                    if not match.get("display_date"):
                        match["display_date"] = local_info["date_str"]
                else:
                    match["local_date"] = None
                    match["local_time"] = None
                    match["local_weekday"] = None
                    match["local_timezone"] = user_timezone
            event_name = self.get_text_by_xpath(Events.EventMatches.EVENT_NAME)
            self.response["event_name"] = event_name
            self.response["event_id"] = self.event_id
            self.response["matches"] = all_matches
            self.response["match_count"] = len(all_matches)
            self.response["timezone"] = user_timezone
            self.logger.info(
                f"total matches parsed: {len(all_matches)} using timezone {user_timezone}",
            )

        except Exception as e:
            self.logger.exception(f"error in get_upcoming_matches: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        return self.response
