# app/services/team_upcoming_matches.py

import re
from dataclasses import dataclass
from datetime import datetime

import pytz
from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import convert_timestamp_to_user_timezone, extract_from_url
from app.utils.xpath import Teams


@dataclass
class HLTVTeamUpcomingMatches(HLTVBase):
    """class for getting upcoming matches for a team.

    Attributes:
        team_id: hltv team id

    """

    team_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Setup upcoming matches with team id."""
        super().__post_init__()

        self.URL = f"https://www.hltv.org/team/{self.team_id}/who#tab-matchesBox"
        self.response["team_id"] = self.team_id

        self.logger.info(f"loading upcoming matches for team {self.team_id}")
        self.page = self.request_url_page()
        self.logger.info(f"team page loaded for {self.team_id}")

    # ==================== PRIVATE METHODS ====================

    def __get_upcoming_match_ids(self) -> list[str]:
        """Extract upcoming match ids from the team page.

        Returns:
            list of match id strings

        """
        match_ids = []
        try:
            upcoming_container = self.get_elements_by_xpath(
                Teams.UpcomingMatches.UPCOMING_MATCHES_ROW,
            )
            if not upcoming_container:
                self.logger.warning("no upcoming matches container found")
                return []
            container = upcoming_container[0]
            match_urls = self.get_all_by_xpath(
                Teams.UpcomingMatches.MATCH_URL, element=container,
            )
            for idx, url in enumerate(match_urls):
                try:
                    match_id = extract_from_url(url, "id")
                    if match_id:
                        match_ids.append(match_id)
                    else:
                        self.logger.warning(
                            f"could not extract id from url {idx}: {url}",
                        )
                except Exception as e:
                    self.logger.exception(f"error extracting id from url {idx}: {e}")
            self.logger.info(f"extracted {len(match_ids)} upcoming match ids")
        except Exception as e:
            self.logger.exception(f"error getting upcoming match ids: {e}")
        return match_ids

    # ==================== PARSING METHODS ====================

    def __parse_single_match(
        self, match_id: str, user_timezone: str = "UTC",
    ) -> dict | None:
        """Parse a single match page into a dictionary with local date fields.

        Args:
            match_id: hltv match id
            user_timezone: IANA timezone for date conversion

        Returns:
            dict with match data or None

        """
        match_url = f"https://www.hltv.org/matches/{match_id}/who"
        self.logger.debug(f"fetching match page: {match_url}")

        try:
            match_page = self.request_url_page(match_url)
        except HTTPException as e:
            if e.status_code == 404:
                self.logger.warning(f"match {match_id} not found (404), skipping")
            else:
                self.logger.exception(
                    f"http error {e.status_code} for match {match_id}: {e.detail}",
                )
            return None
        except Exception as e:
            self.logger.exception(f"unexpected error fetching match {match_id}: {e}")
            return None

        try:
            event_name = self.get_text_by_xpath(
                Teams.UpcomingMatches.EVENT_NAME, element=match_page,
            )
            event_url = self.get_text_by_xpath(
                Teams.UpcomingMatches.EVENT_URL, element=match_page,
            )
            tournament_id = extract_from_url(event_url, "id") if event_url else None

            rival_team_name = self.get_text_by_xpath(
                Teams.UpcomingMatches.RIVAL_TEAM_NAME, element=match_page,
            )
            rival_team_url = self.get_text_by_xpath(
                Teams.UpcomingMatches.RIVAL_TEAM_URL, element=match_page,
            )
            rival_team_id = (
                extract_from_url(rival_team_url, "id") if rival_team_url else None
            )

            match_type = self.get_text_by_xpath(
                Teams.UpcomingMatches.MATCH_TYPE, element=match_page,
            )

            # --- timestamp extraction: uses data-unix from .time or .date element ---
            match_timestamp = None
            unix_elem = match_page.xpath(
                ".//div[contains(@class, 'timeAndEvent')]//*[@data-unix]",
            )
            if unix_elem:
                match_timestamp = float(unix_elem[0].get("data-unix"))
            else:
                time_div = match_page.xpath(".//div[contains(@class, 'time')]")
                if time_div and time_div[0].get("data-unix"):
                    match_timestamp = float(time_div[0].get("data-unix"))

            if not match_timestamp:
                date_str = self.get_text_by_xpath(
                    Teams.UpcomingMatches.MATCH_DATE, element=match_page,
                )
                hour_str = self.get_text_by_xpath(
                    Teams.UpcomingMatches.MATCH_HOUR, element=match_page,
                )
                if date_str and hour_str:
                    try:
                        if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
                            dt = datetime.strptime(
                                f"{date_str} {hour_str}", "%Y-%m-%d %H:%M",
                            )
                        else:
                            clean_date = re.sub(r"(\d)(st|nd|rd|th)", r"\1", date_str)
                            dt = datetime.strptime(clean_date, "%B %d %Y")
                            dt = dt.replace(
                                hour=int(hour_str.split(":")[0]),
                                minute=int(hour_str.split(":")[1]),
                            )
                        cet = pytz.timezone("CET")
                        match_timestamp = cet.localize(dt).timestamp() * 1000
                    except Exception as e:
                        self.logger.debug(
                            f"could not parse date/hour for match {match_id}: {e}",
                        )

            local_info = convert_timestamp_to_user_timezone(
                match_timestamp, user_timezone, logger=self.logger,
            )

            match_data = {
                "match_id": match_id,
                "match_url": match_url,
                "event_name": event_name,
                "event_id": tournament_id,
                "rival_team_name": rival_team_name,
                "rival_team_id": rival_team_id,
                "match_type": match_type,
                "match_timestamp": match_timestamp,
                "local_date": local_info["date_str"] if local_info else None,
                "local_time": local_info["time_str"] if local_info else None,
                "local_weekday": local_info["weekday"] if local_info else None,
                "local_timezone": user_timezone if local_info else None,
            }
            self.logger.debug(
                f"parsed match {match_id}: {event_name} vs {rival_team_name}",
            )
            return match_data
        except Exception as e:
            self.logger.exception(f"error parsing match {match_id}: {e}")
            return None

    def __parse_upcoming_matches(self, user_timezone: str = "UTC") -> list[dict]:
        """Parse all upcoming matches for the team.

        Args:
            user_timezone: IANA timezone for date conversion

        Returns:
            list of match dictionaries

        """
        matches = []
        match_ids = self.__get_upcoming_match_ids()
        if not match_ids:
            self.logger.info(f"no upcoming matches found for team {self.team_id}")
            return []
        self.logger.info(f"parsing {len(match_ids)} upcoming matches")
        for match_id in match_ids:
            match_data = self.__parse_single_match(match_id, user_timezone)
            if match_data:
                matches.append(match_data)
        self.logger.info(f"successfully parsed {len(matches)} upcoming matches")
        return matches

    # ==================== PUBLIC METHODS ====================

    def get_team_upcoming_matches(self, user_timezone: str = "UTC") -> dict:
        """Get upcoming matches for the team with timezone conversion.

        Args:
            user_timezone: IANA timezone name (e.g., "America/Sao_Paulo")

        Returns:
            dict with team_id, upcoming_matches, match_count, timezone

        """
        try:
            matches = self.__parse_upcoming_matches(user_timezone)
            self.response["team_id"] = self.team_id
            self.response["upcoming_matches"] = matches
            self.response["match_count"] = len(matches)
            self.response["timezone"] = user_timezone
            self.logger.info(
                f"returning {len(matches)} upcoming matches for team {self.team_id} using {user_timezone}",
            )
        except Exception as e:
            self.logger.exception(f"error in get_team_upcoming_matches: {e}")
            raise HTTPException(
                status_code=500, detail=f"error getting team upcoming matches: {e!s}",
            )
        return self.response
