from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel


class AuditMixin(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.now)


class HLTVBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @field_validator("age", mode="before", check_fields=False)
    @classmethod
    def parse_age(cls, v: str | int) -> int | None:
        if isinstance(v, int):
            return v
        if v and v.isdigit():
            return int(v)
        return None

    @field_validator("rating", mode="before", check_fields=False)
    @classmethod
    def parse_rating(cls, v: str) -> float | None:
        try:
            return float(v)
        except ValueError, TypeError:
            return None
