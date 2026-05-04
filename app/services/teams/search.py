# app/services/team_search.py

from dataclasses import dataclass
from typing import List, Dict

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import extract_country_name_from_flag_url, extract_from_url


@dataclass
class HLTVTeamSearch(HLTVBase):
    """
    class for searching teams on hltv.
    
    attributes:
        query: search term for teams
    """
    
    query: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup team search with query."""
        super().__post_init__()
        
        self.URL = f"https://www.hltv.org/search?term={self.query}"
        self.response["query"] = self.query
        
        self.logger.info(f"searching teams with query: {self.query}")
        
        self.page_data = self.__fetch_json()
        
        self.logger.info("team search data fetched successfully")

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
                detail=f"error fetching team search data: {str(e)}"
            )

    # ==================== PARSING METHODS ====================

    def __parse_search_results(self) -> List[Dict]:
        """
        parse teams from search results.
        
        returns:
            list of team dictionaries with id, name, country, url,
            team_logo_url and lineup (list of players)
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
                    url = f"https://www.hltv.org{location_path}" if location_path else None
                    
                    team_logo_url = team.get("teamLogoDay")
                    
                    lineup = []
                    players = team.get("players", [])
                    
                    for player_idx, player in enumerate(players):
                        try:
                            player_location = player.get("location")
                            player_id = extract_from_url(player_location, "id") if player_location else None
                            
                            if not player_id:
                                self.logger.debug(f"skipping player {player_idx} in team {team_id}: missing id")
                                continue
                            
                            first_name = player.get("firstName", "")
                            last_name = player.get("lastName", "")
                            full_name = f"{first_name} {last_name}".strip()
                            
                            player_data = {
                                "id": player_id,
                                "nickname": player.get("nickName"),
                                "name": full_name if full_name else None,
                                "nationality": extract_country_name_from_flag_url(player.get("flagUrl")),
                                "profile_url": f"https://www.hltv.org{player_location}" if player_location else None
                            }
                            lineup.append(player_data)
                            
                        except Exception as e:
                            self.logger.error(f"error parsing player {player_idx} in team {team_id}: {e}")
                            continue
                    
                    team_data = {
                        "id": str(team_id),
                        "name": name,
                        "country": country,
                        "url": url,
                        "team_logo_url": team_logo_url,
                        "lineup": lineup
                    }
                    
                    results.append(team_data)
                    
                except Exception as e:
                    self.logger.error(f"error parsing team {team_idx}: {e}")
                    continue
                    
            self.logger.info(f"successfully parsed {len(results)} teams with {sum(len(t['lineup']) for t in results)} players")
            
        except Exception as e:
            self.logger.error(f"error parsing search results: {e}")
            
        return results

    # ==================== PUBLIC METHODS ====================

    def search_teams(self) -> dict:
        """
        search teams and return formatted results.
        
        returns:
            dict with query, results list, total count and success flag
        """
        try:
            results = self.__parse_search_results()
            
            self.response["query"] = self.query
            self.response["results"] = results
            self.response["total"] = len(results)
            self.response["success"] = True
            
            self.logger.info(f"search complete: {len(results)} teams found for '{self.query}'")
            
        except Exception as e:
            self.logger.error(f"error in search_teams: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"error searching teams: {str(e)}"
            )
        
        return self.response