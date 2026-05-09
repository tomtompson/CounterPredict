class Matches:
    class LiveMatches:
        LIVE_MATCH_CONTAINER = (
            "//div[contains(@class, 'match-wrapper') and @live='true']"
        )

        TEAM = ".//div[contains(@class, 'match-teamname')]/text()"
        TEAM_ID_FROM_CONTAINER = "./@team1 | ./@team2"
        TEAM_CURRENT_MAP_SCORE = ".//span[contains(@class, 'current-map-score')]/text()"
        TEAM_MAP_SCORE = ".//span[@class='map-score']/span/text()"
        TOURNAMENT_NAME = ".//div[@class='match-event text-ellipsis']/div[@class='text-ellipsis']/text()"
        TOURNAMENT_ID = "./@data-event-id"
        MATCH_TYPE = ".//div[contains(@class, 'match-meta') and not(contains(text(), 'Live'))]/text()"
        MATCH_URL = ".//a[contains(@class, 'match-info')]/@href"

    class TodayMatches:
        DAY_SECTION = (
            "//div[contains(@class, 'matches-list-section') and @match-container]"
        )
        DAY_HEADLINE = ".//div[contains(@class, 'matches-list-headline')]/text()"
        DAY_HEADLINE_ALT = ".//div[contains(@class, 'section-headline')]/text()"
        MATCH_WRAPPER = (
            ".//div[contains(@class, 'match-wrapper') and not(@live='true')]"
        )

        MATCH_ID = "./@data-match-id"
        TEAM_NAME = ".//div[contains(@class, 'match-teamname')]/text()"
        TEAM_LOGO = ".//div[contains(@class, 'match-team-logo-container')]/img/@src"
        TOURNAMENT_NAME = ".//div[@class='match-event']/text()"
        TOURNAMENT_ID = ".//div[@class='match-event']/@data-event-id"
        TOURNAMENT_LOGO = (
            ".//div[contains(@class, 'match-event-logo-container')]/img/@src"
        )
        MATCH_TIME = ".//div[contains(@class, 'match-time')]/text()"
        MATCH_TIMESTAMP_ATTR = ".//div[contains(@class, 'match-time')]/@data-unix"
        MATCH_TIMESTAMP = ".//div[contains(@class, 'match-time')]/@data-unix"
        MATCH_TYPE = ".//div[contains(@class, 'match-meta') and not(contains(text(), 'Live'))]/text()"
        MATCH_URL = ".//a[contains(@class, 'match-info')]/@href"
        # wraper team xpath
        TEAM1_ID = "./@team1"
        TEAM2_ID = "./@team2"

    class MatchStats:
        URL = "//link[@rel='canonical']/@href"

        HAS_STATS = "//div[@class='matchstats']"
        WITH_SCORE = "//div[contains(@class,'withScore')]"

        TEAM1_NAME = (
            "(//div[@class='standard-box teamsBox']//div[@class='teamName'])[1]/text()"
        )
        TEAM1_ID = "//a[contains(@class,'dropdownTeam team1')]/@href"
        TEAM1_SCORE = "//div[@class='score']/span[1]/text()"

        TEAM2_NAME = (
            "(//div[@class='standard-box teamsBox']//div[@class='teamName'])[2]/text()"
        )
        TEAM2_ID = "//a[contains(@class,'dropdownTeam team2')]/@href"
        TEAM2_SCORE = "//div[@class='score']/span[2]/text()"

        MATCH_DATE = "//div[@class='standard-box teamsBox']//div[@class='timeAndEvent']//div[@class='date']/text()"
        MATCH_TIME = "//div[@class='standard-box teamsBox']//div[@class='timeAndEvent']//div[@class='time']/text()"
        UNIX_TIMESTAMP = "//div[@class='standard-box teamsBox']//div[@class='timeAndEvent']//div[@class='date']/@data-unix"

        EVENT_NAME = "//div[@class='standard-box teamsBox']//div[@class='timeAndEvent']//a/text()"
        EVENT_ID = (
            "//div[@class='standard-box teamsBox']//div[@class='timeAndEvent']//a/@href"
        )

        _MAP_NAME_BASE = (
            "(//div[@class='mapholder']//div[@class='mapname'])[{n}]/text()"
        )
        _MAP_SCORE_BASE = "((//div[@class='mapholder'])[{m}]//div[@class='results-team-score'])[{t}]/text()"
        _MAP_HALF_BASE = "(//div[@class='mapholder'])[{m}]//div[@class='results-center-half-score']/span[@class='{side}'][{t}]/text()"

        MAP_POOL = "//div[@class='mapholder']//div[@class='mapname']/text()"

        MAP1_NAME = _MAP_NAME_BASE.format(n=1)
        MAP2_NAME = _MAP_NAME_BASE.format(n=2)
        MAP3_NAME = _MAP_NAME_BASE.format(n=3)
        MAP4_NAME = _MAP_NAME_BASE.format(n=4)
        MAP5_NAME = _MAP_NAME_BASE.format(n=5)

        MAP1_TEAM1_SCORE = _MAP_SCORE_BASE.format(m=1, t=1)
        MAP1_TEAM1_CT = _MAP_HALF_BASE.format(m=1, side="ct", t=1)
        MAP1_TEAM1_TR = _MAP_HALF_BASE.format(m=1, side="t", t=1)

        MAP1_TEAM2_SCORE = _MAP_SCORE_BASE.format(m=1, t=2)
        MAP1_TEAM2_CT = _MAP_HALF_BASE.format(m=1, side="ct", t=2)
        MAP1_TEAM2_TR = _MAP_HALF_BASE.format(m=1, side="t", t=2)

        MAP2_TEAM1_SCORE = _MAP_SCORE_BASE.format(m=2, t=1)
        MAP2_TEAM1_CT = _MAP_HALF_BASE.format(m=2, side="ct", t=1)
        MAP2_TEAM1_TR = _MAP_HALF_BASE.format(m=2, side="t", t=1)

        MAP2_TEAM2_SCORE = _MAP_SCORE_BASE.format(m=2, t=2)
        MAP2_TEAM2_CT = _MAP_HALF_BASE.format(m=2, side="ct", t=2)
        MAP2_TEAM2_TR = _MAP_HALF_BASE.format(m=2, side="t", t=2)

        MAP3_TEAM1_SCORE = _MAP_SCORE_BASE.format(m=3, t=1)
        MAP3_TEAM1_CT = _MAP_HALF_BASE.format(m=3, side="ct", t=1)
        MAP3_TEAM1_TR = _MAP_HALF_BASE.format(m=3, side="t", t=1)

        MAP3_TEAM2_SCORE = _MAP_SCORE_BASE.format(m=3, t=2)
        MAP3_TEAM2_CT = _MAP_HALF_BASE.format(m=3, side="ct", t=2)
        MAP3_TEAM2_TR = _MAP_HALF_BASE.format(m=3, side="t", t=2)

        MAP4_TEAM1_SCORE = _MAP_SCORE_BASE.format(m=4, t=1)
        MAP4_TEAM1_CT = _MAP_HALF_BASE.format(m=4, side="ct", t=1)
        MAP4_TEAM1_TR = _MAP_HALF_BASE.format(m=4, side="t", t=1)

        MAP4_TEAM2_SCORE = _MAP_SCORE_BASE.format(m=4, t=2)
        MAP4_TEAM2_CT = _MAP_HALF_BASE.format(m=4, side="ct", t=2)
        MAP4_TEAM2_TR = _MAP_HALF_BASE.format(m=4, side="t", t=2)

        MAP5_TEAM1_SCORE = _MAP_SCORE_BASE.format(m=5, t=1)
        MAP5_TEAM1_CT = _MAP_HALF_BASE.format(m=5, side="ct", t=1)
        MAP5_TEAM1_TR = _MAP_HALF_BASE.format(m=5, side="t", t=1)

        MAP5_TEAM2_SCORE = _MAP_SCORE_BASE.format(m=5, t=2)
        MAP5_TEAM2_CT = _MAP_HALF_BASE.format(m=5, side="ct", t=2)
        MAP5_TEAM2_TR = _MAP_HALF_BASE.format(m=5, side="t", t=2)

        # Per-map stats containers (excludes the aggregate 'all-content' container)
        MAP_CONTAINERS = "//div[@class='stats-content' and @id!='all-content']"
        MAP_CONTAINER_ID = "@id"

        _TABLE_BASE = "(.//table[@class='table {cls}'])[{t}]"
        _PLAYER_ROWS_BASE = _TABLE_BASE + "//tr[not(@class='header-row')]"

        # Each map container has 6 tables: team1 total/ct/t, team2 total/ct/t
        TEAM1_TOTAL_TABLE = _TABLE_BASE.format(cls="totalstats", t=1)
        TEAM1_CT_TABLE = _TABLE_BASE.format(cls="ctstats hidden", t=1)
        TEAM1_T_TABLE = _TABLE_BASE.format(cls="tstats hidden", t=1)

        TEAM2_TOTAL_TABLE = _TABLE_BASE.format(cls="totalstats", t=2)
        TEAM2_CT_TABLE = _TABLE_BASE.format(cls="ctstats hidden", t=2)
        TEAM2_T_TABLE = _TABLE_BASE.format(cls="tstats hidden", t=2)

        # Player rows — tables have no thead/tbody, header row has class="header-row"
        PLAYER_ROWS = ".//tr[not(@class='header-row')]"

        # Player nick (clean nickname from span)
        PLAYER_NICK = ".//td[@class='players']//span[@class='player-nick']/text()"
        PLAYER_ID = ".//td[@class='players']//a/@href"

        # Per-side stat columns (swing class varies: won/lost suffix)
        PLAYER_KD = ".//td[@class='kd text-center traditional-data']/text()"
        PLAYER_SWING = ".//td[contains(@class,'roundSwing text-center')]/text()"
        PLAYER_ADR = ".//td[@class='adr text-center traditional-data']/text()"
        PLAYER_KAST = ".//td[@class='kast text-center traditional-data']/text()"
        PLAYER_RATING = ".//td[contains(@class,'rating text-center')]/text()"

        # CT side — Team 1
        TEAM1_CT_PLAYER_NICK = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=1)
            + "//span[@class='player-nick']/text()"
        )
        TEAM1_CT_PLAYER_ID = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=1)
            + "//td[@class='players']//a/@href"
        )
        TEAM1_CT_PLAYER_KD = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=1)
            + "//td[@class='kd text-center traditional-data']/text()"
        )
        TEAM1_CT_PLAYER_SWING = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=1)
            + "//td[contains(@class,'roundSwing text-center')]/text()"
        )
        TEAM1_CT_PLAYER_ADR = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=1)
            + "//td[@class='adr text-center traditional-data']/text()"
        )
        TEAM1_CT_PLAYER_KAST = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=1)
            + "//td[@class='kast text-center traditional-data']/text()"
        )
        TEAM1_CT_PLAYER_RATING = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=1)
            + "//td[contains(@class,'rating text-center')]/text()"
        )

        # T side — Team 1
        TEAM1_T_PLAYER_NICK = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=1)
            + "//span[@class='player-nick']/text()"
        )
        TEAM1_T_PLAYER_ID = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=1)
            + "//td[@class='players']//a/@href"
        )
        TEAM1_T_PLAYER_KD = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=1)
            + "//td[@class='kd text-center traditional-data']/text()"
        )
        TEAM1_T_PLAYER_SWING = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=1)
            + "//td[contains(@class,'roundSwing text-center')]/text()"
        )
        TEAM1_T_PLAYER_ADR = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=1)
            + "//td[@class='adr text-center traditional-data']/text()"
        )
        TEAM1_T_PLAYER_KAST = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=1)
            + "//td[@class='kast text-center traditional-data']/text()"
        )
        TEAM1_T_PLAYER_RATING = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=1)
            + "//td[contains(@class,'rating text-center')]/text()"
        )

        # CT side — Team 2
        TEAM2_CT_PLAYER_NICK = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=2)
            + "//span[@class='player-nick']/text()"
        )
        TEAM2_CT_PLAYER_ID = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=2)
            + "//td[@class='players']//a/@href"
        )
        TEAM2_CT_PLAYER_KD = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=2)
            + "//td[@class='kd text-center traditional-data']/text()"
        )
        TEAM2_CT_PLAYER_SWING = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=2)
            + "//td[contains(@class,'roundSwing text-center')]/text()"
        )
        TEAM2_CT_PLAYER_ADR = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=2)
            + "//td[@class='adr text-center traditional-data']/text()"
        )
        TEAM2_CT_PLAYER_KAST = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=2)
            + "//td[@class='kast text-center traditional-data']/text()"
        )
        TEAM2_CT_PLAYER_RATING = (
            _PLAYER_ROWS_BASE.format(cls="ctstats hidden", t=2)
            + "//td[contains(@class,'rating text-center')]/text()"
        )

        # T side — Team 2
        TEAM2_T_PLAYER_NICK = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=2)
            + "//span[@class='player-nick']/text()"
        )
        TEAM2_T_PLAYER_ID = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=2)
            + "//td[@class='players']//a/@href"
        )
        TEAM2_T_PLAYER_KD = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=2)
            + "//td[@class='kd text-center traditional-data']/text()"
        )
        TEAM2_T_PLAYER_SWING = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=2)
            + "//td[contains(@class,'roundSwing text-center')]/text()"
        )
        TEAM2_T_PLAYER_ADR = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=2)
            + "//td[@class='adr text-center traditional-data']/text()"
        )
        TEAM2_T_PLAYER_KAST = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=2)
            + "//td[@class='kast text-center traditional-data']/text()"
        )
        TEAM2_T_PLAYER_RATING = (
            _PLAYER_ROWS_BASE.format(cls="tstats hidden", t=2)
            + "//td[contains(@class,'rating text-center')]/text()"
        )
