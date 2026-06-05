from app.schemas.base import AuditMixin, HLTVBaseModel


class MatchPastPlayerRoleSideStats(HLTVBaseModel):
    score: float | None = None
    stats: dict[str, float | str | None] | None = None


class MatchPastPlayerRole(HLTVBaseModel):
    combined: MatchPastPlayerRoleSideStats | None = None
    ct: MatchPastPlayerRoleSideStats | None = None
    t: MatchPastPlayerRoleSideStats | None = None


class MatchPastPlayerRoles(HLTVBaseModel):
    firepower: MatchPastPlayerRole | None = None
    entrying: MatchPastPlayerRole | None = None
    trading: MatchPastPlayerRole | None = None
    opening: MatchPastPlayerRole | None = None
    clutching: MatchPastPlayerRole | None = None
    sniping: MatchPastPlayerRole | None = None
    utility: MatchPastPlayerRole | None = None


class MatchPastPlayerStatsData(HLTVBaseModel):
    summary: dict[str, float | str | None] | None = None
    roles: MatchPastPlayerRoles | None = None


class MatchPastPlayerStatsItem(HLTVBaseModel):
    id: str
    name: str
    stats: MatchPastPlayerStatsData | None = None


class MatchPastPlayersStats(HLTVBaseModel, AuditMixin):
    match_id: int
    match_date: str | None = None
    players: list[MatchPastPlayerStatsItem] | None = None
