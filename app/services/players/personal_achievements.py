# app/services/player_personal_achievements.py

from dataclasses import dataclass

from fastapi import HTTPException

from app.services.base import HLTVBase
from app.utils.utils import trim
from app.utils.xpath import Players


@dataclass
class HLTVPlayerPersonalAchievements(HLTVBase):
    """class for getting personal achievements from a player profile.

    Attributes:
        player_id: hltv player id

    """

    player_id: str

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """Setup personal achievements with player id."""
        super().__post_init__()

        self.URL = f"https://www.hltv.org/player/{self.player_id}/who#tab-trophiesBox"
        self.response["id"] = self.player_id

        self.logger.info(f"loading personal achievements for player {self.player_id}")

        self.page = self.request_url_page()

        self.raise_exception_if_not_found(xpath=Players.Profile.URL)

        self.logger.info(f"page loaded for player {self.player_id}")

    # ==================== PARSING METHODS ====================

    def __parse_player_personal_achievements(self) -> dict:
        """Parse personal achievements from player profile.

        Returns:
            dict with all personal achievements data

        """
        self.logger.info("parsing personal achievements")

        placements = self.get_all_by_xpath(
            Players.PersonalAchievements.TOP_20_PLACEMENT,
        )
        years = self.get_all_by_xpath(Players.PersonalAchievements.TOP_20_YEAR)
        article_urls = self.get_all_by_xpath(
            Players.PersonalAchievements.TOP_20_ARTICLE_URL,
        )

        self.logger.debug(
            f"top20 - placements: {len(placements)}, years: {len(years)}, articles: {len(article_urls)}",
        )

        top_20_list = []
        for i, (placement, year) in enumerate(zip(placements, years, strict=False)):
            clean_placement = trim(placement)
            clean_year = "20" + year.strip("()'")
            article = (
                f"https://www.hltv.org{article_urls[i]}"
                if i < len(article_urls)
                else None
            )
            top_20_list.append(
                {
                    "placement": clean_placement,
                    "year": clean_year,
                    "article": article,
                },
            )

        major_winner_count = self.get_text_by_xpath(
            Players.PersonalAchievements.MAJOR_WINNER_COUNT,
        )
        major_mvp_count = self.get_text_by_xpath(
            Players.PersonalAchievements.MAJOR_MVP_COUNT,
        )
        mvp_winner_count = self.get_text_by_xpath(
            Players.PersonalAchievements.MVP_WINNER_COUNT,
        )

        self.logger.debug(
            f"major winner: {major_winner_count}, major mvp: {major_mvp_count}, mvp count: {mvp_winner_count}",
        )

        raw_mvp_winner = self.get_text_by_xpath(Players.PersonalAchievements.MVP_WINNER)
        mvp_winner = (
            [
                e.strip()
                for e in raw_mvp_winner.split("\n")
                if e.strip() and "MVP winner at:" not in e
            ]
            if raw_mvp_winner
            else []
        )
        self.logger.debug(f"mvp winner list: {len(mvp_winner)} items")

        evp_at = self.get_all_by_xpath(Players.PersonalAchievements.EVP)
        self.logger.debug(f"evp list: {len(evp_at)} items")

        achievements = {
            "major_winner_count": major_winner_count or None,
            "major_mvp_count": major_mvp_count or None,
            "mvp_winner_count": mvp_winner_count or None,
            "evp_count": len(evp_at) if evp_at else None,
            "top_20_count": len(top_20_list) if top_20_list else None,
            "mvp_winner": mvp_winner or None,
            "evp_at": evp_at or None,
            "top_20": top_20_list or None,
        }

        self.logger.info(
            f"parsed {len(top_20_list)} top20 entries, {len(evp_at)} evp entries",
        )

        return achievements

    # ==================== PUBLIC METHODS ====================

    def get_player_personal_achievements(self) -> dict:
        """Get personal achievements for player.

        Returns:
            dict with player id and personal achievements

        """
        try:
            achievements = self.__parse_player_personal_achievements()

            self.response["id"] = self.player_id
            self.response["personal_achievements"] = achievements

            self.logger.info(
                f"returning personal achievements for player {self.player_id}",
            )

        except Exception as e:
            self.logger.exception("error in get_player_personal_achievements")
            raise HTTPException(
                status_code=500,
                detail=f"error processing personal achievements: {e!s}",
            )

        return self.response
