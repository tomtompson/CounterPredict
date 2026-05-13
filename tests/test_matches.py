from tests.fixtures import LIVE_MATCHES, MATCH_STATS, TODAY_MATCHES

MATCH_ID = MATCH_STATS.match_id


def test_get_live_matches(client):
    response = client.get("/matches/live")
    assert response.status_code == 200
    data = response.json()
    assert "liveMatchsCount" in data
    assert isinstance(data["liveMatchsCount"], int)
    assert isinstance(data["liveMatchs"], list)


def test_get_today_matches(client):
    response = client.get("/matches/today/")
    assert response.status_code == 200
    data = response.json()
    assert "matchCount" in data
    assert isinstance(data["matchCount"], int)
    assert isinstance(data["matches"], list)


def test_get_match_stats(client):
    response = client.get(f"/matches/stats/{MATCH_ID}")
    assert response.status_code == 200
    data = response.json()
    expected = MATCH_STATS
    assert data["matchId"] == expected.match_id
    assert data["matchUrl"] == expected.match_url
    assert data["isLive"] == expected.is_live
    assert data["stats"]["matchInfo"]["team1"]["name"] == expected.stats.match_info.team1.name
    assert data["stats"]["matchInfo"]["team1"]["score"] == expected.stats.match_info.team1.score
    assert data["stats"]["matchInfo"]["team2"]["name"] == expected.stats.match_info.team2.name
    assert data["stats"]["matchInfo"]["team2"]["score"] == expected.stats.match_info.team2.score
