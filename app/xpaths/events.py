class Events:
    class EventProfile:
        EVENT_URL = "//div[@class ='event-hub']//a/@href"
        EVENT_NAME = "//h1[contains(@class, 'event-hub-title')]/text()"
        TEAM_COUNT = "//td[contains(@class,'teamsNumber')]/text()"
        EVENT_START_DATE = (
            "//th[contains(text(), 'Start date')]/parent::tr/td/span/text()"
        )
        EVENT_END_DATE = (
            "//th[contains(text(), 'End date')]/parent::tr/td/span/span/text()"
        )
        PRIZE_POOL = "//td[contains(@class, 'prizepool')]/text()"
        PRIZE_CLUB_SHARE = "//th[contains(text(), 'Club share')]/following-sibling::td"
        PRIZE_PLAYER_SHARE = (
            "//th[contains(text(), 'Player share')]/following-sibling::td"
        )
        EVENT_LOCATION = "//td[contains(@class,'location')]//span/text()"
        LOCATION_FLAG_URL = "//td[contains(@class,'location')]//img/@src"
        MAP_POOL = "//div[@class = 'map-pool-map-name']"

        # MVP
        EVENT_MVP_NICKNAME = (
            "//div[@class= 'player-name']//a//span[@class = 'bold']/text()"
        )
        EVENT_MVP_URL = "//div[@class= 'player-name']//a/@href"

        # EVPS
        EVENT_EVPS_NICKNAME = (
            "//a[contains(@class, 'evp-wrapper')]//div[@class= 'evp-name-top']/text()"
        )
        EVENT_EVPS_URL = "//a[contains(@class, 'evp-wrapper')]/@href"

        # teams
        TEAM_NAME = "//div[@class='team-name']//div[@class='text-container']//div[@class='text']/text()"
        TEAM_URL = "//div[@class='team-name']//a/@href"
        TEAM_PLACEMENT = "//div[contains(@class,'placement')]/div[not(@class)]/text()"

    class EventTeamStats:
        # Base pattern
        _TEAM_BOX_BASE = "//div[contains(@class, 'team-box') and .//a[contains(@href, '/team/{team_id}/')]]"

        #'teams attended' box
        TEAM_LINEUP = (
            _TEAM_BOX_BASE
            + "//div[contains(@class, 'lineup-box')]//div[contains(@class , 'flag-align player')]//text()"
        )
        TEAM_PLAYER_URL = (
            _TEAM_BOX_BASE
            + "//div[contains(@class, 'lineup-box')]//div[contains(@class , 'flag-align player')]//a/@href"
        )
        TEAM_COACH = (
            _TEAM_BOX_BASE
            + "//div[contains(@class,'coach-text')]/parent::div//div[contains(@class, 'flag-align player')]//text()"
        )
        TEAM_COACH_URL = (
            _TEAM_BOX_BASE
            + "//div[contains(@class,'coach-text')]/parent::div//div[contains(@class, 'flag-align player')]//a/@href"
        )
        QUALIFY_METHOD = (
            _TEAM_BOX_BASE + "//div[contains(@class, 'sub-text event-text')]//text()"
        )

        #'vrs ranking' box
        VRS_DATE = "//th[contains(text(), 'VRS date')]/following-sibling::td//span"
        VRS_POINTS_BEFORE_EVENT = "//tbody[contains(@class, 'vrs-before')][.//a[contains(@href, '/team/{team_id}/')]]//tr[.//a[contains(@href, '/team/{team_id}/')]]/td[@class='vrs-points']/div[@class='start-only']//div"
        VRS_POINTS_AFTER_EVENT = "//tbody[contains(@class, 'vrs-after')][.//a[contains(@href, '/team/{team_id}/')]]//tr[.//a[contains(@href, '/team/{team_id}/')]]/td[@class='vrs-points']/div[@class='start-only']//div"
        VRS_POINTS_ACQUIRED = "//tbody[contains(@class, 'vrs-after')][.//a[contains(@href, '/team/{team_id}/')]]//tr[.//a[contains(@href, '/team/{team_id}/')]]/td[@class='vrs-points']/div[@class='finished-only']//div[contains(@class, 'finished-points')]"
        VRS_PLACEMENT_BEFORE_EVENT = "//tbody[contains(@class, 'vrs-before')][.//a[contains(@href, '/team/{team_id}/')]]//tr[.//a[contains(@href, '/team/{team_id}/')]]/td[@class = 'vrs-placements']//div[@class = 'start-only']//div[@class = 'vrs-placement-btn']"
        VRS_PLACEMENT_AFTER_EVENT = "//tbody[contains(@class, 'vrs-after')][.//a[contains(@href, '/team/{team_id}/')]]//tr[.//a[contains(@href, '/team/{team_id}/')]]/td[@class = 'vrs-placements']//div[@class = 'start-only']//div[@class = 'vrs-placement-btn']"

        #'prize distribution' box
        PRIZE = "//div[@class = 'team' and .//a[contains(@href,'/team/{team_id}/')]]/following-sibling::div[@class='prize']/text()"
        PRIZE_CLUB_SHARE = "//div[@class = 'team' and .//a[contains(@href,'/team/{team_id}/')]]/following-sibling::div[@class='prize club-share']/text()"
        TEAM_PLACEMENT = "//div[@class = 'team' and .//a[contains(@href,'/team/{team_id}/')]]/following-sibling::div[not(@class)]/text()"

    class EventResults:
        _TEAM_CELL_BASE = ".//td[contains(@class, 'team-cell')]"
        _RESULT_SCORE_BASE = ".//td[contains(@class, 'result-score')]"

        RESULT_CONTAINER = "//div[contains(@class, 'results-all')]//div[contains(@class, 'result-con') and @data-zonedgrouping-entry-unix]"
        MATCH_ID = ".//a[contains(@class, 'a-reset')]/@href"
        TIMESTAMP = "@data-zonedgrouping-entry-unix"
        TEAM1_NAME = _TEAM_CELL_BASE + "[1]//div[contains(@class, 'team')]/text()"
        TEAM1_LOGO = _TEAM_CELL_BASE + "[1]//img[contains(@class, 'team-logo')]/@src"
        TEAM1_SCORE = _RESULT_SCORE_BASE + "/span[1]/text()"
        TEAM1_SCORE_CLASS = _RESULT_SCORE_BASE + "/span[1]/@class"

        TEAM2_NAME = _TEAM_CELL_BASE + "[2]//div[contains(@class, 'team')]/text()"
        TEAM2_LOGO = _TEAM_CELL_BASE + "[2]//img[contains(@class, 'team-logo')]/@src"
        TEAM2_SCORE = _RESULT_SCORE_BASE + "/span[2]/text()"
        TEAM2_SCORE_CLASS = _RESULT_SCORE_BASE + "/span[2]/@class"

        MATCH_TYPE = ".//div[contains(@class, 'map-text')]/text()"

        MATCH_URL = ".//a[contains(@class, 'a-reset')]/@href"
