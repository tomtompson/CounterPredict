# app/services/ranking_stats.py

from dataclasses import dataclass
from typing import List, Dict, Optional

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import extract_from_url, parse_date, clear_number_str
from app.utils.xpath import Ranking


@dataclass
class HLTVRankingStats(HLTVBase):
    """
    class for getting hltv world ranking stats.
    
    attributes:
        start_placement: first placement to include (1-based)
        end_placement: last placement to include
    """
    
    start_placement: int
    end_placement: int

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup ranking stats with placement range."""
        super().__post_init__()
        
        self.URL = "https://www.hltv.org/ranking/teams"
        
        self.logger.info(f"loading ranking stats for placements {self.start_placement} to {self.end_placement}")
        
        if self.start_placement < 1 or self.end_placement < self.start_placement:
            self.logger.error(f"invalid placement range: {self.start_placement} - {self.end_placement}")
            raise HTTPException(
                status_code=400,
                detail=f"invalid placement range: start must be >= 1 and end must be >= start"
            )
        
        self.page = self.request_url_page()
        
        self.logger.info("ranking page loaded successfully")

    # ==================== PRIVATE METHODS ====================

    def _make_absolute_url(self, url: Optional[str]) -> Optional[str]:
        """
        convert relative url to absolute url.
        
        args:
            url: relative or absolute url
            
        returns:
            absolute url or None
        """
        if not url:
            return None
        if url.startswith('http'):
            return url
        elif url.startswith('/'):
            return f"https://www.hltv.org{url}"
        else:
            return url

    # ==================== PARSING METHODS ====================

    def __parse_team_lineup(self, team_element) -> List[Dict]:
        """
        parse team lineup from ranking.
        
        args:
            team_element: lxml element for the team
            
        returns:
            list of player dictionaries with player_id, nickname, nationality, picture_url
        """
        lineup = []
        
        try:
            player_rows = self.get_elements_by_xpath(Ranking.Stats.PLAYER_ROW, element=team_element)
            self.logger.debug(f"found {len(player_rows)} players in lineup")
            
            for player_idx, player in enumerate(player_rows):
                try:
                    player_nickname = self.get_text_by_xpath(Ranking.Stats.PLAYER_NICKNAME, element=player)
                    player_url = self.get_text_by_xpath(Ranking.Stats.PLAYER_URL, element=player)
                    player_nationality = self.get_text_by_xpath(Ranking.Stats.PLAYER_NATIONALITY, element=player)
                    
                    player_picture_rel = self.get_text_by_xpath(Ranking.Stats.PLAYER_PICTURE_URL, element=player)
                    player_picture_abs = self._make_absolute_url(player_picture_rel)
                    
                    player_id = extract_from_url(player_url, 'id') if player_url else None
                    
                    if player_id and player_nickname:
                        lineup.append({
                            "player_id": player_id,
                            "nickname": player_nickname,
                            "nationality": player_nationality,
                            "picture_url": player_picture_abs
                        })
                    else:
                        self.logger.debug(f"skipping player {player_idx}: missing id or nickname")
                except Exception as e:
                    self.logger.error(f"error parsing player {player_idx}: {e}")
                    continue
        except Exception as e:
            self.logger.error(f"error parsing team lineup: {e}")
            
        return lineup

    def __parse_ranking_stats(self) -> List[Dict]:
        """
        parse ranking stats within placement range.
        
        returns:
            list of team ranking dictionaries with team_id, team_name, placement, hltv_points, logo_url, lineup
        """
        ranking_data = []
        
        try:
            team_rows = self.get_elements_by_xpath(Ranking.Stats.TEAM_ROW)
            self.logger.info(f"found {len(team_rows)} teams in ranking")
            
            for index, team in enumerate(team_rows, start=1):
                if index < self.start_placement or index > self.end_placement:
                    continue
                    
                self.logger.debug(f"processing team at placement {index}")
                
                try:
                    team_name = self.get_text_by_xpath(Ranking.Stats.TEAM_NAME, element=team)
                    team_url = self.get_text_by_xpath(Ranking.Stats.TEAM_URL, element=team)
                    
                    team_logo_rel = self.get_text_by_xpath(Ranking.Stats.TEAM_LOGO_URL, element=team)
                    team_logo_abs = self._make_absolute_url(team_logo_rel)
                    
                    placement_text = self.get_text_by_xpath(Ranking.Stats.PLACEMENT, element=team)
                    placement = clear_number_str(placement_text) if placement_text else index
                    
                    hltv_points = clear_number_str(
                        self.get_text_by_xpath(Ranking.Stats.HLTV_POINTS, element=team)
                    )
                    
                    team_id = extract_from_url(team_url, 'id') if team_url else None
                    
                    if not team_id or not team_name:
                        self.logger.warning(f"skipping team {index}: missing id or name")
                        continue
                    
                    lineup = self.__parse_team_lineup(team)
                    
                    team_data = {
                        "team_id": team_id,
                        "team_name": team_name,
                        "placement": placement,
                        "hltv_points": hltv_points,
                        "logo_url": team_logo_abs,
                        "lineup": lineup
                    }
                    
                    ranking_data.append(team_data)
                    self.logger.debug(f"added team {team_name} at position {placement}")
                except Exception as e:
                    self.logger.error(f"error parsing team at index {index}: {e}")
                    continue
            
            self.logger.info(f"parsed {len(ranking_data)} teams in range {self.start_placement}-{self.end_placement}")
            
        except Exception as e:
            self.logger.error(f"error parsing ranking stats: {e}")
            
        return ranking_data

    # ==================== PUBLIC METHODS ====================

    def get_ranking_stats(self) -> dict:
        """
        get ranking stats for specified placement range.
        
        returns:
            dict with start_placement, end_placement, ranking_date, ranking_stats, total_teams
        """
        try:
            ranking_date_raw = self.get_text_by_xpath(Ranking.Stats.RANKING_DATE)
            ranking_date = parse_date(ranking_date_raw) if ranking_date_raw else None
            
            ranking_data = self.__parse_ranking_stats()
            
            self.response["start_placement"] = self.start_placement
            self.response["end_placement"] = self.end_placement
            self.response["ranking_date"] = ranking_date
            self.response["ranking_stats"] = ranking_data
            self.response["total_teams"] = len(ranking_data)
            
            self.logger.info(f"returning ranking stats for placements {self.start_placement}-{self.end_placement} ({len(ranking_data)} teams)")
            
        except Exception as e:
            self.logger.error(f"error in get_ranking_stats: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error getting ranking stats: {str(e)}"
            )
        
        return self.response