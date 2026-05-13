from tests.fixtures import (
    PLAYER_CAREER_STATS,
    PLAYER_PERSONAL_ACHIEVEMENTS,
    PLAYER_PROFILE,
    PLAYER_SEARCH,
    PLAYER_STATS,
    PLAYER_TEAM_ACHIEVEMENTS,
    PLAYER_TROPHIES,
)

PLAYER_ID = PLAYER_PROFILE.id


def test_search_players(client):
    response = client.get(f"/players/{PLAYER_SEARCH.query}/search")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == PLAYER_SEARCH.query
    first = data["results"][0]
    expected = PLAYER_SEARCH.results[0]
    assert first["id"] == expected.id
    assert first["nickname"] == expected.nickname
    assert first["nationality"] == expected.nationality


def test_get_player_profile(client):
    response = client.get(f"/players/{PLAYER_ID}/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == PLAYER_PROFILE.id
    assert data["nickname"] == PLAYER_PROFILE.nickname
    assert data["name"] == PLAYER_PROFILE.name
    assert data["nationality"] == PLAYER_PROFILE.nationality


def test_get_player_team_achievements(client):
    response = client.get(f"/players/{PLAYER_ID}/team-achievements")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == PLAYER_TEAM_ACHIEVEMENTS.id
    assert data["achievementCount"] >= PLAYER_TEAM_ACHIEVEMENTS.achievement_count
    assert len(data["achievements"]) > 0


def test_get_player_personal_achievements(client):
    response = client.get(f"/players/{PLAYER_ID}/personal-achievements")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == PLAYER_PERSONAL_ACHIEVEMENTS.id
    expected = PLAYER_PERSONAL_ACHIEVEMENTS.personal_achievements
    achievements = data["personalAchievements"]
    assert achievements["majorWinnerCount"] == expected.major_winner_count
    assert achievements["majorMvpCount"] == expected.major_mvp_count
    assert achievements["top20Count"] == expected.top_20_count


def test_get_player_trophies(client):
    response = client.get(f"/players/{PLAYER_ID}/trophies")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == PLAYER_TROPHIES.id
    assert data["trophyCount"] >= PLAYER_TROPHIES.trophy_count
    assert len(data["trophies"]) > 0


def test_get_player_stats(client):
    response = client.get(f"/players/{PLAYER_ID}/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == PLAYER_STATS.id

    expected = PLAYER_STATS.stats
    fp = data["stats"]["firepower"]
    assert fp["killsPerRound"] == expected.firepower.kills_per_round
    assert fp["killsPerRoundWin"] == expected.firepower.kills_per_round_win
    assert fp["damagePerRound"] == expected.firepower.damage_per_round
    assert fp["damagePerRoundWin"] == expected.firepower.damage_per_round_win
    assert fp["roundsWithAKillPercentage"] == expected.firepower.rounds_with_a_kill_percentage
    assert fp["rating10"] == expected.firepower.rating_1_0
    assert fp["roundsWithMultiKillPercentage"] == expected.firepower.rounds_with_multi_kill_percentage
    assert fp["pistolRoundRating"] == expected.firepower.pistol_round_rating

    en = data["stats"]["entrying"]
    assert en["savedByTeammatePerRound"] == expected.entrying.saved_by_teammate_per_round
    assert en["tradedDeathsPerRound"] == expected.entrying.traded_deaths_per_round
    assert en["tradedDeathsPercentage"] == expected.entrying.traded_deaths_percentage
    assert en["openingDeathsTradedPercentage"] == expected.entrying.opening_deaths_traded_percentage
    assert en["assistsPerRound"] == expected.entrying.assists_per_round
    assert en["supportRoundsPercentage"] == expected.entrying.support_rounds_percentage

    tr = data["stats"]["trading"]
    assert tr["savedTeammatePerRound"] == expected.trading.saved_teammate_per_round
    assert tr["tradeKillsPerRound"] == expected.trading.trade_kills_per_round
    assert tr["tradeKillsPercentage"] == expected.trading.trade_kills_percentage
    assert tr["assistedKillsPercentage"] == expected.trading.assisted_kills_percentage
    assert tr["damagePerKill"] == expected.trading.damage_per_kill

    op = data["stats"]["opening"]
    assert op["openingKillsPerRound"] == expected.opening.opening_kills_per_round
    assert op["openingDeathsPerRound"] == expected.opening.opening_deaths_per_round
    assert op["openingAttemptsPercentage"] == expected.opening.opening_attempts_percentage
    assert op["openingSuccessPercentage"] == expected.opening.opening_success_percentage
    assert op["winAfterOpeningKillPercentage"] == expected.opening.win_after_opening_kill_percentage

    cl = data["stats"]["clutching"]
    assert cl["clutchPointsPerRound"] == expected.clutching.clutch_points_per_round
    assert cl["lastAlivePercentage"] == expected.clutching.last_alive_percentage
    assert cl["savesPerRoundLossPercentage"] == expected.clutching.saves_per_round_loss_percentage

    sn = data["stats"]["sniping"]
    assert sn["sniperKillsPerRound"] == expected.sniping.sniper_kills_per_round
    assert sn["sniperKillsPercentage"] == expected.sniping.sniper_kills_percentage
    assert sn["roundsWithSniperKillsPercentage"] == expected.sniping.rounds_with_sniper_kills_percentage
    assert sn["sniperMultiKillRounds"] == expected.sniping.sniper_multi_kill_rounds
    assert sn["sniperOpeningKillsPerRound"] == expected.sniping.sniper_opening_kills_per_round

    ut = data["stats"]["utility"]
    assert ut["utilityDamagePerRound"] == expected.utility.utility_damage_per_round
    assert ut["utilityKillsPer100Rounds"] == expected.utility.utility_kills_per_100_rounds
    assert ut["flashesThrownPerRound"] == expected.utility.flashes_thrown_per_round
    assert ut["flashAssistsPerRound"] == expected.utility.flash_assists_per_round
    assert ut["timeOpponentFlashedPerRound"] == expected.utility.time_opponent_flashed_per_round


def test_get_player_career_stats(client):
    response = client.get(f"/players/{PLAYER_ID}/career-stats")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == PLAYER_CAREER_STATS.id
    expected = PLAYER_CAREER_STATS.stats
    stats = data["stats"]
    assert stats["totalKills"] == expected.total_kills
    assert stats["headshotPercentage"] == expected.headshot_percentage
    assert stats["totalDeaths"] == expected.total_deaths
    assert stats["kdRatio"] == expected.kd_ratio
    assert stats["damagePerRound"] == expected.damage_per_round
    assert stats["mapsPlayed"] == expected.maps_played
    assert stats["killsPerRound"] == expected.kills_per_round
    assert stats["assistsPerRound"] == expected.assists_per_round
