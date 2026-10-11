"""코퍼스 스크립트 공용: manifest 읽기·쓰기, SEC 클라이언트, 원문 경로 규칙.

manifest는 JSON 배열이고 항목마다 `cik`, `accession`, `form`, `file`(주 문서 파일명)이 있다. 원문은
`<코퍼스 폴더>/<form 폴더>/<accession>/<file>`에 둔다. 기업명·접수번호가 든 manifest는 커밋하지 않는다
(`docs/plans/sec-notes-corpus/`, git 무시).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MANIFEST_DIR = REPO_ROOT / "docs" / "plans" / "sec-notes-corpus"


def sec_client():
    import dotenv
    from cluefin_openapi.sec import Client

    dotenv.load_dotenv(REPO_ROOT / ".env.test")
    user_agent = os.getenv("SEC_USER_AGENT")
    if not user_agent:
        raise SystemExit("SEC_USER_AGENT가 없습니다 (.env.test)")
    return Client(user_agent)


def read_manifest(path: Path) -> list[dict]:
    return json.loads(path.read_text()) if path.exists() else []


def write_manifest(path: Path, entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=1, ensure_ascii=False) + "\n")


def form_folder(form: str) -> str:
    return form.upper().replace("/", "_")


def filing_path(root: Path, entry: dict) -> Path:
    return root / form_folder(entry["form"]) / entry["accession"] / entry["file"]
