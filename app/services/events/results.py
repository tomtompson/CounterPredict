# app/services/event_results.py

from dataclasses import dataclass

from app.services.base import HLTVBase
from app.utils.utils import convert_timestamp_to_user_timezone, extract_from_url
from app.xpaths import Events


@dataclass
class HLTVEventResults(HLTVBase):
    """class for getting results from a specific event.

    Attributes:
        event_id: hltv event id
    """

    event_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """initialize response dict and URL."""
        super().__post_init__()

        self.use_flaresolverr = True
        self.response["event_id"] = self.event_id
        self.URL = f"https://www.hltv.org/events/{self.event_id}/matches"

    # ==================== PRIVATE METHODS ====================

    def _parse_match_won(self, container) -> bool | None:
        """Determine if team1 won based on 'score-won' class."""
        try:
            first_span_class = self.get_text_by_xpath(
                Events.EventResults.TEAM1_SCORE_CLASS,
                element=container,
            )
            return bool(first_span_class and "score-won" in first_span_class)
        except Exception:
            return None

    def _parse_match_type(self, match_type: str | None) -> str:
        """Normalize match type to 'boN' format."""
        if match_type and "bo" in match_type.lower():
            return match_type.lower()
        return "bo1"

    def _parse_match_container(self, container) -> dict | None:
        """Parse a single result container into a match dictionary."""
        # match url and id
        match_url_rel = self.get_text_by_xpath(
            Events.EventResults.MATCH_URL,
            element=container,
        )
        if not match_url_rel:
            return None
        match_url = f"https://www.hltv.org{match_url_rel}"
        match_id = extract_from_url(match_url, "id")

        # timestamp (atributo do container)
        timestamp_str = container.get("data-zonedgrouping-entry-unix")
        match_date = None

        if timestamp_str:
            try:
                timestamp_ms = float(timestamp_str)
                local_info = convert_timestamp_to_user_timezone(
                    timestamp_ms,
                    user_timezone="UTC",
                    logger=self.logger,
                )
                if local_info:
                    match_date = local_info["date_str"]
            except ValueError:
                self.logger.exception(f"invalid timestamp value: {timestamp_str}")

        # team 1
        team1_name = self.get_text_by_xpath(
            Events.EventResults.TEAM1_NAME,
            element=container,
        )
        team1_name = team1_name.strip() if team1_name else None

        team1_logo_rel = self.get_text_by_xpath(
            Events.EventResults.TEAM1_LOGO,
            element=container,
        )
        team1_logo = f"https:{team1_logo_rel}" if team1_logo_rel else None

        # team 2
        team2_name = self.get_text_by_xpath(
            Events.EventResults.TEAM2_NAME,
            element=container,
        )
        team2_name = team2_name.strip() if team2_name else None

        team2_logo_rel = self.get_text_by_xpath(
            Events.EventResults.TEAM2_LOGO,
            element=container,
        )
        team2_logo = f"https:{team2_logo_rel}" if team2_logo_rel else None

        # scores
        t1_raw = self.get_text_by_xpath(
            Events.EventResults.TEAM1_SCORE,
            element=container,
        )
        t2_raw = self.get_text_by_xpath(
            Events.EventResults.TEAM2_SCORE,
            element=container,
        )

        try:
            team1_score = int(t1_raw) if t1_raw else None
        except ValueError:
            team1_score = None
        try:
            team2_score = int(t2_raw) if t2_raw else None
        except ValueError:
            team2_score = None

        # match type
        raw_match_type = self.get_text_by_xpath(
            Events.EventResults.MATCH_TYPE,
            element=container,
        )
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
            "match_type": match_type,
            "match_won": match_won,
        }

    # ==================== PUBLIC METHODS ====================

    def get_event_results(self) -> dict:
        """
        Retrieve all results for a specific event.

        Returns:
            dict: event_id, results list, and result_count.
        """
        self.logger.info(f"fetching results for event {self.event_id}")

        # Carrega a página (uma só, sem paginação)
        self.page = self.request_url_page()

        # Encontra todos os containers de resultados
        containers = self.get_elements_by_xpath(Events.EventResults.RESULT_CONTAINER)

        results = []
        for container in containers:
            match_data = self._parse_match_container(container)
            if match_data:
                results.append(match_data)

        self.response["results"] = results
        self.response["result_count"] = len(results)

        self.logger.info(f"returned {len(results)} results for event {self.event_id}")
        return self.response
