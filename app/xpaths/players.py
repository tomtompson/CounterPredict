class Players:
    class Profile:
        URL = "//link[@rel='canonical']//@href"
        NICKNAME = "//h1[@class='playerNickname']/text()"
        NAME = "//div[@class='playerRealname']/text()"
        AGE = "//div[@class='playerInfoRow playerAge']//span[@itemprop='text']/text()"
        NATIONALITY = "//div[@class='playerRealname']//img/@alt"
        RATING = "//div[@class='player-stat']//span[@class='statsVal']//p/text()"
        CURRENT_TEAM = "//div[@class= 'playerInfoRow playerTeam']//a/text()"
        CURRENT_TEAM_URL = "//div[@class= 'playerInfoRow playerTeam']//a/@href"
        IMAGE_URL = "//img[@class = 'bodyshot-img']/@src"
        SOCIAL_MEDIA = "//div[@class = 'socialMediaButtons']//a/@href"

    class Search:
        FOUND = "//text()"
        BASE = "//table[@class='table'][.//td[@class='table-header'][contains(text(), 'Player')]]"
        RESULTS = BASE + "/tbody/tr[not(td[@class='table-header'])]"
        NAME = RESULTS + "/td/a/text()"
        URL = RESULTS + "/td/a/@href"
        NATIONALITY = RESULTS + "//img/@alt"

    class TeamAchievements:
        ROWS = "//table[contains(@class, 'achievement-table')]//tr[contains(@class, 'team')]"
        PLACEMENT = ".//div[contains(@class, 'achievement')]/text()"
        TEAM_NAME = (
            ".//td[contains(@class, 'team-name-cell')]//span[@class='team-name']/text()"
        )
        TEAM_URL = ".//td[contains(@class, 'team-name-cell')]//a/@href"
        TOURNAMENT_NAME = ".//td[contains(@class, 'tournament-name-cell')]/a/text()"
        TOURNAMENT_URL = ".//td[contains(@class, 'tournament-name-cell')]/a/@href"
        PLAYER_STATS_URL = ".//td[contains(@class, 'stats-button-cell')]/a/@href"

    class PersonalAchievements:
        _TOP_20_BASE = "//div[contains(@class,'playerTop20')]//span[contains(@class, 'top20ListRight')]"
        TOP_20_PLACEMENT = _TOP_20_BASE + "/a/text()"
        TOP_20_YEAR = _TOP_20_BASE + "/span/text()"
        TOP_20_ARTICLE_URL = _TOP_20_BASE + "/a/@href"
        MAJOR_WINNER_COUNT = "//div[contains(@class, 'majorWinner')]/b"
        MAJOR_MVP_COUNT = "//div[contains(@class, 'majorMVP')]/b"
        MVP_WINNER_COUNT = "//div[contains(@class, 'mvp-count')]//text()"
        MVP_WINNER = "//div[contains(@class, 'trophyHolder')]//span[contains(@title, 'MVP')]/@title"
        EVP = "//div[contains(@id, 'EVPs')]//tr[contains(@class,'trophy-row')]//div[contains(@class,'trophy-event')]/a/text()"

    class Trophies:
        _TROPHY_BASE = "//div[contains(@id, 'Trophies')]//tr[contains(@class, 'trophy-row')]//div[contains(@class, 'trophy-event')]/a"
        TOURNAMENT_NAME = _TROPHY_BASE + "/text()"
        TOURNAMENT_URL = _TROPHY_BASE + "/@href"
        TROPHY_IMG_URL = "//div[contains(@id, 'Trophies')]//tr[contains(@class, 'trophy-row')]//div[contains(@class, 'trophy-detail')]/img/@src"

    class Stats:
        # Base patterns
        _STATS_SIDE_COMBINED = "//div[contains(@class, 'stats-side-combined')]"
        _PER_ROUND_BASE = (
            _STATS_SIDE_COMBINED
            + "//div[contains(@data-per-round-title, '{title}') and contains(@class, 'stats-side-combined')]//div[contains(@class, 'role-stats-data')]//text()"
        )
        _TITLED_STAT_BASE = (
            _STATS_SIDE_COMBINED
            + "//div[contains(@class, 'role-stats-top')][.//div[contains(@class, 'role-stats-title') and contains(text(), '{title}')]]//div[contains(@class, 'role-stats-data')]/text()"
        )

        # firepower stats
        KILLS_PER_ROUND = _PER_ROUND_BASE.format(title="Kills per round")
        KILLS_PER_ROUND_WIN = _PER_ROUND_BASE.format(title="Kills per round win")
        DAMAGE_PER_ROUND = "//div[contains(@data-per-round-title, 'Damage per round') and not(contains(@data-per-round-title, 'Damage per round win')) and contains(@class, 'stats-side-combined')]//div[contains(@class, 'role-stats-data')]//text()"
        DAMAGE_PER_ROUND_WIN = _PER_ROUND_BASE.format(title="Damage per round win")
        ROUNDS_WITH_A_KILL_PERCENTAGE = _PER_ROUND_BASE.format(
            title="Rounds with a kill"
        )
        RATING_1_0 = _TITLED_STAT_BASE.format(title="Rating 1.0")
        ROUNDS_WITH_MULTI_KILL_PERCENTAGE = _PER_ROUND_BASE.format(
            title="Rounds with a multi-kill"
        )
        PISTOL_ROUND_RATING = _TITLED_STAT_BASE.format(title="Pistol round rating")

        # entrying stats
        SAVED_BY_TEAMMATE_PER_ROUND = _TITLED_STAT_BASE.format(
            title="Saved by teammate per round"
        )
        TRADED_DEATHS_PER_ROUND = _TITLED_STAT_BASE.format(
            title="Traded deaths per round"
        )
        TRADED_DEATHS_PERCENTAGE = _TITLED_STAT_BASE.format(
            title="Traded deaths percentage"
        )
        OPENING_DEATHS_TRADED_PERCENTAGE = _TITLED_STAT_BASE.format(
            title="Opening deaths traded percentage"
        )
        ASSISTS_PER_ROUND = _PER_ROUND_BASE.format(title="Assists per round")
        SUPPORT_ROUNDS_PERCENTAGE = _TITLED_STAT_BASE.format(title="Support rounds")

        # trading stats
        SAVED_TEAMMATE_PER_ROUND = _PER_ROUND_BASE.format(
            title="Saved teammate per round"
        )
        TRADE_KILLS_PER_ROUND = _PER_ROUND_BASE.format(title="Trade kills per round")
        TRADE_KILLS_PERCENTAGE = _TITLED_STAT_BASE.format(
            title="Trade kills percentage"
        )
        ASSISTED_KILLS_PERCENTAGE = _TITLED_STAT_BASE.format(
            title="Assisted kills percentage"
        )
        DAMAGE_PER_KILL = _TITLED_STAT_BASE.format(title="Damage per kill")

        # opening stats
        OPENING_KILLS_PER_ROUND = _PER_ROUND_BASE.format(
            title="Opening kills per round"
        )
        OPENING_DEATHS_PER_ROUND = _PER_ROUND_BASE.format(
            title="Opening deaths per round"
        )
        OPENING_ATTEMPTS_PERCENTAGE = _PER_ROUND_BASE.format(title="Opening attempts")
        OPENING_SUCCESS_PERCENTAGE = _TITLED_STAT_BASE.format(title="Opening success")
        WIN_AFTER_OPENING_KILL_PERCENTAGE = _TITLED_STAT_BASE.format(
            title="Win% after opening kill"
        )
        ATTACKS_PER_ROUND = _PER_ROUND_BASE.format(title="Attacks per round")

        # clutching stats
        CLUTCH_POINTS_PER_ROUND = _PER_ROUND_BASE.format(
            title="Clutch points per round"
        )
        LAST_ALIVE_PERCENTAGE = _TITLED_STAT_BASE.format(title="Last alive percentage")
        _1v1_WIN_PERCENTAGE = _TITLED_STAT_BASE.format(title="1on1 win percentage")
        TIME_ALIVE_PER_ROUND = _PER_ROUND_BASE.format(title="Time alive per round")
        SAVES_PER_ROUND_LOSS_PERCENTAGE = _TITLED_STAT_BASE.format(
            title="Saves per round loss"
        )

        # sniping stats
        SNIPER_KILLS_PER_ROUND = _PER_ROUND_BASE.format(title="Sniper kills per round")
        SNIPER_KILLS_PERCENTAGE = _TITLED_STAT_BASE.format(
            title="Sniper kills percentage"
        )
        ROUNDS_WITH_SNIPER_KILLS_PERCENTAGE = _PER_ROUND_BASE.format(
            title="Rounds with sniper kills percentage"
        )
        SNIPER_MULTI_KILL_ROUNDS = _PER_ROUND_BASE.format(
            title="Sniper multi-kill rounds"
        )
        SNIPER_OPENING_KILLS_PER_ROUND = _PER_ROUND_BASE.format(
            title="Sniper opening kills per round"
        )

        # utility stats
        UTILITY_DAMAGE_PER_ROUND = _PER_ROUND_BASE.format(
            title="Utility damage per round"
        )
        UTILITY_KILLS_PER_100_ROUNDS = _PER_ROUND_BASE.format(
            title="Utility kills per 100 rounds"
        )
        FLASHES_THROWN_PER_ROUND = _PER_ROUND_BASE.format(
            title="Flashes thrown per round"
        )
        FLASH_ASSISTS_PER_ROUND = _PER_ROUND_BASE.format(
            title="Flash assists per round"
        )
        TIME_OPPONENT_FLASHED_PER_ROUND = _PER_ROUND_BASE.format(
            title="Time opponent flashed per round"
        )

    class CareerStats:
        _STAT_BASE = "//div[contains(@class, 'stats-row')]/span[contains(text(),'{label}')]/following-sibling::span[1]/text()"

        TOTAL_KILLS = _STAT_BASE.format(label="Total kills")
        HEADSHOT_PERCENTAGE = _STAT_BASE.format(label="Headshot %")
        TOTAL_DEATHS = _STAT_BASE.format(label="Total deaths")
        KD_RATIO = _STAT_BASE.format(label="K/D Ratio")
        DAMAGE_PER_ROUND = _STAT_BASE.format(label="Damage / Round")
        GRENADE_DMG_PER_ROUND = _STAT_BASE.format(label="Grenade dmg / Round")
        MAPS_PLAYED = _STAT_BASE.format(label="Maps played")
        ROUNDS_PLAYED = _STAT_BASE.format(label="Rounds played")
        KILLS_PER_ROUND = _STAT_BASE.format(label="Kills / round")
        ASSISTS_PER_ROUND = _STAT_BASE.format(label="Assists / round")
        DEATHS_PER_ROUND = _STAT_BASE.format(label="Deaths / round")
        SAVED_BY_TEAMMATE_PER_ROUND = _STAT_BASE.format(label="Saved by teammate / round")
        SAVED_TEAMMATES_PER_ROUND = _STAT_BASE.format(label="Saved teammates / round")
        RATING1_0 = _STAT_BASE.format(label="Rating 1.0")
