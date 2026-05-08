from dataclasses import dataclass

from app.services.base import HLTVBase
from app.utils.utils import extract_country_name_from_flag_url


@dataclass
class HLTVPlayerSearch(HLTVBase):
    """A class for searching players on HLTV and retrieving search results.

    Args:
        query (str): The search query for finding players on HLTV.

    """

    query: str

    def __post_init__(self) -> None:
        """Set up player search URL and fetch initial data."""
        super().__post_init__()
        self.URL = f"https://www.hltv.org/search?term={self.query}"
        self.response["query"] = self.query
        self.page_data = self.__fetch_json()

    def __fetch_json(self) -> dict:
        """
        Make GET request and return JSON response.

        Returns:
            dict: raw JSON data from HLTV search endpoint.
        """
        res = self.make_request(self.URL)
        return res.json()

    def __parse_search_results(self) -> list:
        """
        Parse the list of players from HLTV search results.

        Returns:
            list: player dicts with id, name, nickname, nationality, flag_url, url.
        """
        results = []

        players = self.page_data[0].get("players", [])

        for player in players:
            id = player.get("id")
            name = f"{player.get('firstName', '')} {player.get('lastName', '')}".strip()
            nickname = player.get("nickName")
            flag_url = player.get("flagUrl")
            nationality = extract_country_name_from_flag_url(flag_url)
            url = f"https://www.hltv.org{player.get('location', '')}"

            results.append(
                {
                    "id": str(id),
                    "name": name,
                    "nickname": nickname,
                    "nationality": nationality,
                    "flag_url": flag_url,
                    "url": url,
                },
            )

        return results

    def search_players(self) -> dict:
        """
        Retrieve and parse player search results.

        Returns:
            dict: search query and results list.
        """
        self.response["query"] = self.query
        self.response["results"] = self.__parse_search_results()

        return self.response
