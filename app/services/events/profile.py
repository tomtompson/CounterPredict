# app/services/event_profile.py

from dataclasses import dataclass
from typing import List, Dict

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import extract_from_url, clear_number_str
from app.utils.xpath import Events


@dataclass
class HLTVEventProfile(HLTVBase):
    """
    class for getting event profile from hltv.
    
    attributes:
        event_id: hltv event id
    """
    
    event_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup event profile with event id."""
        super().__post_init__()
        
        self.URL = f"https://www.hltv.org/events/{self.event_id}/who"
        self.response["id"] = self.event_id
        
        self.logger.info(f"loading event profile for event {self.event_id}")
        
        self.page = self.request_url_page()
        
        self.logger.info(f"event page loaded for {self.event_id}")

    # ==================== PARSING METHODS ====================

    def __parse_event_profile(self) -> Dict:
        """
        parse event profile data from page.
        
        returns:
            dict with all event profile data (name, dates, teams, prize, location, mvp, evps)
        """
        self.logger.info("parsing event profile")
        
        try:
            event_name = self.get_text_by_xpath(Events.EventProfile.EVENT_NAME)
            team_count = self.get_text_by_xpath(Events.EventProfile.TEAM_COUNT)
            event_start_date = self.get_text_by_xpath(Events.EventProfile.EVENT_START_DATE)
            event_end_date = self.get_text_by_xpath(Events.EventProfile.EVENT_END_DATE)
            
            prize_pool = clear_number_str(self.get_text_by_xpath(Events.EventProfile.PRIZE_POOL))
            event_location = self.get_text_by_xpath(Events.EventProfile.EVENT_LOCATION)
            
            flag_suffix = self.get_text_by_xpath(Events.EventProfile.LOCATION_FLAG_URL)
            location_flag_url = f"https://www.hltv.org{flag_suffix}" if flag_suffix else None
            
            self.logger.debug(f"basic info: {event_name}, {event_location}, prize: {prize_pool}")
            
            mvp_list = None
            event_mvp_nickname = self.get_text_by_xpath(Events.EventProfile.EVENT_MVP_NICKNAME)
            event_mvp_url_suffix = self.get_text_by_xpath(Events.EventProfile.EVENT_MVP_URL)
            
            if event_mvp_nickname and event_mvp_url_suffix:
                event_mvp_url = f"https://www.hltv.org{event_mvp_url_suffix}"
                event_mvp_id = extract_from_url(event_mvp_url, 'id')
                
                mvp_list = [{
                    "id": event_mvp_id,
                    "nickname": event_mvp_nickname,
                    "event_stats": f"https://www.hltv.org/stats/players/{event_mvp_id}/who?event={self.event_id}"
                }]
                self.logger.debug(f"mvp: {event_mvp_nickname}")
            
            team_names = self.get_all_by_xpath(Events.EventProfile.TEAM_NAME)
            team_urls = self.get_all_by_xpath(Events.EventProfile.TEAM_URL)
            team_placements = self.get_all_by_xpath(Events.EventProfile.TEAM_PLACEMENT)
            
            self.logger.debug(f"found {len(team_names)} teams")
            
            team_list = []
            for i, (name, url, placement) in enumerate(zip(team_names, team_urls, team_placements)):
                try:
                    team_id = extract_from_url(url, 'id') if url else None
                    team_list.append({
                        "id": team_id,
                        "name": name,
                        "team_placement": placement
                    })
                except Exception as e:
                    self.logger.error(f"error parsing team {i}: {e}")
                    continue
            
            evp_nicknames = self.get_all_by_xpath(Events.EventProfile.EVENT_EVPS_NICKNAME)
            evp_urls = self.get_all_by_xpath(Events.EventProfile.EVENT_EVPS_URL)
            
            self.logger.debug(f"found {len(evp_nicknames)} evps")
            
            evps_list = []
            for i, (nickname, url) in enumerate(zip(evp_nicknames, evp_urls)):
                try:
                    evp_id = extract_from_url(url, 'id') if url else None
                    evps_list.append({
                        "id": evp_id,
                        "nickname": nickname,
                        "event_stats": f"https://www.hltv.org/stats/players/{evp_id}/who?event={self.event_id}"
                    })
                except Exception as e:
                    self.logger.error(f"error parsing evp {i}: {e}")
                    continue
            
            result = {
                "name": event_name,
                "start_date": event_start_date,
                "end_date": event_end_date,
                "teams": team_list,
                "team_count": team_count,
                "prize_pool": prize_pool,
                "location": event_location,
                "location_flag_url": location_flag_url,
                "mvp": mvp_list if mvp_list else None,
                "evps": evps_list if evps_list else None
            }
            
            self.logger.info(f"event profile parsed: {len(team_list)} teams, {len(evps_list)} evps")
            
            return result
            
        except Exception as e:
            self.logger.error(f"error parsing event profile: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error parsing event profile: {str(e)}"
            )

    # ==================== PUBLIC METHODS ====================

    def get_event_profile(self) -> dict:
        """
        get event profile data.
        
        returns:
            dict with event id and profile data
        """
        try:
            event_data = self.__parse_event_profile()
            
            self.response["id"] = self.event_id
            self.response["event_profile"] = event_data
            
            self.logger.info(f"returning profile for event {self.event_id}")
            
        except Exception as e:
            self.logger.error(f"error in get_event_profile: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error getting event profile: {str(e)}"
            )
        
        return self.response