# app/services/event_team_stats.py

from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import clear_number_str, extract_from_url
from app.utils.xpath import Events


@dataclass
class HLTVEventTeamStats(HLTVBase):
    """class for getting team stats from a specific event.

    Attributes:
        event_id: hltv event id
        team_id: hltv team id

    """

    event_id: str
    team_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Setup event team stats with event and team ids."""
        super().__post_init__()

        self.URL = f"https://www.hltv.org/events/{self.event_id}/who"
        self.response["event_id"] = self.event_id
        self.response["team_id"] = self.team_id

        self.logger.info(
            f"loading event team stats for event {self.event_id}, team {self.team_id}",
        )

        self.page = self.request_url_page()

        self.raise_exception_if_not_found(xpath=Events.EventProfile.EVENT_URL)

        self.logger.info(f"event page loaded for {self.event_id}")

    # ==================== PARSING METHODS ====================

    def __parse_team_placement(self) -> dict:
        """Parse team placement data.

        Returns:
            dict with team_placement (string) and qualify_method (optional)

        """
        data = {}

        try:
            team_placement = self.get_text_by_xpath(
                Events.EventTeamStats.TEAM_PLACEMENT.format(team_id=self.team_id),
            )
            data["team_placement"] = team_placement or ""

            qualify_method = self.get_text_by_xpath(
                Events.EventTeamStats.QUALIFY_METHOD.format(team_id=self.team_id),
            )
            data["qualify_method"] = qualify_method or None

            self.logger.debug(
                f"placement: '{data['team_placement']}', qualify: {data['qualify_method']}",
            )

        except Exception as e:
            self.logger.exception(f"error parsing team placement: {e}")
            data["team_placement"] = ""
            data["qualify_method"] = None

        return data

    def __parse_team_lineup(self) -> list[dict]:
        """Parse team lineup data.

        Returns:
            list of player dicts with id, nickname, event_stats url

        """
        lineup = []

        try:
            team_lineup = self.get_all_by_xpath(
                Events.EventTeamStats.TEAM_LINEUP.format(team_id=self.team_id),
            )
            team_player_urls = self.get_all_by_xpath(
                Events.EventTeamStats.TEAM_PLAYER_URL.format(team_id=self.team_id),
            )

            self.logger.debug(f"found {len(team_lineup)} players in lineup")

            for i, (nickname, url) in enumerate(
                zip(team_lineup, team_player_urls, strict=False)
            ):
                try:
                    player_id = extract_from_url(url, "id") if url else None

                    if player_id and nickname:
                        lineup.append(
                            {
                                "id": player_id,
                                "nickname": nickname,
                                "event_stats": f"https://www.hltv.org/stats/players/{player_id}/who?event={self.event_id}",
                            },
                        )
                    else:
                        self.logger.warning(
                            f"skipping player {i}: missing id or nickname",
                        )
                except Exception as e:
                    self.logger.exception(f"error parsing player {i}: {e}")
                    continue

        except Exception as e:
            self.logger.exception(f"error parsing team lineup: {e}")

        return lineup

    def __parse_team_coach(self) -> list[dict]:
        """Parse team coach data.

        Returns:
            list with coach dict (id, nickname) or empty list

        """
        coach_data = []

        try:
            team_coach = self.get_text_by_xpath(
                Events.EventTeamStats.TEAM_COACH.format(team_id=self.team_id),
            )

            coach_url_suffix = self.get_text_by_xpath(
                Events.EventTeamStats.TEAM_COACH_URL.format(team_id=self.team_id),
            )

            if team_coach and coach_url_suffix:
                coach_url = f"https://www.hltv.org{coach_url_suffix}"
                coach_id = extract_from_url(coach_url, "id")

                if coach_id:
                    coach_data.append({"id": coach_id, "nickname": team_coach})
                    self.logger.debug(f"coach: {team_coach}")

        except Exception as e:
            self.logger.exception(f"error parsing team coach: {e}")

        return coach_data

    def __parse_vrs_data(self) -> list[dict]:
        """Parse vrs ranking data.

        Returns:
            list of vrs dicts (date, points, placements)

        """
        vrs_list = []

        try:
            vrs_data = {
                "vrs_date": self.get_text_by_xpath(Events.EventTeamStats.VRS_DATE),
                "points_before_event": self._parse_int_safe(
                    Events.EventTeamStats.VRS_POINTS_BEFORE_EVENT.format(
                        team_id=self.team_id,
                    ),
                ),
                "points_after_event": self._parse_int_safe(
                    Events.EventTeamStats.VRS_POINTS_AFTER_EVENT.format(
                        team_id=self.team_id,
                    ),
                ),
                "points_acquired": self._parse_int_safe(
                    Events.EventTeamStats.VRS_POINTS_ACQUIRED.format(
                        team_id=self.team_id,
                    ),
                ),
                "placement_before_event": self._parse_int_safe(
                    Events.EventTeamStats.VRS_PLACEMENT_BEFORE_EVENT.format(
                        team_id=self.team_id,
                    ),
                    use_clear=True,
                ),
                "placement_after_event": self._parse_int_safe(
                    Events.EventTeamStats.VRS_PLACEMENT_AFTER_EVENT.format(
                        team_id=self.team_id,
                    ),
                    use_clear=True,
                ),
            }

            if any(vrs_data.values()):
                vrs_list.append(vrs_data)
                self.logger.debug(
                    f"vrs data parsed: before {vrs_data['placement_before_event']} → after {vrs_data['placement_after_event']}",
                )

        except Exception as e:
            self.logger.exception(f"error parsing vrs data: {e}")

        return vrs_list

    def __parse_prize_data(self) -> list[dict]:
        """Parse prize money data.

        Returns:
            list of prize dicts (prize, club_share)

        """
        prize_list = []

        try:
            prize = self._parse_int_safe(
                Events.EventTeamStats.PRIZE.format(team_id=self.team_id),
                use_clear=True,
            )

            club_share = self._parse_int_safe(
                Events.EventTeamStats.PRIZE_CLUB_SHARE.format(team_id=self.team_id),
                use_clear=True,
            )

            if prize is not None:
                prize_list.append(
                    {"prize": prize, "club_share": club_share or None},
                )
                self.logger.debug(f"prize: {prize}, club share: {club_share}")

        except Exception as e:
            self.logger.exception(f"error parsing prize data: {e}")

        return prize_list

    def _parse_int_safe(self, xpath: str, use_clear: bool = False) -> int | None:
        """Safely parse integer values, returning None if not found.

        Args:
            xpath: xpath to get value
            use_clear: whether to use clear_number_str

        Returns:
            int or None

        """
        try:
            value = self.get_text_by_xpath(xpath)
            if not value:
                return None
            if use_clear:
                return clear_number_str(value)
            try:
                return int(value)
            except Exception:
                return None
        except Exception:
            return None

    def __parse_all_stats(self) -> dict:
        """Parse all team stats for the event.

        Returns:
            dict with team_placement, qualify_method, lineup, coach, vrs, prize

        """
        self.logger.info(
            f"parsing stats for team {self.team_id} at event {self.event_id}",
        )

        try:
            placement_data = self.__parse_team_placement()
            lineup = self.__parse_team_lineup()
            coach = self.__parse_team_coach()
            vrs = self.__parse_vrs_data()
            prize = self.__parse_prize_data()

            event_stats = {
                "team_placement": placement_data.get("team_placement", ""),
                "qualify_method": placement_data.get("qualify_method"),
                "lineup": lineup,
                "coach": coach or None,
                "vrs": vrs or None,
                "prize": prize or None,
            }

            self.logger.info(
                f"stats parsed: {len(lineup)} players, {len(vrs)} vrs entries",
            )
            return event_stats

        except Exception as e:
            self.logger.exception(f"error parsing all stats: {e}")
            return {
                "team_placement": "",
                "qualify_method": None,
                "lineup": [],
                "coach": None,
                "vrs": None,
                "prize": None,
            }

    # ==================== PUBLIC METHODS ====================

    def get_team_event_stats(self) -> dict:
        """Get team stats for specific event.

        Returns:
            dict with team_id, event_id and stats

        """
        try:
            event_stats = self.__parse_all_stats()

            self.response["team_id"] = self.team_id
            self.response["event_id"] = self.event_id
            self.response["stats"] = event_stats

            self.logger.info(
                f"returning stats for team {self.team_id} at event {self.event_id}",
            )

        except Exception as e:
            self.logger.exception(f"error in get_team_event_stats: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error processing team event stats: {e!s}",
            )

        return self.response
