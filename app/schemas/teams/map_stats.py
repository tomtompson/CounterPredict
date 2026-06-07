from app.schemas.base import AuditMixin, HLTVBaseModel


class TeamMapStats(HLTVBaseModel):
    wins_draws_losses: str | None
    win_rate: float | None
    total_rounds: int | None
    round_win_after_first_kill: float | None
    round_win_after_first_death: float | None
    pick_rate: float | None
    ban_rate: float | None


class TeamMap(HLTVBaseModel):
    map_name: str
    stats: TeamMapStats


class TeamMapStatsResponse(HLTVBaseModel, AuditMixin):
    id: int
    maps: list[TeamMap]