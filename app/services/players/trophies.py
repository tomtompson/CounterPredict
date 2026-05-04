# app/services/players_trophies.py

from dataclasses import dataclass
from typing import List, Dict

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import trim, extract_from_url
from app.utils.xpath import Players


@dataclass
class HLTVPlayersTrophies(HLTVBase):
    """
    class for getting personal trophies from a player profile.
    
    attributes:
        player_id: hltv player id
    """
    
    player_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup trophies with player id."""
        super().__post_init__()
        
        self.URL = f"https://www.hltv.org/player/{self.player_id}/who#tab-trophiesBox"
        self.response["id"] = self.player_id
        
        self.logger.info(f"loading trophies for player {self.player_id}")
        
        self.page = self.request_url_page()
        
        self.raise_exception_if_not_found(xpath=Players.Profile.URL)
        
        self.logger.info(f"page loaded for player {self.player_id}")

    # ==================== PARSING METHODS ====================

    def __parse_player_trophies(self) -> List[Dict]:
        """
        parse personal trophies from player profile.
        
        returns:
            list of trophy dictionaries
        """
        trophies_data = []
        
        try:
            tournament_names = self.get_all_by_xpath(Players.Trophies.TOURNAMENT_NAME)
            trophy_images = self.get_all_by_xpath(Players.Trophies.TROPHY_IMG_URL)
            tournament_urls = self.get_all_by_xpath(Players.Trophies.TOURNAMENT_URL)
            
            self.logger.info(f"found {len(tournament_names)} trophies")
            self.logger.debug(f"images: {len(trophy_images)}, urls: {len(tournament_urls)}")
            
            tournament_ids = []
            for url in tournament_urls:
                try:
                    tid = extract_from_url(url, "id")
                    tournament_ids.append(tid)
                except Exception as e:
                    self.logger.error(f"error extracting id from url {url}: {e}")
                    tournament_ids.append(None)
            
            for i, (name, img_url, url, tid) in enumerate(zip(
                tournament_names, trophy_images, tournament_urls, tournament_ids
            )):
                try:
                    trophy = {
                        "tournament_name": trim(name) if name else None,
                        "tournament_img_url": f"https://www.hltv.org{img_url}" if img_url else None,
                        "tournament_url": f"https://www.hltv.org{url}" if url else None,
                        "tournament_id": tid if tid else None
                    }
                    trophies_data.append(trophy)
                except Exception as e:
                    self.logger.error(f"error building trophy {i}: {e}")
                    continue
            
            self.logger.info(f"successfully parsed {len(trophies_data)} trophies")
            
        except Exception as e:
            self.logger.error(f"error parsing trophies: {e}")
            
        return trophies_data

    # ==================== PUBLIC METHODS ====================

    def get_player_trophies(self) -> dict:
        """
        get personal trophies for player.
        
        returns:
            dict with player id and trophies list
        """
        try:
            trophies = self.__parse_player_trophies()
            
            self.response["id"] = self.player_id
            self.response["trophy_count"] = len(trophies)
            self.response["trophies"] = trophies
            
            self.logger.info(f"returning {len(trophies)} trophies for player {self.player_id}")
            
        except Exception as e:
            self.logger.error(f"error in get_player_trophies: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error processing player trophies: {str(e)}"
            )
        
        return self.response