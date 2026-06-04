from tests.fixtures import RANKING_STATS


def test_get_ranking_stats(client):
    response = client.get(
        f"/ranking/stats/start-placement/{RANKING_STATS.start_placement}/end-placement/{RANKING_STATS.end_placement}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["startPlacement"] == RANKING_STATS.start_placement
    assert data["endPlacement"] == RANKING_STATS.end_placement
    expected_team = RANKING_STATS.ranking_stats[0]
    team = data["rankingStats"][0]
    assert team["placement"] == expected_team.placement
    assert team["hltvPoints"] == expected_team.hltv_points
    expected_nicknames = {p.nickname for p in expected_team.lineup}
    actual_nicknames = {p["nickname"] for p in team["lineup"]}
    assert expected_nicknames == actual_nicknames
