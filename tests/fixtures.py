from app.schemas.events import (
    EventMvpDetail,
    EventProfile,
    EventProfileDetail,
    EventResultDetails,
    EventResults,
    EventsSearch,
    EventTeamStats,
    EventTeamStatsDetails,
    PrizeDetails,
)
from app.schemas.matches import (
    EventInfo,
    LiveMatches,
    MatchInfo,
    MatchStats,
    MatchStatsData,
    TeamInfo,
    TodayMatches,
)
from app.schemas.players import (
    PersonalAchievementDetail,
    PlayerCareerStats,
    PlayerCareerStatsDetails,
    PlayerPersonalAchievements,
    PlayerProfile,
    PlayerSearch,
    PlayerSearchResult,
    PlayerStats,
    PlayerStatsClutching,
    PlayerStatsEntrying,
    PlayerStatsFirepower,
    PlayerStatsOpening,
    PlayerStatsRoles,
    PlayerStatsSniping,
    PlayerStatsTrading,
    PlayerStatsUtility,
    PlayerTeamAchievements,
    PlayerTrophies,
)
from app.schemas.ranking import (
    LineupDetails as RankingLineupDetails,
)
from app.schemas.ranking import (
    RankingStats,
    RankingStatsDetails,
)
from app.schemas.teams import (
    CoachDetails,
    TeamAchievements,
    TeamProfile,
    TeamProfileDetails,
    TeamResults,
    TeamSearch,
    TeamSearchResult,
    UpcomingMatches,
)
from app.schemas.teams import (
    LineupDetails as TeamLineupDetails,
)

# ---------------------------------------------------------------------------
# Players
# ---------------------------------------------------------------------------

PLAYER_SEARCH = PlayerSearch(
    query="s1mple",
    results=[
        PlayerSearchResult(
            id="7998",
            name="Oleksandr Kostyliev",
            nickname="s1mple",
            nationality="Ukraine",
            flag_url="https://www.hltv.org/img/static/flags/30x20/UA.gif",
            url="https://www.hltv.org/player/7998/s1mple",
        )
    ],
)

PLAYER_PROFILE = PlayerProfile(
    id="7998",
    url="https://www.hltv.org/player/7998/s1mple",
    nickname="s1mple",
    name="Oleksandr Kostyliev",
    age=28,
    nationality="Ukraine",
    rating=1.12,
    current_team="BC.Game",
    current_team_url="https://www.hltv.org/team/12878/bcgame",
    image_url="https://img-cdn.hltv.org/playerbodyshot/kIHjh9sr2gW8b-xmLfW4Oq.png?ixlib=java-2.1.0&w=400&s=64dfb77304c7c004658a0e7a43d67cad",
    social_media=None,
)

PLAYER_TEAM_ACHIEVEMENTS = PlayerTeamAchievements(
    id="7998",
    achievement_count=56,
    achievements=[],
)

PLAYER_PERSONAL_ACHIEVEMENTS = PlayerPersonalAchievements(
    id="7998",
    personal_achievements=PersonalAchievementDetail(
        major_winner_count=1,
        major_mvp_count=1,
        mvp_winner_count=21,
        evp_count=37,
        top_20_count=8,
    ),
)

PLAYER_TROPHIES = PlayerTrophies(
    id="7998",
    trophy_count=18,
    trophies=[],
)

