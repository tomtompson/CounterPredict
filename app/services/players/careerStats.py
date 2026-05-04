from dataclasses import dataclass
from typing import Dict, Optional
from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import extract_float_from_percentage_number, parse_float, parse_int
from app.utils.xpath import Players


@dataclass
class HLTVPlayerCareerStats(HLTVBase):
    """
    class for getting career stats from a player profile.
    
    attributes:
        player_id: hltv player id
    """

    player_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup career stats with player id."""
        super().__post_init__()
        
        url = f"https://www.hltv.org/stats/players/{self.player_id}/who"
        self.URL = url
        self.response["id"] = self.player_id
        
        self.logger.info(f"loading career stats for player {self.player_id}")
        
        # load page
        self.page = self.request_url_page()
        
        # check if page is valid
        self.raise_exception_if_not_found(xpath=Players.Profile.URL)
        
        self.logger.info(f"career stats page loaded for player {self.player_id}")

    # ==================== PARSING METHODS ====================

    def __parse_career_stats(self) -> Dict:
        """
        parse career stats from player profile.
        
        returns:
            dict with all career stats
        """
        stats = {}
        
        try:
            self.logger.debug("parsing career stats")
            
            # basic stats
            stats["total_kills"] = parse_float(self.get_text_by_xpath(Players.careerStats.TOTAL_KILLS))
            stats["headshot_percentage"] = extract_float_from_percentage_number(
                self.get_text_by_xpath(Players.careerStats.HEADSHOT_PERCENTAGE)
            )
            stats["total_deaths"] = parse_float(self.get_text_by_xpath(Players.careerStats.TOTAL_DEATHS))
            stats["kd_ratio"] = parse_float(self.get_text_by_xpath(Players.careerStats.KD_RATIO))
            stats["damage_per_round"] = parse_float(self.get_text_by_xpath(Players.careerStats.DAMAGE_PER_ROUND))
            stats["grenade_dmg_per_round"] = parse_float(self.get_text_by_xpath(Players.careerStats.GRENADE_DMG_PER_ROUND))
            
            # match stats
            stats["maps_played"] = parse_int(self.get_text_by_xpath(Players.careerStats.MAPS_PLAYED))
            stats["rounds_played"] = parse_int(self.get_text_by_xpath(Players.careerStats.ROUNDS_PLAYED))
            
            # per round stats
            stats["kills_per_round"] = parse_float(self.get_text_by_xpath(Players.careerStats.KILLS_PER_ROUND))
            stats["assists_per_round"] = parse_float(self.get_text_by_xpath(Players.careerStats.ASSISTS_PER_ROUND))
            stats["deaths_per_round"] = parse_float(self.get_text_by_xpath(Players.careerStats.DEATHS_PER_ROUND))
            
            # teammate stats
            stats["saved_by_teammate_per_round"] = parse_float(self.get_text_by_xpath(Players.careerStats.SAVED_BY_TEAMMATE_PER_ROUND))
            stats["saved_teammates_per_round"] = parse_float(self.get_text_by_xpath(Players.careerStats.SAVED_TEAMMATES_PER_ROUND))
            
            # rating
            stats["rating_1_0"] = parse_float(self.get_text_by_xpath(Players.careerStats.RATING1_0))
            
            self.logger.debug("career stats parsed successfully")
            
        except Exception as e:
            self.logger.error(f"error parsing career stats: {e}")
            
        return stats

    # ==================== PUBLIC METHODS ====================

    def get_player_career_stats(self) -> dict:
        """
        get career stats for player.
        
        returns:
            dict with player id and career stats
        """
        try:
            career_stats = self.__parse_career_stats()
            
            self.response["id"] = self.player_id
            self.response["stats"] = career_stats
            
            self.logger.info(f"returning career stats for player {self.player_id}")
            
        except Exception as e:
            self.logger.error(f"error in get_player_career_stats: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error processing player career stats: {str(e)}"
            )
        
        return self.response