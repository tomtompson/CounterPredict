from app.schemas.base import AuditMixin, HLTVBaseModel


class PlayerStatsFirepower(HLTVBaseModel):
    kills_per_round: float | None
    kills_per_round_win: float | None
    damage_per_round: float | None = None
    damage_per_round_win: float | None
    rounds_with_a_kill_percentage: float | None
    rating_1_0: float | None
    rounds_with_multi_kill_percentage: float | None
    pistol_round_rating: float | None


class PlayerStatsEntrying(HLTVBaseModel):
    saved_by_teammate_per_round: float | None
    traded_deaths_per_round: float | None
    traded_deaths_percentage: float | None
    opening_deaths_traded_percentage: float | None
    assists_per_round: float | None
    support_rounds_percentage: float | None


class PlayerStatsTrading(HLTVBaseModel):
    saved_teammate_per_round: float | None
    trade_kills_per_round: float | None
    trade_kills_percentage: float | None
    assisted_kills_percentage: float | None
    damage_per_kill: float | None


class PlayerStatsOpening(HLTVBaseModel):
    opening_kills_per_round: float | None
    opening_deaths_per_round: float | None
    opening_attempts_percentage: float | None
    opening_success_percentage: float | None
    win_after_opening_kill_percentage: float | None
    attacks_per_round: float | None


class PlayerStatsClutching(HLTVBaseModel):
    clutch_points_per_round: float | None
    last_alive_percentage: float | None
    _1v1_win_percentage: float | None
    time_alive_per_round: float | None
    saves_per_round_loss_percentage: float | None


class PlayerStatsSniping(HLTVBaseModel):
    sniper_kills_per_round: float | None
    sniper_kills_percentage: float | None
    rounds_with_sniper_kills_percentage: float | None
    sniper_multi_kill_rounds: float | None
    sniper_opening_kills_per_round: float | None


class PlayerStatsUtility(HLTVBaseModel):
    utility_damage_per_round: float | None
    utility_kills_per_100_rounds: float | None
    flashes_thrown_per_round: float | None
    flash_assists_per_round: float | None
    time_opponent_flashed_per_round: float | None


class PlayerStatsRoles(HLTVBaseModel):
    firepower: PlayerStatsFirepower | None
    entrying: PlayerStatsEntrying | None
    trading: PlayerStatsTrading | None
    opening: PlayerStatsOpening | None
    clutching: PlayerStatsClutching | None
    sniping: PlayerStatsSniping | None
    utility: PlayerStatsUtility | None


class PlayerStats(HLTVBaseModel, AuditMixin):
    id: str
    stats: list[PlayerStatsRoles] | None = None