PLAYER_STATS = PlayerStats(
    id="7998",
    stats=PlayerStatsRoles(
        firepower=PlayerStatsFirepower(
            kills_per_round=0.84,
            kills_per_round_win=1.15,
            damage_per_round=85.0,
            damage_per_round_win=90.6,
            rounds_with_a_kill_percentage=53.9,
            rating_1_0=1.23,
            rounds_with_multi_kill_percentage=22.2,
            pistol_round_rating=1.2,
        ),
        entrying=PlayerStatsEntrying(
            saved_by_teammate_per_round=0.08,
            traded_deaths_per_round=0.09,
            traded_deaths_percentage=14.2,
            opening_deaths_traded_percentage=12.3,
            assists_per_round=0.11,
            support_rounds_percentage=14.5,
        ),
        trading=PlayerStatsTrading(
            saved_teammate_per_round=0.11,
            trade_kills_per_round=0.12,
            trade_kills_percentage=14.8,
            assisted_kills_percentage=17.4,
            damage_per_kill=81.0,
        ),
        opening=PlayerStatsOpening(
            opening_kills_per_round=0.14,
            opening_deaths_per_round=0.09,
            opening_attempts_percentage=23.1,
            opening_success_percentage=61.6,
            win_after_opening_kill_percentage=74.6,
            attacks_per_round=2.14,
        ),
        clutching=PlayerStatsClutching(
            clutch_points_per_round=0.03,
            last_alive_percentage=10.2,
            _1v1_win_percentage=64.0,
            time_alive_per_round=59.0,
            saves_per_round_loss_percentage=9.1,
        ),
        sniping=PlayerStatsSniping(
            sniper_kills_per_round=0.32,
            sniper_kills_percentage=38.3,
            rounds_with_sniper_kills_percentage=23.7,
            sniper_multi_kill_rounds=0.09,
            sniper_opening_kills_per_round=0.08,
        ),
        utility=PlayerStatsUtility(
            utility_damage_per_round=2.52,
            utility_kills_per_100_rounds=0.52,
            flashes_thrown_per_round=0.57,
            flash_assists_per_round=0.04,
            time_opponent_flashed_per_round=2.05,
        ),
    ),
)

PLAYER_CAREER_STATS = PlayerCareerStats(
    id="7998",
    stats=PlayerCareerStatsDetails(
        total_kills=41402.0,
        headshot_percentage=41.2,
        total_deaths=31171.0,
        kd_ratio=1.33,
        damage_per_round=85.0,
        maps_played=1888,
        kills_per_round=0.84,
        assists_per_round=0.11,
        saved_by_teammate_per_round=0.08,
        saved_teammates_per_round=0.11,
    ),
)


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------

TEAM_SEARCH = TeamSearch(
    query="natus vincere",
    results=[
        TeamSearchResult(
            id="4608",
            name="Natus Vincere",
            country="Europe",
            url="https://www.hltv.org/team/4608/natus-vincere",
            team_logo_url="https://img-cdn.hltv.org/teamlogo/9iMirAi7ArBLNU8p3kqUTZ.svg?ixlib=java-2.1.0&s=4dd8635be16122656093ae9884675d0c",
            lineup=None,
        )
    ],
)

TEAM_PROFILE = TeamProfile(
    id="4608",
    team_profile=TeamProfileDetails(
        name="Natus Vincere",
        valve_ranking=3,
        world_ranking=2,
        weeks_in_top30_for_core=148,
        average_player_age=24.0,
        lineup=[
            TeamLineupDetails(id="9816", nickname="Aleksib"),
            TeamLineupDetails(id="14759", nickname="iM"),
            TeamLineupDetails(id="18987", nickname="b1t"),
            TeamLineupDetails(id="20127", nickname="w0nderful"),
            TeamLineupDetails(id="22673", nickname="makazze"),
        ],
        coach=[CoachDetails(id="472", nickname="B1ad3")],
        logo_url=None,
        social_media=None,
    ),
)

TEAM_ACHIEVEMENTS = TeamAchievements(
    id="4608",
    achievement_count=105,
    team_achievements=[],
)

TEAM_UPCOMING_MATCHES = UpcomingMatches(
    team_id="4608",
    upcoming_matches=None,
    match_count=0,
    timezone="UTC",
)

TEAM_RESULTS = TeamResults(
    team_id="4608",
    results=[],
    result_count=0,
)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

EVENTS_SEARCH = EventsSearch(
    query="IEM Katowice",
    results=None,
)

EVENT_PROFILE = EventProfile(
    id="7148",
    event_profile=EventProfileDetail(
        name="PGL CS2 Major Copenhagen 2024",
        start_date="Mar 21st 2024",
        end_date="Mar 31st 2024",
        team_count=16,
        prize_pool=1250000,
        location="Copenhagen, Denmark",
        location_flag_url="https://www.hltv.org/img/static/flags/30x20/DK.gif",
        mvp=[
            EventMvpDetail(
                id="19206",
                nickname="jL",
                event_stats="https://www.hltv.org/stats/players/19206/who?event=7148",
            )
        ],
        evps=None,
        teams=[],
    ),
)

EVENT_TEAM_STATS = EventTeamStats(
    event_id="7148",
    team_id="4608",
    stats=EventTeamStatsDetails(
        team_placement="1st",
        prize=[PrizeDetails(prize=500000, club_share=None)],
        vrs=None,
        qualify_method="Europe RMR A",
        lineup=[],
        coach=None,
    ),
)

