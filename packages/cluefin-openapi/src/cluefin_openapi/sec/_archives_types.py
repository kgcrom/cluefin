from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FilingIndexItem(BaseModel):
    """공시 폴더 안의 파일 하나 (`index.json`의 `directory.item[]`)."""

    model_config = ConfigDict(title="SEC 공시 폴더 항목", populate_by_name=True, extra="allow")

    name: str = Field(description="파일명")
    type: Optional[str] = Field(default=None, description="EDGAR 디렉터리 목록의 아이콘 종류 (text.gif, folder.gif)")
    size: Optional[int] = Field(default=None, description="크기(바이트). 하위 폴더는 None")
    last_modified: Optional[datetime] = Field(default=None, alias="last-modified", description="수정 시각")

    @field_validator("size", mode="before")
    @classmethod
    def _blank_size(cls, value: Any) -> Any:
        """SEC는 크기를 문자열로 주고, 폴더는 빈 문자열로 준다."""
        return None if value == "" else value


class FilingIndex(BaseModel):
    """공시 폴더 목록 (`Archives/edgar/data/{cik}/{접수번호}/index.json`)."""

    model_config = ConfigDict(title="SEC 공시 폴더", populate_by_name=True, extra="allow")

    name: str = Field(description="폴더 경로 (/Archives/edgar/data/320193/000032019323000106)")
    parent_dir: Optional[str] = Field(default=None, alias="parent-dir", description="상위 폴더 경로")
    items: List[FilingIndexItem] = Field(default_factory=list, alias="item", description="파일 목록")
