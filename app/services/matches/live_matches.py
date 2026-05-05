# app/services/live_matches.py

from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import extract_from_url
from app.utils.xpath import Matches


@dataclass
class HLTVLiveMatches(HLTVBase):
    """class for getting live matches from hltv."""

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Setup live matches fetch."""
        super().__post_init__()

        self.URL = "https://www.hltv.org/matches"

        self.logger.info("loading live matches")

        self.page = self.request_url_page()

        self.logger.info("matches page loaded successfully")

    # ==================== PRIVATE METHODS ====================

    def __get_live_match_containers(self) -> list:
        """Find only live match containers (with live="true" attribute).

        Returns:
            list of lxml elements representing live match containers

        """
        containers = self.get_elements_by_xpath(
            Matches.LiveMatches.LIVE_MATCH_CONTAINER,
        )
        self.logger.info(f"found {len(containers)} live matches")
        return containers

    # ==================== PARSING METHODS ====================

    def __parse_match_data(self, match_element) -> dict | None:
        """Parse data from a single live match element.

        Args:
            match_element: lxml element for the match

        Returns:
            dict with match data or None if error

        """
        try:
            team_a_name = self.get_text_by_xpath(
                Matches.LiveMatches.TEAM, element=match_element,
            )
            team_b_name = self.get_text_by_xpath(
                Matches.LiveMatches.TEAM, pos=1, element=match_element,
            )

            team_a_id = match_element.get("team1")
            team_b_id = match_element.get("team2")

            tournament_name = self.get_text_by_xpath(
                Matches.LiveMatches.TOURNAMENT_NAME, element=match_element,
            )
            tournament_id = match_element.get("data-event-id")

            match_type = self.get_text_by_xpath(
                Matches.LiveMatches.MATCH_TYPE, element=match_element,
            )

            match_url = self.get_text_by_xpath(
                Matches.LiveMatches.MATCH_URL, element=match_element,
            )
            if match_url and not match_url.startswith("http"):
                match_url = f"https://www.hltv.org{match_url}"

            match_id = extract_from_url(match_url, "id") if match_url else None

            self.logger.info(f"parsed: {team_a_name} vs {team_b_name}")

            return {
                "match_id": match_id,
                "teamA": team_a_name,
                "teamAId": team_a_id,
                "teamAMapScore": None,
                "teamACurrentMapScore": None,
                "teamB": team_b_name,
                "teamBId": team_b_id,
                "teamBMapScore": None,
                "teamBCurrentMapScore": None,
                "tournamentName": tournament_name,
                "tournamentId": tournament_id,
                "matchType": match_type,
                "matchUrl": match_url,
            }


        except Exception as e:
            self.logger.exception(f"error parsing match: {e}")
            return None

    def __parse_live_matches(self) -> list[dict]:
        """Parse all live matches from page.

        Returns:
            list of live match dictionaries

        """
        live_matches = []

        try:
            match_containers = self.__get_live_match_containers()

            if not match_containers:
                self.logger.info("no live matches currently")
                return []

            self.logger.info(f"parsing {len(match_containers)} live matches")

            for idx, match_element in enumerate(match_containers):
                match_data = self.__parse_match_data(match_element)
                if match_data and match_data.get("teamA") and match_data.get("teamB"):
                    live_matches.append(match_data)
                    self.logger.info(
                        f"added match {idx + 1}: {match_data['teamA']} vs {match_data['teamB']}",
                    )

            self.logger.info(f"successfully parsed {len(live_matches)} live matches")

        except Exception as e:
            self.logger.exception(f"error parsing live matches: {e}")

        return live_matches

    # ==================== PUBLIC METHODS ====================

    def get_live_matches(self) -> dict:
        """Get all live matches following schema.

        Returns:
            dict with liveMatchsCount and liveMatchs list

        """
        try:
            live_matches = self.__parse_live_matches()

            self.response["liveMatchsCount"] = len(live_matches)
            self.response["liveMatchs"] = live_matches

            self.logger.info(f"returning {len(live_matches)} live matches")

        except Exception as e:
            self.logger.exception(f"error in get_live_matches: {e}")
            raise HTTPException(
                status_code=500, detail=f"error getting live matches: {e!s}",
            )

        return self.response