EVENT_RESULTS = EventResults(
    event_id="7148",
    results=[
        EventResultDetails(
            match_url="https://www.hltv.org/matches/2370727/faze-vs-natus-vincere-pgl-cs2-major-copenhagen-2024",
            match_id="2370727",
            match_date="2024-03-31",
            team1_name="FaZe",
            team1_logo=None,
            team1_score=1,
            team2_name="Natus Vincere",
            team2_logo=None,
            team2_score=2,
            match_type="bo3",
            match_won=None,
        )
    ],
    result_count=40,
)


# ---------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------

RANKING_STATS = RankingStats(
    start_placement=1,
    end_placement=1,
    ranking_date="2026-05-11",
    ranking_stats=[
        RankingStatsDetails(
            team_id="9565",
            team_name="Vitality",
            placement=1,
            hltv_points=1000,
            logo_url="https://img-cdn.hltv.org/teamlogo/yeXBldn9w8LZCgdElAenPs.png?ixlib=java-2.1.0&w=50&s=15eaba0b75250065d20162d2cb05e3e6",
            lineup=[
                RankingLineupDetails(
                    player_id="7322",
                    nickname="apEX",
                    nationality="France",
                    picture_url="https://img-cdn.hltv.org/playerbodyshot/3M9h08qvl3YOsaRcAvKhs4.png?bg=3e4c54&h=200&ixlib=java-2.1.0&rect=121%2C0%2C467%2C467&w=200&s=35368eff8b418f421339d96c83c5cf3f",
                ),
                RankingLineupDetails(
                    player_id="11816",
                    nickname="ropz",
                    nationality="Estonia",
                    picture_url="https://img-cdn.hltv.org/playerbodyshot/YQ9kQQ3aop1JZQE9xJ140r.png?bg=3e4c54&h=200&ixlib=java-2.1.0&rect=117%2C8%2C467%2C467&w=200&s=6a04eac3ad99e2e75838eae47df2ee97",
                ),
                RankingLineupDetails(
                    player_id="11893",
                    nickname="ZywOo",
                    nationality="France",
                    picture_url="https://img-cdn.hltv.org/playerbodyshot/blnoWFtH8GUJZjhr8H0P4u.png?bg=3e4c54&h=200&ixlib=java-2.1.0&rect=121%2C8%2C467%2C467&w=200&s=b1042678b6af57a2f029eb7a5eb79c10",
                ),
                RankingLineupDetails(
                    player_id="16693",
                    nickname="flameZ",
                    nationality="Israel",
                    picture_url="https://img-cdn.hltv.org/playerbodyshot/LUQi5dX9boyO0uDadUGht5.png?bg=3e4c54&h=200&ixlib=java-2.1.0&rect=121%2C8%2C467%2C467&w=200&s=0d6e89c20fa62ca1e8bec46074e936cc",
                ),
                RankingLineupDetails(
                    player_id="18462",
                    nickname="mezii",
                    nationality="United Kingdom",
                    picture_url="https://img-cdn.hltv.org/playerbodyshot/7GVUrVLAQkgnuovRkk5Bxw.png?bg=3e4c54&h=200&ixlib=java-2.1.0&rect=117%2C8%2C467%2C467&w=200&s=a48f2791f78b51e6fefa5f54346cdb07",
                ),
            ],
        )
    ],
)


# ---------------------------------------------------------------------------
# Matches
# ---------------------------------------------------------------------------

LIVE_MATCHES = LiveMatches(
    live_matchs_count=0,
    live_matchs=[],
)

TODAY_MATCHES = TodayMatches(
    match_count=0,
    matches=[],
)

MATCH_STATS = MatchStats(
    match_id=2374287,
    match_url="https://www.hltv.org/matches/2374287/project-g-vs-ruby-cct-season-2-europe-series-8-closed-qualifier",
    is_live=False,
    stats=MatchStatsData(
        match_info=MatchInfo(
            team1=TeamInfo(name="Project G", id="12502", score="2"),
            team2=TeamInfo(name="RUBY", id="12694", score="1"),
            match_date="4th of August 2024",
            match_time="11:00",
            unix_timestamp="1722762000000",
            event=EventInfo(name=None, id=None),
        ),
        map_pool=[],
        map_stats=[],
    ),
)
