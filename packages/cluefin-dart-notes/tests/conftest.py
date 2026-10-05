"""합성 원문 문서(실제 공시가 아니며 관찰한 세대별 구조만 흉내 낸다)와 통합 테스트용 원문 디렉터리."""

import os
from pathlib import Path

import pytest

from cluefin_dart_notes import DartDocument, load_document

# 2024년 이후 정기보고서: 메타가 루트 바로 아래, 사업의 내용·재무제표가 LIBRARY 안, 맨 앞에 정정신고 블록.
PERIODIC_RECENT = """<?xml version="1.0" encoding="utf-8"?>
<DOCUMENT>
<DOCUMENT-NAME ACODE="11012">반기보고서</DOCUMENT-NAME>
<FORMULA-VERSION ADATE="20260101">6.7</FORMULA-VERSION>
<COMPANY-NAME AREGCIK="00000001">가나다 주식회사</COMPANY-NAME>
<SUMMARY><EXTRACTION ACODE="IFRS_YN">Y</EXTRACTION><EXTRACTION>코드 없음</EXTRACTION></SUMMARY>
<BODY>
<COVER><COVER-TITLE ATOC="Y" AASSOCNOTE="COVER">반 기 보 고 서</COVER-TITLE></COVER>
<LIBRARY>
<CORRECTION>
<TITLE ATOC="Y" AASSOCNOTE="CORRECTION" ENG="Report of Disclosure Revision" ATOCID="90">정 정 신 고 (보고)</TITLE>
<P>1. 정정대상 공시서류 : 반기보고서</P>
</CORRECTION>
</LIBRARY>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="TTL_CEO_CERT" ATOCID="2">【 대표이사 등의 확인 】</TITLE></SECTION-1>
<SECTION-1>
<TITLE ATOC="Y" ENG="I. Overview" ATOCID="3">I. 회사의 개요</TITLE>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-1-1-0" ATOCID="4">1. 회사의 개요</TITLE><P>본문</P></SECTION-2>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-1-2-0" ATOCID="5">2. 회사의   연혁</TITLE></SECTION-2>
</SECTION-1>
<SECTION-1>
<TITLE ATOC="Y" AASSOCNOTE="D-0-2-0-0" ATOCID="6">II. 사업의 내용</TITLE>
<LIBRARY>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="L-0-2-1-L1" ATOCID="7">1. 사업의 개요</TITLE></SECTION-2>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="L-0-2-2-L1" ATOCID="8">2. 주요 제품 및 서비스</TITLE></SECTION-2>
</LIBRARY>
</SECTION-1>
<SECTION-1>
<TITLE ATOC="Y" AASSOCNOTE="D-0-3-0-0" ATOCID="9">III. 재무에 관한 사항</TITLE>
<LIBRARY>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-3-3-0" ATOCID="10">3. 연결재무제표 주석</TITLE></SECTION-2>
</LIBRARY>
<SECTION-2>
<TITLE ATOC="Y" AASSOCNOTE="D-0-3-7-0" ATOCID="11">7. 증권의 발행을 통한 자금조달에 관한 사항</TITLE>
<SECTION-3><TITLE ATOC="Y" AASSOCNOTE="D-0-3-7-1" ATOCID="12">7-1. 증권의 발행을 통한 자금조달 실적</TITLE></SECTION-3>
</SECTION-2>
</SECTION-1>
</BODY>
</DOCUMENT>
"""

# 2017~2021년 정기보고서: 메타가 DOCUMENT-HEADER 안, ENG·ATOCID 없음, cp949, 사업의 내용 하위 섹션 없음.
PERIODIC_LEGACY = """<?xml version="1.0" encoding="utf-8"?>
<DOCUMENT>
<DOCUMENT-HEADER>
<DOCUMENT-NAME ACODE="11011">사업보고서</DOCUMENT-NAME>
<FORMULA-VERSION ADATE="20170101">3.2</FORMULA-VERSION>
<COMPANY-NAME AREGCIK="00000002">라마바(주)</COMPANY-NAME>
</DOCUMENT-HEADER>
<BODY>
<SECTION-1><TITLE ATOC="Y">I. 회사의 개요</TITLE>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-1-1-0">1. 회사의 개요</TITLE></SECTION-2>
</SECTION-1>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-2-0-0">II. 사업의 내용</TITLE><P>R&D 본문</P></SECTION-1>
</BODY>
</DOCUMENT>
"""

# 감사보고서 단독: 같은 D-0-2-0-0 이 "외부감사 실시내용"이다.
AUDIT_REPORT = """<?xml version="1.0" encoding="utf-8"?>
<DOCUMENT>
<DOCUMENT-NAME ACODE="00761">연결감사보고서</DOCUMENT-NAME>
<FORMULA-VERSION ADATE="20260101">6.0</FORMULA-VERSION>
<COMPANY-NAME AREGCIK="00000003">사아자 주식회사</COMPANY-NAME>
<SUMMARY>
<EXTRACTION ACODE="AUDIT_CIK">00000009</EXTRACTION>
<EXTRACTION ACODE="TOT_ASSETS"> 1,234 </EXTRACTION>
</SUMMARY>
<BODY>
<LIBRARY><SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-0-1-0">독립된 감사인의 감사보고서</TITLE></SECTION-1></LIBRARY>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-0-0-0">(첨부)연 결 재 무 제 표</TITLE>
<SECTION-2><TITLE ATOC="Y" AASSOCNOTE="D-0-1-0-0">주석</TITLE></SECTION-2>
</SECTION-1>
<SECTION-1><TITLE ATOC="Y" AASSOCNOTE="D-0-2-0-0">외부감사 실시내용</TITLE></SECTION-1>
</BODY>
</DOCUMENT>
"""


@pytest.fixture
def periodic_recent_bytes() -> bytes:
    return PERIODIC_RECENT.encode("utf-8")


@pytest.fixture
def periodic_legacy_bytes() -> bytes:
    return PERIODIC_LEGACY.encode("cp949")


@pytest.fixture
def audit_report_bytes() -> bytes:
    return AUDIT_REPORT.encode("utf-8")


@pytest.fixture(scope="session")
def corpus_paths() -> list[Path]:
    """`CLUEFIN_DART_NOTES_TEST_DIR` 아래의 원문 XML(하위 폴더 포함). 없으면 통합 테스트를 건너뛴다."""
    directory = os.getenv("CLUEFIN_DART_NOTES_TEST_DIR")
    if not directory:
        pytest.skip("CLUEFIN_DART_NOTES_TEST_DIR is not set")
    paths = sorted(Path(directory).rglob("*.xml"))
    if not paths:
        pytest.skip(f"no *.xml under {directory}")
    return paths


@pytest.fixture(scope="session")
def corpus_documents(corpus_paths) -> list[DartDocument]:
    return [load_document(path) for path in corpus_paths]
