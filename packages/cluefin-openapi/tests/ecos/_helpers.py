"""ECOS 단위 테스트 공용: 픽스처 읽기와 'sample 키 쪽 넘김' 흉내 서버."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import requests_mock

FIXTURES = Path(__file__).parent / "fixtures"
BASE = "https://ecos.bok.or.kr/api"
SAMPLE_LIMIT_MESSAGE = (
    "조회건수 값의 타입이 유효하지 않습니다. 조회건수 값을 확인하십시오!\n"
    " 조회건수 값의 타입이 유효하지 않으면 오류를 발생합니다. \n sample은 최대 10건 이내에서 호출이 가능합니다."
)

# /api/{서비스}/{키}/json/{언어}/{시작}/{끝}/...
_PATH = re.compile(r"^/api/(?P<service>\w+)/(?P<key>[^/]+)/json/(?P<lang>\w+)/(?P<start>\d+)/(?P<end>\d+)")


def load(name: str) -> Dict[str, Any]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def result(code: str, message: str = "") -> Dict[str, Any]:
    return {"RESULT": {"CODE": code, "MESSAGE": message}}


def serve_rows(mocker: requests_mock.Mocker, service: str, rows: List[Dict[str, Any]], sample_limit: int = 10):
    """URL 의 행 범위대로 잘라 주는 가짜 ECOS. sample 키로 sample_limit 를 넘기면 ERROR-301."""

    def respond(request, context):
        groups = _PATH.match(request.path).groupdict()
        start, end = int(groups["start"]), int(groups["end"])
        if groups["key"] == "sample" and end - start + 1 > sample_limit:
            return result("ERROR-301", SAMPLE_LIMIT_MESSAGE)
        page = rows[start - 1 : end]
        if not page:
            return result("INFO-200", "해당하는 데이터가 없습니다.")
        return {service: {"list_total_count": len(rows), "row": page}}

    return mocker.get(re.compile(rf"^{re.escape(BASE)}/{service}/"), json=respond)
