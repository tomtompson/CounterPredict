
from dataclasses import dataclass
from typing import List, Dict, Optional
from urllib.parse import urlencode

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import convert_timestamp_to_user_timezone, extract_from_url
from app.utils.xpath import Teams


@dataclass
class HLTVTeamResults(HLTVBase):
    """
    class for getting a team's past match results (all pages).

    attributes:
        team_id: hltv team id
        page_size: number of matches per page (default 100)
    """

    team_id: str
    page_size: int = 100

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """initialize response."""
        super().__post_init__()
        self.response["team_id"] = self.team_id
        self.URL = ""

    # ==================== PRIVATE METHODS ====================

    def _get_results_url(self, offset: int = 0) -> str:
        """build url for the results page with optional offset."""
        params = {"team": self.team_id}
        if offset > 0:
            params["offset"] = offset
        return f"https://www.hltv.org/results?{urlencode(params)}"

    def _parse_match_won(self, container) -> Optional[bool]:
        """
        determine if the team won based on which score has class 'score-won'.
        returns True if first score (team1) has class 'score-won', False otherwise.
        """
        try:
            first_span_class = self.get_text_by_xpath(
                Teams.Results.TEAM1_SCORE_CLASS, 
                element=container
            )
            if first_span_class and 'score-won' in first_span_class:
                return True
            return False
        except Exception:
            return None

    def _parse_match_type(self, match_type: Optional[str]) -> str:
        """
        normalize match type:
        - if contains 'bo' (bo3, bo5), keep as is
        - otherwise, return 'bo1'
        """
        if match_type and 'bo' in match_type.lower():
            return match_type.lower()
        return 'bo1'

    def _parse_match_container(self, container) -> Optional[Dict]:
        """parse a single result container into a match dictionary."""
        # match url
        match_url_rel = self.get_text_by_xpath(Teams.Results.MATCH_URL, element=container)
        if not match_url_rel:
            return None
        match_url = f"https://www.hltv.org{match_url_rel}"
        match_id = extract_from_url(match_url, "id")

        timestamp_str = self.get_text_by_xpath(Teams.Results.TIMESTAMP, element=container)
        match_date = None

        if timestamp_str:
            try:
                timestamp_ms = float(timestamp_str)
                local_info = convert_timestamp_to_user_timezone(timestamp_ms, user_timezone="UTC", logger=self.logger)
                
                if local_info:
                    match_date = local_info["date_str"]
            except ValueError:
                self.logger.error(f"invalid timestamp value: {timestamp_str}")

        # teams
        team1_name = self.get_text_by_xpath(Teams.Results.TEAM1_NAME, element=container)
        team1_name = team1_name if team1_name and team1_name.strip() else None
        
        team1_logo_rel = self.get_text_by_xpath(Teams.Results.TEAM1_LOGO, element=container)
        team1_logo = f"https:{team1_logo_rel}" if team1_logo_rel else None

        team2_name = self.get_text_by_xpath(Teams.Results.TEAM2_NAME, element=container)
        team2_name = team2_name if team2_name and team2_name.strip() else None
        
        team2_logo_rel = self.get_text_by_xpath(Teams.Results.TEAM2_LOGO, element=container)
        team2_logo = f"https:{team2_logo_rel}" if team2_logo_rel else None

        # scores
        t1_raw = self.get_text_by_xpath(Teams.Results.TEAM1_SCORE, element=container)
        t2_raw = self.get_text_by_xpath(Teams.Results.TEAM2_SCORE, element=container)
        
        try:
            team1_score = int(t1_raw) if t1_raw else None
        except ValueError:
            team1_score = None
        try:
            team2_score = int(t2_raw) if t2_raw else None
        except ValueError:
            team2_score = None

        # event
        event_name = self.get_text_by_xpath(Teams.Results.EVENT_NAME, element=container)
        event_name = event_name if event_name and event_name.strip() else None
        
        event_logo_rel = self.get_text_by_xpath(Teams.Results.EVENT_LOGO, element=container)
        event_logo = f"https:{event_logo_rel}" if event_logo_rel else None

        # match type
        raw_match_type = self.get_text_by_xpath(Teams.Results.MATCH_TYPE, element=container)
        match_type = self._parse_match_type(raw_match_type)

        # match won
        match_won = self._parse_match_won(container)

        return {
            "match_url": match_url,
            "match_id": match_id,
            "match_date": match_date,
            "team1_name": team1_name,
            "team1_logo": team1_logo,
            "team1_score": team1_score,
            "team2_name": team2_name,
            "team2_logo": team2_logo,
            "team2_score": team2_score,
            "event_name": event_name,
            "event_logo": event_logo,
            "match_type": match_type,
            "match_won": match_won,
        }

    def _fetch_page_results(self, offset: int) -> List[Dict]:
        """
        fetch and parse a single results page.
        
        args:
            offset: page offset (0, 100, 200, ...)
            
        returns:
            list of match dictionaries for that page
        """
        url = self._get_results_url(offset)
        self.logger.info(f"fetching results page (offset={offset}): {url}")

        try:
            old_url = self.URL
            self.URL = url
            self.page = self.request_url_page()
            self.URL = old_url
        except Exception as e:
            self.logger.error(f"failed to load page at offset {offset}: {e}")
            return []

        if self.page is None:
            return []

        containers = self.get_elements_by_xpath(Teams.Results.RESULT_CONTAINER)
        self.logger.info(f"found {len(containers)} result containers on page (offset={offset})")

        results = []
        for container in containers:
            match_data = self._parse_match_container(container)
            if match_data:
                results.append(match_data)
        return results

    def _fetch_all_results(self) -> List[Dict]:
        """
        fetch all results pages until no more matches are found.
        
        returns:
            combined list of all matches from all pages
        """
        all_matches = []
        offset = 0
        
        while True:
            page_matches = self._fetch_page_results(offset)
            
            if not page_matches:
                self.logger.info(f"no more matches found at offset {offset}, stopping")
                break
            
            all_matches.extend(page_matches)
            self.logger.info(f"fetched {len(page_matches)} matches from offset {offset}, total: {len(all_matches)}")
            
            # if we got less than page_size, this is the last page
            if len(page_matches) < self.page_size:
                self.logger.info(f"last page reached (got {len(page_matches)} < {self.page_size})")
                break
            
            offset += self.page_size
        
        self.logger.info(f"total matches fetched: {len(all_matches)}")
        return all_matches

    # ==================== PUBLIC METHODS ====================

    def get_team_results(self) -> dict:
        """retrieve all past results for the team (all pages)."""
        self.logger.info(f"fetching all results for team {self.team_id}")
        results = self._fetch_all_results()

        self.response["results"] = results
        self.response["result_count"] = len(results)

        self.logger.info(f"returned {len(results)} results for team {self.team_id}")
        return self.response