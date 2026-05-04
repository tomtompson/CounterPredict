# app/services/team_achievements.py

from dataclasses import dataclass
from typing import List, Dict

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import extract_from_url, trim
from app.utils.xpath import Teams


@dataclass
class HLTVTeamAchievements(HLTVBase):
    """
    class for getting team achievements from hltv.
    
    attributes:
        team_id: hltv team id
    """
    
    team_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup team achievements with team id."""
        super().__post_init__()
        
        self.URL = f"https://www.hltv.org/team/{self.team_id}/who#tab-achievementsBox"
        self.response["id"] = self.team_id
        
        self.logger.info(f"loading achievements for team {self.team_id}")
        
        self.page = self.request_url_page()
        
        self.logger.info(f"team page loaded for {self.team_id}")

    # ==================== PARSING METHODS ====================

    def __parse_team_achievements(self) -> List[Dict]:
        """
        parse team achievements from page.
        
        returns:
            list of achievement dictionaries with id, tournament_name, placement, team_event_stats
        """
        achievements = []
        
        try:
            self.logger.debug("parsing team achievements")
            
            placements = self.get_all_by_xpath(Teams.Achievements.PLACEMENT)
            tournament_names = self.get_all_by_xpath(Teams.Achievements.TOURNAMENT_NAME)
            tournament_urls = self.get_all_by_xpath(Teams.Achievements.TOURNAMENT_URL)
            
            self.logger.debug(f"found {len(placements)} placements, {len(tournament_names)} tournaments")
            
            min_length = min(len(placements), len(tournament_names), len(tournament_urls))
            
            if min_length == 0:
                self.logger.info(f"no achievements found for team {self.team_id}")
                return []
            
            if len(placements) != len(tournament_names) or len(placements) != len(tournament_urls):
                self.logger.warning(f"data length mismatch: placements={len(placements)}, names={len(tournament_names)}, urls={len(tournament_urls)}")
            
            for i in range(min_length):
                try:
                    placement = trim(placements[i]) if i < len(placements) else None
                    name = trim(tournament_names[i]) if i < len(tournament_names) else None
                    url = trim(tournament_urls[i]) if i < len(tournament_urls) else None
                    
                    tournament_id = extract_from_url(url, 'id') if url else None
                    
                    if not tournament_id or not name:
                        self.logger.debug(f"skipping achievement {i}: missing data")
                        continue
                    
                    achievement = {
                        "id": tournament_id,
                        "tournament_name": name,
                        "placement": placement,
                        "team_event_stats": f"https://www.hltv.org/stats/teams/{self.team_id}/who?event={tournament_id}"
                    }
                    
                    achievements.append(achievement)
                except Exception as e:
                    self.logger.error(f"error parsing achievement {i}: {e}")
                    continue
            
            self.logger.info(f"parsed {len(achievements)} achievements for team {self.team_id}")
            
        except Exception as e:
            self.logger.error(f"error parsing team achievements: {e}")
            
        return achievements

    # ==================== PUBLIC METHODS ====================

    def get_team_achievements(self) -> dict:
        """
        get team achievements.
        
        returns:
            dict with team id, achievements list and achievement count
        """
        try:
            achievements = self.__parse_team_achievements()
            
            self.response["id"] = self.team_id
            self.response["achievement_count"] = len(achievements)
            self.response["team_achievements"] = achievements
            
            self.logger.info(f"returning {len(achievements)} achievements for team {self.team_id}")
            
        except Exception as e:
            self.logger.error(f"error in get_team_achievements: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error getting team achievements: {str(e)}"
            )
        
        return self.response