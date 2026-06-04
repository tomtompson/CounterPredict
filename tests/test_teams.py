from tests.fixtures import (
    TEAM_ACHIEVEMENTS,
    TEAM_PROFILE,
    TEAM_RESULTS,
    TEAM_SEARCH,
    TEAM_UPCOMING_MATCHES,
)

TEAM_ID = TEAM_PROFILE.id


def test_search_teams(client):
    response = client.get(f"/teams/{TEAM_SEARCH.query}/search")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == TEAM_SEARCH.query
    first = data["results"][0]
    expected = TEAM_SEARCH.results[0]
    assert first["id"] == expected.id
    assert first["name"] == expected.name


def test_get_team_profile(client):
    response = client.get(f"/teams/{TEAM_ID}/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == TEAM_PROFILE.id
    profile = data["teamProfile"]
    expected = TEAM_PROFILE.team_profile
    assert profile["name"] == expected.name
    assert profile["worldRanking"] >= 1
    lineup_ids = [p["id"] for p in profile["lineup"]]
    for player in expected.lineup:
        assert player.id in lineup_ids


def test_get_team_achievements(client):
    response = client.get(f"/teams/{TEAM_ID}/achievements")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == TEAM_ACHIEVEMENTS.id
    assert data["achievementCount"] >= TEAM_ACHIEVEMENTS.achievement_count
    assert len(data["teamAchievements"]) > 0


def test_get_team_upcoming_matches(client):
    response = client.get(f"/teams/{TEAM_ID}/upcoming-matches")
    assert response.status_code == 200
    data = response.json()
    assert data["teamId"] == TEAM_UPCOMING_MATCHES.team_id
    assert "upcomingMatches" in data
    assert "matchCount" in data


def test_get_team_results(client):
    response = client.get(f"/teams/{TEAM_ID}/results/")
    assert response.status_code == 200
    data = response.json()
    assert data["teamId"] == TEAM_RESULTS.team_id
    assert data["resultCount"] > 0
    first = data["results"][0]
    assert "matchId" in first
    assert "team1Name" in first
    assert "team2Name" in first
    assert "matchDate" in first
