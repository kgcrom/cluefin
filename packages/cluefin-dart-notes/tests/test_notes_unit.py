"""주석 분할. 모든 문서는 합성이며 관찰한 원문 구조만 흉내 낸다."""

import logging

from cluefin_dart_notes import Paragraph, Table, extract_notes, notes_sections, parse_document, split_notes


def periodic(consolidated_body: str, separate_body: str = "<P>1. 일반사항</P>") -> bytes:
    return f"""<DOCUMENT><DOCUMENT-NAME ACODE="11012">반기보고서</DOCUMENT-NAME><BODY>
<SECTION-1><TITLE AASSOCNOTE="D-0-3-0-0">III. 재무에 관한 사항</TITLE><LIBRARY>
<SECTION-2><TITLE AASSOCNOTE="D-0-3-3-0">3. 연결재무제표 주석</TITLE>{consolidated_body}</SECTION-2>
<SECTION-2><TITLE AASSOCNOTE="D-0-3-5-0">5. 재무제표 주석</TITLE>{separate_body}</SECTION-2>
</LIBRARY></SECTION-1></BODY></DOCUMENT>""".encode()


def consolidated(body: str):
    document = parse_document(periodic(body))
    section, basis = notes_sections(document)[0]
    return split_notes(section, basis)


def texts(note):
    return [block.text if isinstance(block, Paragraph) else "TABLE" for block in note.blocks]


class TestSections:
    def test_periodic_report_has_consolidated_then_separate(self):
        document = parse_document(periodic("<P>1. 일반사항</P>"))

        assert [(section.title, basis) for section, basis in notes_sections(document)] == [
            ("3. 연결재무제표 주석", "consolidated"),
            ("5. 재무제표 주석", "separate"),
        ]

    def test_audit_report_basis_follows_document_code(self, audit_report_bytes):
        consolidated_audit = parse_document(audit_report_bytes)
        separate_audit = parse_document(audit_report_bytes.replace(b'ACODE="00761"', b'ACODE="00760"'))

        assert [(s.title, b) for s, b in notes_sections(consolidated_audit)] == [("주석", "consolidated")]
        assert [b for _, b in notes_sections(separate_audit)] == ["separate"]

    def test_sections_without_codes_are_found_by_title_and_missing_ones_skipped(self):
        raw = (
            '<DOCUMENT><DOCUMENT-NAME ACODE="11011">사업보고서</DOCUMENT-NAME><BODY>'
            "<SECTION-2><TITLE>3. 연결재무제표 주석</TITLE><P>1. 일반사항</P></SECTION-2></BODY></DOCUMENT>"
        ).encode()

        assert [(s.title, b) for s, b in notes_sections(parse_document(raw))] == [
            ("3. 연결재무제표 주석", "consolidated")
        ]

    def test_extract_notes_returns_both_bases(self):
        notes = extract_notes(parse_document(periodic("<P>1. 일반사항</P><P>2. 현금</P>")))

        assert [(note.number, note.basis) for note in notes] == [
            ("1", "consolidated"),
            ("2", "consolidated"),
            ("1", "separate"),
        ]


class TestHeadingMethod:
    BODY = (
        '<TABLE-GROUP><TITLE ATOC="Y">1. 일반사항 (연결)</TITLE><P>본문 1</P></TABLE-GROUP>'
        '<TABLE-GROUP><TITLE ATOC="Y">9-1. 리스 (연결)</TITLE><P>본문 2</P>'
        '<TABLE BORDER="1"><TR><TD>a</TD><TD>1</TD></TR></TABLE></TABLE-GROUP>'
        '<TABLE-GROUP><TITLE ATOC="Y">6-A. 금융상품</TITLE></TABLE-GROUP>'
        '<TABLE-GROUP><TITLE ATOC="Y">9 &amp; 10. 유형자산 및 무형자산</TITLE><TITLE>소제목 없는 TITLE</TITLE>'
        "<P>본문 3</P></TABLE-GROUP>"
    )

    def test_numbers_are_strings_and_basis_suffix_is_dropped(self):
        result = consolidated(self.BODY)

        assert result.method == "heading"
        assert [(note.number, note.title) for note in result.notes] == [
            ("1", "일반사항"),
            ("9-1", "리스"),
            ("6-A", "금융상품"),
            ("9&10", "유형자산 및 무형자산"),
        ]
        assert result.notes[0].heading == "1. 일반사항 (연결)"
        assert result.notes[0].basis == "consolidated"

    def test_blocks_belong_to_their_note(self):
        notes = consolidated(self.BODY).notes

        assert texts(notes[1]) == ["본문 2", "TABLE"]
        assert notes[2].blocks == ()
        assert [type(block).__name__ for block in notes[3].blocks] == ["Heading", "Paragraph"]


