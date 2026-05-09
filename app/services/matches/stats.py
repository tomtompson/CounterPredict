# app/services/matches/stats.py

from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import extract_from_url, parse_float,extract_float_from_percentage_number
from app.xpaths import Matches


@dataclass
class HLTVMatchStats(HLTVBase):
    """Class for getting detailed match statistics from HLTV.

    Attributes:
        match_id: HLTV match ID
    """

    match_id: int

    def __post_init__(self) -> None:
        """Set up match stats with match ID."""
        super().__post_init__()

        self.URL = f"https://www.hltv.org/matches/{self.match_id}/na-vs-na"

        self.logger.info(f"loading match stats for match {self.match_id}")

        self.page = self.request_url_page()

        self.logger.info(f"match page loaded for {self.match_id}")

    def __parse_match_info(self) -> dict:
        """
        Parse basic match information (teams, scores, date, event).

        Returns:
            dict: match info with team names, IDs, scores, date, and event details.
        """
        try:
            team1_name = self.get_text_by_xpath(Matches.MatchStats.TEAM1_NAME)
            team1_id = self.get_text_by_xpath(Matches.MatchStats.TEAM1_ID)
            team1_id = extract_from_url(team1_id, "id") if team1_id else None
            team1_score = self.get_text_by_xpath(Matches.MatchStats.TEAM1_SCORE)

            team2_name = self.get_text_by_xpath(Matches.MatchStats.TEAM2_NAME)
            team2_id = self.get_text_by_xpath(Matches.MatchStats.TEAM2_ID)
            team2_id = extract_from_url(team2_id, "id") if team2_id else None
            team2_score = self.get_text_by_xpath(Matches.MatchStats.TEAM2_SCORE)

            match_date = self.get_text_by_xpath(Matches.MatchStats.MATCH_DATE)
            match_time = self.get_text_by_xpath(Matches.MatchStats.MATCH_TIME)
            unix_timestamp = self.get_text_by_xpath(Matches.MatchStats.UNIX_TIMESTAMP)
            event_name = self.get_text_by_xpath(Matches.MatchStats.EVENT_NAME)
            event_id = self.get_text_by_xpath(Matches.MatchStats.EVENT_ID)
            event_id = extract_from_url(event_id, "id") if event_id else None

            self.logger.debug(
                f"match info: {team1_name} vs {team2_name}, score: {team1_score}-{team2_score}",
            )

            return {
                "team1": {
                    "name": team1_name or "",
                    "id": team1_id,
                    "score": team1_score or "0",
                },
                "team2": {
                    "name": team2_name or "",
                    "id": team2_id,
                    "score": team2_score or "0",
                },
                "match_date": match_date,
                "match_time": match_time,
                "unix_timestamp": unix_timestamp,
                "event": {
                    "name": event_name,
                    "id": event_id,
                },
            }

        except Exception as e:
            self.logger.exception(f"error parsing match info: {e}")
            return {
                "team1": {"name": "", "id": None, "score": "0"},
                "team2": {"name": "", "id": None, "score": "0"},
                "match_date": None,
                "match_time": None,
                "unix_timestamp": None,
                "event": {"name": None, "id": None},
            }

    def __parse_map_pool(self) -> list[str]:
        """
        Parse the map pool for the series.

        Returns:
            list[str]: list of map names in the series.
        """
        try:
            maps = self.get_all_by_xpath(Matches.MatchStats.MAP_POOL)
            self.logger.debug(f"found {len(maps)} maps: {maps}")
            return maps
        except Exception as e:
            self.logger.exception(f"error parsing map pool: {e}")
            return []

    def __parse_map_score(self, map_num: int) -> tuple[dict, dict]:
        """
        Parse the score for a specific map (1-based index).

        Args:
            map_num (int): map number (1-5).

        Returns:
            tuple[dict, dict]: (team1_score, team2_score) dicts with score/ct/tr keys.
        """
        xpaths = {
            1: (
                Matches.MatchStats.MAP1_TEAM1_SCORE,
                Matches.MatchStats.MAP1_TEAM1_CT,
                Matches.MatchStats.MAP1_TEAM1_TR,
                Matches.MatchStats.MAP1_TEAM2_SCORE,
                Matches.MatchStats.MAP1_TEAM2_CT,
                Matches.MatchStats.MAP1_TEAM2_TR,
            ),
            2: (
                Matches.MatchStats.MAP2_TEAM1_SCORE,
                Matches.MatchStats.MAP2_TEAM1_CT,
                Matches.MatchStats.MAP2_TEAM1_TR,
                Matches.MatchStats.MAP2_TEAM2_SCORE,
                Matches.MatchStats.MAP2_TEAM2_CT,
                Matches.MatchStats.MAP2_TEAM2_TR,
            ),
            3: (
                Matches.MatchStats.MAP3_TEAM1_SCORE,
                Matches.MatchStats.MAP3_TEAM1_CT,
                Matches.MatchStats.MAP3_TEAM1_TR,
                Matches.MatchStats.MAP3_TEAM2_SCORE,
                Matches.MatchStats.MAP3_TEAM2_CT,
                Matches.MatchStats.MAP3_TEAM2_TR,
            ),
            4: (
                Matches.MatchStats.MAP4_TEAM1_SCORE,
                Matches.MatchStats.MAP4_TEAM1_CT,
                Matches.MatchStats.MAP4_TEAM1_TR,
                Matches.MatchStats.MAP4_TEAM2_SCORE,
                Matches.MatchStats.MAP4_TEAM2_CT,
                Matches.MatchStats.MAP4_TEAM2_TR,
            ),
            5: (
                Matches.MatchStats.MAP5_TEAM1_SCORE,
                Matches.MatchStats.MAP5_TEAM1_CT,
                Matches.MatchStats.MAP5_TEAM1_TR,
                Matches.MatchStats.MAP5_TEAM2_SCORE,
                Matches.MatchStats.MAP5_TEAM2_CT,
                Matches.MatchStats.MAP5_TEAM2_TR,
            ),
        }

        if map_num not in xpaths:
            empty: dict = {"score": None, "ct": None, "tr": None}
            return empty, empty

        t1s, t1c, t1t, t2s, t2c, t2t = xpaths[map_num]
        return (
            {
                "score": self.get_text_by_xpath(t1s),
                "ct": self.get_text_by_xpath(t1c),
                "tr": self.get_text_by_xpath(t1t),
            },
            {
                "score": self.get_text_by_xpath(t2s),
                "ct": self.get_text_by_xpath(t2c),
                "tr": self.get_text_by_xpath(t2t),
            },
        )

    def __parse_player_stats_by_map(self, map_names: list[str]) -> list[dict]:
        """
        Parse player statistics for each map and side (CT/T).

        Args:
            map_names (list[str]): list of map names ordered by map index.

        Returns:
            list[dict]: list of map stats dicts with team1/team2 side stats.
        """
        map_stats_list = []

        try:
            map_containers = self.get_elements_by_xpath(
                Matches.MatchStats.MAP_CONTAINERS
            )
            self.logger.debug(f"found {len(map_containers)} map containers")

            for map_idx, map_container in enumerate(map_containers):
                try:
                    map_name = map_names[map_idx] if map_idx < len(map_names) else None
                    team1_score, team2_score = self.__parse_map_score(map_idx + 1)
                    raw_id = map_container.get("id", "")
                    map_stats_id = raw_id.replace("-content", "") if raw_id else None
                    map_stats = self.__parse_single_map_stats(
                        map_container,
                        map_idx,
                        map_name,
                        map_stats_id,
                        team1_score,
                        team2_score,
                    )
                    if map_stats:
                        map_stats_list.append(map_stats)
                except Exception as e:
                    self.logger.exception(f"error parsing map {map_idx} stats: {e}")
                    continue

        except Exception as e:
            self.logger.exception(f"error parsing player stats by map: {e}")

        return map_stats_list

    def __parse_single_map_stats(
        self,
        map_element,
        map_idx: int,
        map_name: str | None,
        map_stats_id: str | None,
        team1_score: dict,
        team2_score: dict,
    ) -> dict | None:
        """
        Parse statistics for a single map.

        Args:
            map_element: lxml element for the map container.
            map_idx (int): map index (0-based).
            map_name (str | None): name of the map.
            map_stats_id (str | None): HLTV map stats ID.
            team1_score (dict): team1 score with score/ct/tr keys.
            team2_score (dict): team2 score with score/ct/tr keys.

        Returns:
            dict | None: map stats dict with team1 and team2 player stats by side.
        """
        try:
            ct_t1 = self.__parse_team_side_stats(
                map_element,
                Matches.MatchStats.TEAM1_CT_PLAYER_NICK,
                Matches.MatchStats.TEAM1_CT_PLAYER_ID,
                Matches.MatchStats.TEAM1_CT_PLAYER_KD,
                Matches.MatchStats.TEAM1_CT_PLAYER_SWING,
                Matches.MatchStats.TEAM1_CT_PLAYER_ADR,
                Matches.MatchStats.TEAM1_CT_PLAYER_KAST,
                Matches.MatchStats.TEAM1_CT_PLAYER_RATING,
                "ct",
            )
            t_t1 = self.__parse_team_side_stats(
                map_element,
                Matches.MatchStats.TEAM1_T_PLAYER_NICK,
                Matches.MatchStats.TEAM1_T_PLAYER_ID,
                Matches.MatchStats.TEAM1_T_PLAYER_KD,
                Matches.MatchStats.TEAM1_T_PLAYER_SWING,
                Matches.MatchStats.TEAM1_T_PLAYER_ADR,
                Matches.MatchStats.TEAM1_T_PLAYER_KAST,
                Matches.MatchStats.TEAM1_T_PLAYER_RATING,
                "t",
            )
            ct_t2 = self.__parse_team_side_stats(
                map_element,
                Matches.MatchStats.TEAM2_CT_PLAYER_NICK,
                Matches.MatchStats.TEAM2_CT_PLAYER_ID,
                Matches.MatchStats.TEAM2_CT_PLAYER_KD,
                Matches.MatchStats.TEAM2_CT_PLAYER_SWING,
                Matches.MatchStats.TEAM2_CT_PLAYER_ADR,
                Matches.MatchStats.TEAM2_CT_PLAYER_KAST,
                Matches.MatchStats.TEAM2_CT_PLAYER_RATING,
                "ct",
            )
            t_t2 = self.__parse_team_side_stats(
                map_element,
                Matches.MatchStats.TEAM2_T_PLAYER_NICK,
                Matches.MatchStats.TEAM2_T_PLAYER_ID,
                Matches.MatchStats.TEAM2_T_PLAYER_KD,
                Matches.MatchStats.TEAM2_T_PLAYER_SWING,
                Matches.MatchStats.TEAM2_T_PLAYER_ADR,
                Matches.MatchStats.TEAM2_T_PLAYER_KAST,
                Matches.MatchStats.TEAM2_T_PLAYER_RATING,
                "t",
            )

            self.logger.debug(
                f"map {map_idx} ({map_name}): T1 CT={len(ct_t1)}, T1 T={len(t_t1)}, "
                f"T2 CT={len(ct_t2)}, T2 T={len(t_t2)}",
            )

            return {
                "map_index": map_idx,
                "map_stats_id": map_stats_id,
                "map_name": map_name,
                "team1_score": team1_score,
                "team2_score": team2_score,
                "team1": {"ct_side": ct_t1, "t_side": t_t1},
                "team2": {"ct_side": ct_t2, "t_side": t_t2},
            }

        except Exception as e:
            self.logger.exception(f"error parsing single map stats: {e}")
            return None

    def __parse_team_side_stats(
        self,
        map_element,
        nick_xpath: str,
        id_xpath: str,
        kd_xpath: str,
        swing_xpath: str,
        adr_xpath: str,
        kast_xpath: str,
        rating_xpath: str,
        side: str,
    ) -> list[dict]:
        """
        Parse player stats for a specific team and side.

        Args:
            map_element: lxml element for the map.
            nick_xpath (str): XPath for player nickname.
            id_xpath (str): XPath for player href.
            kd_xpath (str): XPath for K/D ratio.
            swing_xpath (str): XPath for swing stat.
            adr_xpath (str): XPath for ADR.
            kast_xpath (str): XPath for KAST.
            rating_xpath (str): XPath for rating.
            side (str): "ct" or "t".

        Returns:
            list[dict]: list of player stats dicts.
        """
        players_stats = []

        try:
            nick_list = self.get_all_by_xpath(nick_xpath, element=map_element)
            id_list = self.get_all_by_xpath(id_xpath, element=map_element)
            kd_list = self.get_all_by_xpath(kd_xpath, element=map_element)
            swing_list = self.get_all_by_xpath(swing_xpath, element=map_element)
            adr_list = self.get_all_by_xpath(adr_xpath, element=map_element)
            kast_list = self.get_all_by_xpath(kast_xpath, element=map_element)
            rating_list = self.get_all_by_xpath(rating_xpath, element=map_element)

            for idx, (nick, player_id, kd, swing, adr, kast, rating) in enumerate(
                zip(
                    nick_list,
                    id_list,
                    kd_list,
                    swing_list,
                    adr_list,
                    kast_list,
                    rating_list,
                    strict=False,
                ),
            ):
                player_id_clean = (
                    extract_from_url(player_id, "id") if player_id else None
                )
                adr_float = parse_float(adr) if adr else None
                rating_float = parse_float(rating) if rating else None
                swing_float = extract_float_from_percentage_number(swing) if swing else None
                kast_float = extract_float_from_percentage_number(kast) if kast else None
                players_stats.append(
                    {
                
                        "side": side,
                        "nickname": nick or "",
                        "id": player_id_clean,
                        "kd": kd or "",
                        "swing": swing_float,
                        "adr": adr_float,
                        "kast": kast_float,
                        "rating": rating_float,
                    }
                )

            self.logger.debug(f"parsed {len(players_stats)} players for {side} side")

        except Exception as e:
            self.logger.exception(f"error parsing team side stats ({side}): {e}")

        return players_stats

    def __parse_all_match_stats(self) -> dict:
        """
        Parse all match statistics.

        Returns:
            dict: complete match stats with info, maps, and player stats.
        """
        self.logger.info(f"parsing all stats for match {self.match_id}")

        try:
            match_info = self.__parse_match_info()
            map_pool = self.__parse_map_pool()
            map_stats = self.__parse_player_stats_by_map(map_pool)

            self.logger.info(
                f"stats parsed: {len(map_pool)} maps, {len(map_stats)} map stats entries",
            )
            return {
                "match_info": match_info,
                "map_pool": map_pool,
                "map_stats": map_stats,
            }

        except Exception as e:
            self.logger.exception(f"error parsing all match stats: {e}")
            return {
                "match_info": {
                    "team1": {"name": "", "id": None, "score": "0"},
                    "team2": {"name": "", "id": None, "score": "0"},
                    "match_date": None,
                    "match_time": None,
                    "unix_timestamp": None,
                    "event": {"name": None, "id": None},
                },
                "map_pool": [],
                "map_stats": [],
            }

    def get_match_stats(self) -> dict:
        """
        Get complete match statistics.

        Returns:
            dict: match_id and detailed stats including teams, maps, and player performance.
        """
        try:
            has_stats = bool(self.get_elements_by_xpath(Matches.MatchStats.HAS_STATS))

            if not has_stats:
                raise HTTPException(
                    status_code=425,
                    detail=f"match {self.match_id} has not started yet — no stats available",
                )

            has_score = bool(self.get_elements_by_xpath(Matches.MatchStats.WITH_SCORE))
            is_live = not has_score

            match_stats = self.__parse_all_match_stats()

            self.response["match_id"] = self.match_id
            self.response["match_url"] = self.get_text_by_xpath(Matches.MatchStats.URL)
            self.response["is_live"] = is_live
            self.response["stats"] = match_stats

            self.logger.info(f"match stats retrieved successfully for {self.match_id}")
            return self.response

        except HTTPException:
            raise
        except Exception as e:
            self.logger.exception(f"error getting match stats: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"failed to retrieve match stats: {e!s}",
            )
