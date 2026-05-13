from tests.fixtures import (
    EVENT_PROFILE,
    EVENT_RESULTS,
    EVENT_TEAM_STATS,
    EVENTS_SEARCH,
)

EVENT_ID = EVENT_PROFILE.id
TEAM_ID = EVENT_TEAM_STATS.team_id


def test_search_events(client):
    response = client.get(f"/events/search/{EVENTS_SEARCH.query}")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == EVENTS_SEARCH.query
    ids = [r["id"] for r in data["results"]]
    assert "3883" in ids  # IEM Katowice 2019


def test_get_event_profile(client):
    response = client.get(f"/events/{EVENT_ID}/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == EVENT_PROFILE.id
    profile = data["eventProfile"]
    expected = EVENT_PROFILE.event_profile
    assert profile["name"] == expected.name
    assert profile["teamCount"] == expected.team_count
    assert profile["prizePool"] == expected.prize_pool
    assert profile["location"] == expected.location
    assert profile["mvp"][0]["id"] == expected.mvp[0].id
    assert profile["mvp"][0]["nickname"] == expected.mvp[0].nickname


def test_get_event_team_stats(client):
    response = client.get(f"/events/{EVENT_ID}/team/{TEAM_ID}/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["eventId"] == EVENT_TEAM_STATS.event_id
    assert data["teamId"] == EVENT_TEAM_STATS.team_id
    expected = EVENT_TEAM_STATS.stats
    assert data["stats"]["teamPlacement"] == expected.team_placement
    assert data["stats"]["prize"][0]["prize"] == expected.prize[0].prize


def test_get_event_results(client):
    response = client.get(f"/events/{EVENT_ID}/results")
    assert response.status_code == 200
    data = response.json()
    assert data["eventId"] == EVENT_RESULTS.event_id
    assert data["resultCount"] > 0
    expected_first = EVENT_RESULTS.results[0]
    first = data["results"][0]
    assert first["matchId"] == expected_first.match_id
    assert first["team1Name"] == expected_first.team1_name
    assert first["team2Name"] == expected_first.team2_name
