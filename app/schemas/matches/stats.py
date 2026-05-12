from app.schemas.base import AuditMixin, HLTVBaseModel


class PlayerStatSide(HLTVBaseModel):
    nickname: str
    id: int | None
    side: str
    kd: str
    swing: float
    adr: float
    kast: float
    rating: float


class TeamSideStats(HLTVBaseModel):
    ct_side: list[PlayerStatSide]
    t_side: list[PlayerStatSide]


class MapScore(HLTVBaseModel):
    score: int | None
    ct: int | None
    tr: int | None


class MapStats(HLTVBaseModel):
    map_index: int
    map_stats_id: int | None
    map_name: str | None
    team1_score: MapScore
    team2_score: MapScore
    team1: TeamSideStats
    team2: TeamSideStats


class TeamInfo(HLTVBaseModel):
    name: str
    id: int | None
    score: int


class EventInfo(HLTVBaseModel):
    name: str | None
    id: int | None


class MatchInfo(HLTVBaseModel):
    team1: TeamInfo
    team2: TeamInfo
    match_date: str | None
    match_time: str | None
    unix_timestamp: int | None
    event: EventInfo


class MatchStatsData(HLTVBaseModel):
    match_info: MatchInfo
    map_pool: list[str]
    map_stats: list[MapStats]


class MatchStats(HLTVBaseModel, AuditMixin):
    match_id: int | None
    match_url: str | None
    is_live: bool = False
    stats: MatchStatsData
