"""dart4 원문 XML에서 쓰이는 태그 이름.

공식 dart4.xsd를 구하지 못해 2017~2026년 정기보고서·감사보고서 원문에서 관찰한 이름을 모았다.
목록 밖의 `<`는 원문 텍스트(`<기후변화>` 같은)로 보고 escape하므로, 진짜 태그가 빠져 있으면
그 태그가 텍스트로 본문에 섞인다. `EscapeUnknownTags`가 닫는 태그 짝이 있는 미지 이름을 경고로
보고하니, 그 경고가 나오면 여기에 추가한다.
"""

KNOWN_TAGS: frozenset[str] = frozenset(
    {
        "A",
        "APPENDIX",
        "BODY",
        "BR",
        "COL",
        "COLGROUP",
        "COMMENT",
        "COMPANY-NAME",
        "CORRECTION",  # [기재정정] 보고서 맨 앞의 정정신고 블록
        "COVER",
        "COVER-TITLE",
        "DOCUMENT",
        "DOCUMENT-HEADER",
        "DOCUMENT-NAME",
        "EXTRACTION",
        "FILENAME",
        "FORMULA-VERSION",
        "IMAGE",
        "IMG",
        "IMG-CAPTION",
        "INSERTION",
        "LIBRARY",
        "LIBRARYLIST",
        "P",
        "PGBRK",
        "SECTION-1",
        "SECTION-2",
        "SECTION-3",
        "SPAN",
        "SUMMARY",
        "TABLE",
        "TABLE-GROUP",
        "TBODY",
        "TD",
        "TE",
        "TH",
        "THEAD",
        "TITLE",
        "TOC",
        "TR",
        "TU",
        "WARNING",
    }
)
