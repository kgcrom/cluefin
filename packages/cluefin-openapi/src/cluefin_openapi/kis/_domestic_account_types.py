from __future__ import annotations

from typing import Dict, Mapping, Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class StockQuoteCurrentItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(alias="KRX_FWDG_ORD_ORGNO", description="거래소코드", max_length=5)
    odno: str = Field(alias="ODNO", description="주문번호", max_length=10)
    ord_tmd: str = Field(alias="ORD_TMD", description="주문시간", max_length=6)


class StockQuoteCurrent(BaseModel, KisHttpBody):
    """주식주문(현금) 응답"""

    items: Sequence[StockQuoteCurrentItem] = Field(default_factory=list)


class StockQuoteCreditItem(BaseModel):
    krx_fwdg_ord_orgno: str = Field(alias="KRX_FWDG_ORD_ORGNO", description="거래소코드", max_length=5)
    odno: str = Field(alias="ODNO", description="주문번호", max_length=10)
    ord_tmd: str = Field(alias="ORD_TMD", description="주문시간", max_length=6)


class StockQuoteCredit(BaseModel, KisHttpBody):
    """주식주문(신용) 응답"""

    items: Sequence[StockQuoteCreditItem] = Field(default_factory=list)