class TestSequenceMethod:
    def test_paragraph_start_headings(self):
        result = consolidated(
            "<P>머리말</P><P>1. 일반사항</P><P>본문 1</P><P>2.1 작성기준</P><P>2. 중요한 회계정책</P>"
            "<P>2.1 작성기준</P><P>(1) 세부</P><P>3. 현금및현금성자산 : </P><P>본문 3</P>"
        )

        assert result.method == "sequence"
        assert [(note.number, note.title) for note in result.notes] == [
            ("1", "일반사항"),
            ("2", "중요한 회계정책"),
            ("3", "현금및현금성자산"),
        ]
        assert texts(result.notes[0]) == ["본문 1", "2.1 작성기준"]
        assert texts(result.notes[1]) == ["2.1 작성기준", "(1) 세부"]
        assert [block.text for block in result.preamble] == ["머리말"]
        assert result.warnings == ()

    def test_inline_heading_needs_colon_after_sentence_end(self):
        result = consolidated(
            "<P>1. 일반사항</P><P>변동 사항은 없습니다.2. 중요한 회계정책 : 다음은 정책입니다. 3. 문장 속 번호는 제목이 아님</P>"
        )

        assert [(note.number, note.title) for note in result.notes] == [("1", "일반사항"), ("2", "중요한 회계정책")]
        assert texts(result.notes[0]) == ["변동 사항은 없습니다."]
        assert texts(result.notes[1]) == ["다음은 정책입니다. 3. 문장 속 번호는 제목이 아님"]

    def test_bold_heading_inside_paragraph_needs_no_colon(self):
        result = consolidated(
            "<P>1. 일반사항</P>"
            '<P>법인세가 반영되었습니다.\n<SPAN USERMARK="B">2. 영업으로부터 창출된 현금</SPAN>당기 중 현금은 다음과 같습니다.'
            '<SPAN USERMARK="B">3. 리스</SPAN></P>'
        )

        assert [(note.number, note.title) for note in result.notes] == [
            ("1", "일반사항"),
            ("2", "영업으로부터 창출된 현금"),
            ("3", "리스"),
        ]
        assert texts(result.notes[0]) == ["법인세가 반영되었습니다."]
        assert texts(result.notes[1]) == ["당기 중 현금은 다음과 같습니다."]
        assert result.notes[2].blocks == ()

    def test_bold_title_stops_before_merged_sub_heading(self):
        result = consolidated(
            '<P><SPAN USERMARK="B">1. 금융수익과 금융비용</SPAN> <SPAN USERMARK="B">1.1 금융수익</SPAN>내용</P>'
        )

        (note,) = result.notes
        assert note.title == "금융수익과 금융비용"
        assert texts(note) == ["1.1 금융수익내용"]
        assert note.blocks[0].bold_spans == ((0, 8),)

    def test_title_glued_to_body_is_cut_at_body_start(self):
        result = consolidated(
            "<P>1. 일반사항주식회사 가나다는 설립되었습니다.</P><P>2. 보고기간후사건회사는 결의하였습니다.</P>"
            "<P>3. 유형자산(1) 보고기간말 현재 내용은 다음과 같습니다.</P>"
        )

        assert [note.title for note in result.notes] == ["일반사항", "보고기간후사건", "유형자산"]
        assert [texts(note) for note in result.notes] == [
            ["주식회사 가나다는 설립되었습니다."],
            ["회사는 결의하였습니다."],
            ["(1) 보고기간말 현재 내용은 다음과 같습니다."],
        ]

    def test_long_line_title_without_body_marker_is_cut_at_a_word(self):
        result = consolidated(
            "<P>1. 기타포괄손익공정가치측정금융자산과 상각후원가측정금융자산 및 파생상품 거래내역 요약표</P>"
            "<P>2. 마흔 자 이하의 제목은 본문 표지가 없으면 그대로 둔다</P>"
        )

        first, second = result.notes
        assert (
            first.title == "기타포괄손익공정가치측정금융자산과 상각후원가측정금융자산 및 파생상품"
        )  # 40자 안의 마지막 공백
        assert texts(first) == ["거래내역 요약표"]
        assert second.title == "마흔 자 이하의 제목은 본문 표지가 없으면 그대로 둔다"
        assert second.blocks == ()

    def test_table_cells_are_not_candidates(self):
        result = consolidated(
            '<P>1. 일반사항</P><TABLE BORDER="1"><TR><TD>2. 당기순이익</TD><TD>57.18</TD></TR></TABLE><P>2. 현금</P>'
        )

        assert [note.number for note in result.notes] == ["1", "2"]
        assert isinstance(result.notes[0].blocks[0], Table)

    def test_one_missing_number_is_allowed_and_warned(self):
        result = consolidated("<P>1. 일반사항</P><P>3. 현금</P><P>4. 리스</P>")

        assert [note.number for note in result.notes] == ["1", "3", "4"]
        assert result.warnings == ("2번 노트가 없습니다(3번으로 건너뜀).",)

    def test_two_missing_numbers_stop_the_split_and_are_warned(self):
        result = consolidated(
            '<P>1. 일반사항</P><TABLE BORDER="1"><TR><TD>a</TD><TD>1</TD></TR></TABLE><P>4. 리스</P><P>5. 차입금</P>'
        )

        assert [note.number for note in result.notes] == ["1"]
        assert len(result.warnings) == 1 and "놓쳤을 수" in result.warnings[0]

    def test_no_notes(self, caplog):
        document = parse_document(periodic("<P>본문만 있습니다.</P>"))

        with caplog.at_level(logging.WARNING):
            notes = extract_notes(document)

        assert [note.basis for note in notes] == ["separate"]
        assert "하나도 찾지 못했습니다" in caplog.text
