class Ranking:
    class Stats:
        TEAM_ROW = "//div[contains(@class, 'ranked-team')]"
        RANKING_DATE = "//div[@class = 'regional-ranking-header-text']"
        TEAM_NAME = ".//div[contains(@class , 'teamLine sectionTeamPlayers')]//span[@class = 'name']/text()"
        TEAM_URL = ".//div[@class = 'more']//a[@class = 'moreLink']/@href"
        TEAM_LOGO_URL = ".//div[@class='bg-holder']//span[@class='team-logo']/img[not(contains(@class, 'day-only')) and (contains(@class, 'night-only') or not(@class))][1]/@src"
        PLAYER_ROW = ".//table[@class='lineup']//td[@class='player-holder']"
        PLAYER_NICKNAME = ".//div[@class='nick']/text()"
        PLAYER_PICTURE_URL = ".//img[@class='playerPicture']/@src"
        PLAYER_URL = ".//a[@class='pointer']/@href"
        PLAYER_NATIONALITY = ".//div[@class='nick']/img/@alt"
        HLTV_POINTS = ".//div[@class = 'bg-holder']//div[contains(@class , 'teamLine sectionTeamPlayers')]//span[@class = 'points']/text()[1]"
        PLACEMENT = ".//div[@class = 'bg-holder']//div[@class = 'ranking-header']//span[@class = 'position wide-position']/text()"
