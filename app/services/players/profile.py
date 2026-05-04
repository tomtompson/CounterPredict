# app/services/player_profile.py

from dataclasses import dataclass, field

from app.services.base import HLTVBase
from app.utils.utils import extract_age
from app.utils.xpath import Players
from fastapi import HTTPException


@dataclass
class HLTVPlayerProfile(HLTVBase):
    """
    class for getting and parsing player profile from hltv.
    
    attributes:
        player_id: hltv player id
    """
    
    player_id: str = field()

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup profile with player id."""
        super().__post_init__()
        
        self.URL = f"https://www.hltv.org/player/{self.player_id}/who"
        self.response["id"] = self.player_id
        
        self.logger.info(f"loading profile for player {self.player_id}")
        self.page = self.request_url_page()
        self.logger.info(f"profile page loaded for player {self.player_id}")

    # ==================== PARSING METHODS ====================

    def get_player_profile(self) -> dict:
        """
        extract player profile data using xpaths.
        
        returns:
            dict with player info (nickname, name, age, nationality, rating, etc.)
        """
        try:
            nickname = self.get_text_by_xpath(Players.Profile.NICKNAME)
            self.response["nickname"] = nickname
            
            name = self.get_text_by_xpath(Players.Profile.NAME)
            self.response["name"] = name
            
            age_text = self.get_text_by_xpath(Players.Profile.AGE)
            self.response["age"] = extract_age(age_text) if age_text else None
            
            nationality = self.get_text_by_xpath(Players.Profile.NATIONALITY)
            self.response["nationality"] = nationality
            
            rating = self.get_text_by_xpath(Players.Profile.RATING)
            self.response["rating"] = rating
            
            current_team = self.get_text_by_xpath(Players.Profile.CURRENT_TEAM)
            self.response["current_team"] = current_team
            
            team_url = self.get_text_by_xpath(Players.Profile.CURRENT_TEAM_URL)
            self.response["current_team_url"] = f"https://www.hltv.org{team_url}" if team_url else None
            
            image_url = self.get_text_by_xpath(Players.Profile.IMAGE_URL)
            self.response["image_url"] = image_url
            
            profile_url = self.get_text_by_xpath(Players.Profile.URL)
            self.response["url"] = profile_url if profile_url else self.URL
            
            social_media = self.get_all_by_xpath(Players.Profile.SOCIAL_MEDIA)
            self.response["social_media"] = social_media or []
            
            if nickname:
                self.logger.info(f"profile extracted: {nickname}")
            else:
                self.logger.warning("profile parsed but nickname not found")
            
        except Exception as e:
            self.logger.error(f"error parsing profile: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error parsing player profile: {str(e)}"
            )
        
        return self.response