# app/services/player_search.py

from dataclasses import dataclass
import json
import brotli
from typing import Optional, List, Dict

from app.services.base import HLTVBase
from app.utils.utils import extract_country_name_from_flag_url
from fastapi import HTTPException


@dataclass
class HLTVPlayerSearch(HLTVBase):
    """
    class for searching players on hltv and getting search results.
    attributes:
        query: query for hltv player search
    """
    
    query: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """setup search with player query"""
        super().__post_init__()
        
        self.URL = f"https://www.hltv.org/search?term={self.query}"
        self.response["query"] = self.query
        
        # headers for ajax json requests
        self._session.headers.update({
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
        })
        
        self.logger.info(f"searching for players with query: {self.query}")
        self.page_data = self.__fetch_json()

    # ==================== PRIVATE METHODS ====================

    def __fetch_json(self) -> dict:
        """
        make a single get request and return json data.
        handles brotli and raises on failure.
        
        returns:
            parsed json dict
            
        raises:
            HTTPException: if blocked, invalid json, or request error
        """
        try:
            res = self.make_request(self.URL)
            
            self.logger.info(f"request completed - status: {res.status_code}")
            self.logger.debug(f"content-type: {res.headers.get('content-type')}")
            self.logger.debug(f"content-encoding: {res.headers.get('content-encoding')}")
            
            decoded = self.__decode_response(res)
            
            if self.__is_blocked(decoded):
                self.logger.error("cloudflare block detected")
                raise HTTPException(
                    status_code=403,
                    detail="access blocked by cloudflare"
                )
            
            try:
                data = json.loads(decoded)
                self.logger.info("successfully parsed json data")
                return data
            except json.JSONDecodeError as e:
                self.logger.error(f"json decode error: {e}")
                self.logger.debug(f"response preview: {decoded[:500]}")
                raise HTTPException(
                    status_code=500,
                    detail="response is not valid json. probably blocked by cloudflare."
                )
                
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"request failed: {e}")
            raise HTTPException(status_code=500, detail=f"failed to fetch search results: {str(e)}")

    def __decode_response(self, response) -> str:
        """
        decode response with brotli support.
        
        args:
            response: http response object
            
        returns:
            decoded string
        """
        content_encoding = response.headers.get('Content-Encoding', '')
        content = response.content
        
        if 'br' in content_encoding:
            try:
                content = brotli.decompress(content)
                self.logger.debug("brotli decompression ok")
                return content.decode('utf-8')
            except Exception as e:
                self.logger.warning(f"brotli failed: {e}")
        
        try:
            return response.text
        except:
            return response.content.decode('utf-8', errors='ignore')

    def __is_blocked(self, html_content: str) -> bool:
        """
        check if response is a cloudflare block page.
        
        args:
            html_content: page content
            
        returns:
            true if blocked, false otherwise
        """
        block_indicators = [
            'cf-browser-verification',
            'cloudflare',
            'checking your browser',
            'please stand by',
            'ddos protection',
            'ray-id',
            '__cf_chl_',
            'just a moment',
            'attention required'
        ]
        
        html_lower = html_content.lower()
        for indicator in block_indicators:
            if indicator in html_lower:
                return True
        return False

    # ==================== PARSING METHODS ====================

    def __parse_search_results(self) -> List[Dict]:
        """
        parse player list from search results.
        
        returns:
            list of player dictionaries
        """
        results = []
        
        try:
            if not isinstance(self.page_data, list):
                self.logger.warning(f"unexpected data type: {type(self.page_data)}")
                return []
            
            if len(self.page_data) == 0:
                self.logger.info("empty response from api")
                return []
            
            first_item = self.page_data[0]
            players = first_item.get("players", [])
            
            self.logger.info(f"found {len(players)} players for '{self.query}'")
            
            for player in players:
                try:
                    player_id = player.get("id")
                    if not player_id:
                        continue
                    
                    first_name = player.get("firstName", "")
                    last_name = player.get("lastName", "")
                    full_name = f"{first_name} {last_name}".strip()
                    nickname = player.get("nickName", "")
                    flag_url = player.get("flagUrl", "")
                    
                    if not full_name and nickname:
                        full_name = nickname
                    
                    nationality = extract_country_name_from_flag_url(flag_url)
                    
                    profile_url = None
                    if player.get('location'):
                        profile_url = f"https://www.hltv.org{player.get('location')}"
                    
                    results.append({
                        "id": str(player_id),
                        "name": full_name,
                        "nickname": nickname,
                        "nationality": nationality,
                        "flag_url": flag_url,
                        "url": profile_url
                    })
                    
                except Exception as e:
                    self.logger.error(f"error parsing player: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"error parsing results: {e}")
            
        return results

    # ==================== PUBLIC METHODS ====================

    def search_players(self) -> dict:
        """
        run search and return formatted results.
        
        returns:
            dict with query, results and stats
        """
        self.response["results"] = self.__parse_search_results()
        self.response["total"] = len(self.response["results"])
        self.response["success"] = True
        
        self.logger.info(f"search complete: {self.response['total']} players found")
        
        return self.response