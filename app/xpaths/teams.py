class Teams:
    class TeamProfile:
        NAME = "//h1[contains(@class, 'profile-team-name')]"
        LOGO_URL = "//div[contains(@class, 'profile-team-logo-container')]//img/@srcset"
        PLAYER_NICKNAME = "//div[contains(@class, 'playerFlagName')]//span[contains(@class,'text-ellipsis bold')]/text()"
        PLAYER_URL = "//div[contains(@class,'teamProfile')]//a[contains(@class, 'col-custom')]/@href"
        COACH_NICKNAME = "//div[@class = 'profile-team-stat'][.//b[contains(text(), 'Coach')]]//span[@class = 'bold a-default']"
        COACH_URL = "//div[@class = 'profile-team-stat'][.//b[contains(text(), 'Coach')]]//a/@href"
        SOCIAL_MEDIA = "//div[@class = 'socialMediaButtons']//a/@href"
        VALVE_RANKING = "//div[@class = 'regional-wrapper']//b[contains(text(), 'Valve ranking')]/following::a[1]/text()"
        WORLD_RANKING = "//div[@class = 'profile-team-stat']//b[contains(text(), 'World ranking')]/following::a[1]/text()"
        WEEKS_IN_TOP30_FOR_CORE = "//div[@class = 'profile-team-stat'][.//b[contains(text(), 'Weeks in top30 for core')]]//span[@class = 'right']"
        AVERAGE_PLAYER_AGE = "//div[@class = 'profile-team-stat'][.//b[contains(text(), 'Average player age')]]//span[@class = 'right']"

    class Achievements:
        PLACEMENT = "//tr[@class='team']//div[contains(@class, 'achievement')][.//i[contains(@class, 'fa-trophy')]]/text()"
        TOURNAMENT_NAME = ".//td[contains(@class, 'tournament-name-cell')]/a/text()"
        TOURNAMENT_URL = ".//td[contains(@class, 'tournament-name-cell')]/a/@href"

    class UpcomingMatches:
        UPCOMING_MATCHES_ROW = "//h2[@class = 'standard-headline' and contains(text(), 'Upcoming matches')]/following::table[@class = 'table-container match-table'][1]"
        MATCH_URL = "//td[@class = 'matchpage-button-cell']//a/@href"

        EVENT_NAME = "//div[contains(@class, 'timeAndEvent')]//div[contains(@class, 'event')]//a/text()"
        EVENT_URL = "//div[contains(@class, 'timeAndEvent')]//div[contains(@class, 'event')]//a/@href"
        MATCH_DATE = "//div[contains(@class, 'timeAndEvent')]//div[contains(@class, 'date')]/text()"
        MATCH_HOUR = "//div[contains(@class, 'timeAndEvent')]//div[contains(@class, 'time')]/text()"
        RIVAL_TEAM_NAME = "//div[contains(@class, 'team2-gradient')]//div[contains(@class, 'teamName')]/text()"
        RIVAL_TEAM_URL = "//div[contains(@class, 'team2-gradient')]/a/@href"
        MATCH_TYPE = "//div[@class = 'standard-box veto-box']//div[@class = 'padding preformatted-text']/text()"

    class Results:
        RESULT_CONTAINER = "//div[contains(@class, 'results-all')]//div[contains(@class, 'result-con') and @data-zonedgrouping-entry-unix]"
        TIMESTAMP = "@data-zonedgrouping-entry-unix"

        MATCH_URL = ".//a[contains(@class, 'a-reset')]/@href"
        TEAM1_NAME = ".//td[contains(@class, 'team-cell')][1]//div[contains(@class, 'team')]/text()"
        TEAM1_LOGO = ".//td[contains(@class, 'team-cell')][1]//img[contains(@class, 'team-logo')]/@src"
        TEAM1_SCORE = ".//td[contains(@class, 'result-score')]/span[1]/text()"
        TEAM1_SCORE_CLASS = ".//td[contains(@class, 'result-score')]/span[1]/@class"
        TEAM2_SCORE = ".//td[contains(@class, 'result-score')]/span[2]/text()"
        TEAM2_NAME = ".//td[contains(@class, 'team-cell')][2]//div[contains(@class, 'team')]/text()"
        TEAM2_LOGO = ".//td[contains(@class, 'team-cell')][2]//img[contains(@class, 'team-logo')]/@src"
        EVENT_NAME = ".//td[contains(@class, 'event')]//span[contains(@class, 'event-name')]/text()"
        EVENT_LOGO = (
            ".//td[contains(@class, 'event')]//img[contains(@class, 'event-logo')]/@src"
        )
        MATCH_TYPE = ".//div[contains(@class, 'map-text')]/text()"
