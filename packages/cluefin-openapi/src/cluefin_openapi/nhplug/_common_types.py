from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugHttpBody


class AccountItem(BaseModel):
    acct_no: str = Field(description="계좌번호 (이후 API 의 입력 `act_no` 에 사용)")
    acct_type: Literal["01", "02", "03"] = Field(
        description="계좌구분 (01: 자계좌, 02: 주문대리인계좌, 03: 모의투자계좌)"
    )


class AccountList(BaseModel):
    """계좌 목록 조회 (`POST /n2/acctinfo`) 응답."""

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    cust_no: str | None = Field(default=None, description="고객번호")
    output_0: list[AccountItem] | None = Field(default=None, alias="Output_0", description="보유 계좌 목록")


class WebsocketCloseResponse(NHPlugHttpBody):
    """실시간(Websocket) 세션해제 (`POST /websocket/close/session`) 응답."""

    pass
