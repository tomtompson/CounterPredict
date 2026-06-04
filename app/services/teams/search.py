# app/services/team_search.py
from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import clear_number_str, extract_country_name_from_flag_url, extract_from_url
from app.xpaths import Ranking


@dataclass
class HLTVTeamSearch(HLTVBase):
    """class for searching teams on hltv.

    Attributes:
        query: search term for teams

    """

    query: str = None
    top_n: int = None

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Set up team search with query."""
        super().__post_init__()
        if self.query is not None:
            self.URL = f"https://www.hltv.org/search?term={self.query}"
            self.response["query"] = self.query

            self.logger.info(f"searching teams with query: {self.query}")

            self.page_data = self.__fetch_json()

            self.logger.info("team search data fetched successfully")
        elif self.top_n is not None:
            self.URL = "https://www.hltv.org/ranking/teams"
            self.response["top_n"] = self.top_n

            self.logger.info(f"fetching top {self.top_n} teams")
            self.page = self.request_url_page()
            self.logger.info("top teams page fetched successfully")

    # ==================== PRIVATE METHODS ====================

    def __fetch_json(self) -> dict:
        """
        Make GET request and return JSON response.

        Raises:
            HTTPException: if the request fails.

        Returns:
            dict: raw JSON data from HLTV search.
        """
        try:
            self.logger.debug(f"fetching json from {self.URL}")

            res = self.make_request(self.URL)

            self.logger.debug(f"response status: {res.status_code}")

            data = res.json()
            self.logger.debug("json data received")

            return data

        except Exception as e:
            self.logger.exception(f"error fetching json: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error fetching team search data: {e!s}",
            )

    # ==================== PARSING METHODS ====================

    @staticmethod
    def __make_absolute_url(url: str | None) -> str | None:
        """Convert a relative HLTV URL into an absolute URL."""
        if not url:
            return None
        if url.startswith("http"):
            return url
        if url.startswith("//"):
            return f"https:{url}"
        if url.startswith("/"):
            return f"https://www.hltv.org{url}"
        return url

    def __parse_ranking_lineup(self, team_element) -> list[dict]:
        """
        Parse lineup data from the ranking page team card.

        Returns:
            list[dict]: player dicts compatible with TeamSearchPlayersDetails.
        """
        lineup = []

        try:
            player_rows = self.get_elements_by_xpath(
                Ranking.Stats.PLAYER_ROW,
                element=team_element,
            )

            for player in player_rows:
                player_nickname = self.get_text_by_xpath(
                    Ranking.Stats.PLAYER_NICKNAME,
                    element=player,
                )
                player_url = self.get_text_by_xpath(
                    Ranking.Stats.PLAYER_URL,
                    element=player,
                )
                nationality = self.get_text_by_xpath(
                    Ranking.Stats.PLAYER_NATIONALITY,
                    element=player,
                )
                player_id = extract_from_url(player_url, "id") if player_url else None
                profile_url = self.__make_absolute_url(player_url)

                if not player_id or not player_nickname or not profile_url:
                    continue

                lineup.append(
                    {
                        "id": str(player_id),
                        "nickname": player_nickname,
                        "name": player_nickname,
                        "nationality": nationality,
                        "profile_url": profile_url,
                    },
                )
        except Exception as e:
            self.logger.exception(f"error parsing ranking lineup: {e}")

        return lineup

    def __parse_top_teams(self) -> list[dict]:
        """
        Parse the ranking page into a plain team list for `/teams/list`.

        Returns:
            list[dict]: top-ranked team data.
        """
        results = []

        try:
            team_rows = self.get_elements_by_xpath(Ranking.Stats.TEAM_ROW)
            self.logger.info(f"found {len(team_rows)} teams in ranking")

            for index, team in enumerate(team_rows, start=1):
                if index > self.top_n:
                    break

                team_name = self.get_text_by_xpath(Ranking.Stats.TEAM_NAME, element=team)
                team_url = self.get_text_by_xpath(Ranking.Stats.TEAM_URL, element=team)
                team_logo_url = self.get_text_by_xpath(
                    Ranking.Stats.TEAM_LOGO_URL,
                    element=team,
                )
                placement_text = self.get_text_by_xpath(
                    Ranking.Stats.PLACEMENT,
                    element=team,
                )
                points_text = self.get_text_by_xpath(
                    Ranking.Stats.HLTV_POINTS,
                    element=team,
                )
                lineup = self.__parse_ranking_lineup(team)

                team_id = extract_from_url(team_url, "id") if team_url else None
                placement = (
                    int(clear_number_str(placement_text))
                    if clear_number_str(placement_text)
                    else index
                )
                hltv_points = (
                    int(clear_number_str(points_text))
                    if clear_number_str(points_text)
                    else None
                )

                if not team_id or not team_name or not team_url:
                    continue

                results.append(
                    {
                        "id": str(team_id),
                        "name": team_name,
                        "url": self.__make_absolute_url(team_url),
                        "team_logo_url": self.__make_absolute_url(team_logo_url),
                        "lineup": lineup,
                        "placement": placement,
                        "hltv_points": hltv_points,
                    },
                )
        except Exception as e:
            self.logger.exception(f"error parsing top teams: {e}")

        return results

    def __parse_search_results(self) -> list[dict]:
        """
        Parse teams from search results.

        Returns:
            list[dict]: team dicts with id, name, country, url, team_logo_url, lineup.
        """
        results = []

        try:
            if not isinstance(self.page_data, list) or len(self.page_data) == 0:
                self.logger.warning("unexpected data structure or empty response")
                return []

            teams = self.page_data[0].get("teams", [])
            self.logger.info(f"found {len(teams)} teams for query '{self.query}'")

            for team_idx, team in enumerate(teams):
                try:
                    team_id = team.get("id")
                    if not team_id:
                        self.logger.debug(f"skipping team {team_idx}: missing id")
                        continue

                    name = team.get("name")
                    country = team.get("countryName")

                    location_path = team.get("location")
                    url = (
                        f"https://www.hltv.org{location_path}"
                        if location_path
                        else None
                    )

                    team_logo_url = team.get("teamLogoDay")

                    lineup = []
                    players = team.get("players", [])

                    for player_idx, player in enumerate(players):
                        try:
                            player_location = player.get("location")
                            player_id = (
                                extract_from_url(player_location, "id")
                                if player_location
                                else None
                            )

                            if not player_id:
                                self.logger.debug(
                                    f"skipping player {player_idx} in team {team_id}: missing id",
                                )
                                continue

                            first_name = player.get("firstName", "")
                            last_name = player.get("lastName", "")
                            full_name = f"{first_name} {last_name}".strip()

                            player_data = {
                                "id": player_id,
                                "nickname": player.get("nickName"),
                                "name": full_name or None,
                                "nationality": extract_country_name_from_flag_url(
                                    player.get("flagUrl"),
                                ),
                                "profile_url": f"https://www.hltv.org{player_location}"
                                if player_location
                                else None,
                            }
                            lineup.append(player_data)

                        except Exception as e:
                            self.logger.exception(
                                f"error parsing player {player_idx} in team {team_id}: {e}",
                            )
                            continue

                    team_data = {
                        "id": team_id,
                        "name": name,
                        "country": country,
                        "url": url,
                        "team_logo_url": team_logo_url,
                        "lineup": lineup,
                    }

                    results.append(team_data)

                except Exception as e:
                    self.logger.exception(f"error parsing team {team_idx}: {e}")
                    continue

            self.logger.info(
                f"successfully parsed {len(results)} teams with {sum(len(t['lineup']) for t in results)} players",
            )

        except Exception as e:
            self.logger.exception(f"error parsing search results: {e}")

        return results

    # ==================== PUBLIC METHODS ====================

    def get_teams(self) -> list[dict]:
        """
        Get a ranked list of teams.

        Returns:
            list[dict]: list of team dicts with id, name, country, url, team_logo_url, lineup, placement, and hltv_points.
        """
        try:
            if self.top_n is None:
                raise HTTPException(
                    status_code=400,
                    detail="top_n is required for team list requests",
                )

            return self.__parse_top_teams()
        except HTTPException:
            raise
        except Exception as e:
            self.logger.exception(f"error getting team list: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error getting team list: {e!s}",
            )

    def search_teams(self) -> dict:
        """
        Search teams and return formatted results.

        Returns:
            dict: query, results list, total count, and success flag.
        """
        try:
            results = self.__parse_search_results()

            self.response["query"] = self.query
            self.response["results"] = results
            self.response["total"] = len(results)
            self.response["success"] = True

            self.logger.info(
                f"search complete: {len(results)} teams found for '{self.query}'",
            )

        except Exception as e:
            self.logger.exception(f"error in search_teams: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error searching teams: {e!s}",
            )

        return self.response
