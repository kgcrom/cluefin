from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SolEtfListItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    fund_code: str
    etf_code: str
    name: str
    badges: list[str] = Field(default_factory=list)
    pension_flags: list[str] = Field(default_factory=list)
    nav: Decimal | None = None
    aum: Decimal | None = None
    detail_url: str
    returns: dict[str, str | None] = Field(default_factory=dict)
    raw: dict[str, object] = Field(default_factory=dict)

    @field_validator("nav", "aum", mode="before")
    @classmethod
    def _empty_decimal_to_none(cls, value: object) -> object:
        if value == "":
            return None
        return value
