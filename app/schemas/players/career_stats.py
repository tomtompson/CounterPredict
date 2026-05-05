from app.schemas.base import AuditMixin, HLTVBaseModel


class PlayerCareerStatsDetails(HLTVBaseModel):
    total_kills: float | None = None
    headshot_percentage: float | None = None
    total_deaths: float | None = None
    kd_ratio: float | None = None
    damage_per_round: float | None = None
    maps_played: int | None = None
    rounds_played: int | None = None
    kills_per_round: float | None = None
    assists_per_round: float | None = None
    saved_by_teammate_per_round: float | None = None
    saved_teammates_per_round: float | None = None
    rating_1_0: float | None = None


class PlayerCareerStats(HLTVBaseModel, AuditMixin):
    id: str
    stats: PlayerCareerStatsDetails | None = None
