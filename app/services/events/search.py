# app/services/events_search.py

from dataclasses import dataclass
from typing import List, Dict

from fastapi import HTTPException

from app.services.base import HLTVBase


@dataclass
class HLTVEventsSearch(HLTVBase):
    """
    class for searching events on hltv.
    
    attributes:
        query: search term for events
    """

    query: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup event search with query."""
        super().__post_init__()
        
        self.URL = f"https://www.hltv.org/search?term={self.query}"
        self.response["query"] = self.query
        
        self.logger.info(f"searching events with query: {self.query}")
        
        self.page_data = self.__fetch_json()
        
        self.logger.info("event search data fetched successfully")

    # ==================== PRIVATE METHODS ====================

    def __fetch_json(self) -> dict:
        """
        make get request and return json response.
        
        returns:
            dict: raw json data from hltv search
            
        raises:
            http exception if request fails
        """
        try:
            self.logger.debug(f"fetching json from {self.URL}")
            
            res = self.make_request(self.URL)
            
            self.logger.debug(f"response status: {res.status_code}")
            
            data = res.json()
            self.logger.debug("json data received")
            
            return data
            
        except Exception as e:
            self.logger.error(f"error fetching json: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error fetching event search data: {str(e)}"
            )

    # ==================== PARSING METHODS ====================

    def __parse_search_results(self) -> List[Dict]:
        """
        parse events from search results.
        
        returns:
            list of event dictionaries with id, name, url, event_location,
            prize_pool, flag_url, event_logo_url, event_type, event_matches_url
        """
        results = []
        
        try:
            if not isinstance(self.page_data, list) or len(self.page_data) == 0:
                self.logger.warning("unexpected data structure or empty response")
                return []
            
            events = self.page_data[0].get("events", [])
            self.logger.info(f"found {len(events)} events for query '{self.query}'")
            
            for idx, event in enumerate(events):
                try:
                    event_id = event.get("id")
                    if not event_id:
                        self.logger.debug(f"skipping event {idx}: missing id")
                        continue
                    
                    name = event.get("name")
                    location_path = event.get("location")
                    url = f"https://www.hltv.org{location_path}" if location_path else None
                    
                    event_location = event.get("physicalLocation")
                    prize_pool = event.get("prizePool")
                    flag_url = event.get("flagUrl")
                    event_logo_url = event.get("eventLogo")
                    event_type = event.get("eventType")
                    
                    matches_path = event.get("eventMatchesLocation")
                    event_matches_url = f"https://www.hltv.org{matches_path}" if matches_path else None
                    
                    event_data = {
                        "id": str(event_id),
                        "name": name,
                        "url": url,
                        "event_location": event_location,
                        "prize_pool": prize_pool,
                        "flag_url": flag_url,
                        "event_logo_url": event_logo_url,
                        "event_type": event_type,
                        "event_matches_url": event_matches_url
                    }
                    
                    results.append(event_data)
                    
                except Exception as e:
                    self.logger.error(f"error parsing event {idx}: {e}")
                    continue
                    
            self.logger.info(f"successfully parsed {len(results)} events")
            
        except Exception as e:
            self.logger.error(f"error parsing search results: {e}")
            
        return results

    # ==================== PUBLIC METHODS ====================

    def search_events(self) -> dict:
        """
        search events and return formatted results.
        
        returns:
            dict with query, results list, total count and success flag
        """
        try:
            results = self.__parse_search_results()
            
            self.response["query"] = self.query
            self.response["results"] = results
            self.response["total"] = len(results)
            self.response["success"] = True
            
            self.logger.info(f"search complete: {len(results)} events found for '{self.query}'")
            
        except Exception as e:
            self.logger.error(f"error in search_events: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error searching events: {str(e)}"
            )
        
        return self.response