"""블록 추출. 모든 조각은 합성이며 관찰한 원문 구조만 흉내 낸다."""

from defusedxml.ElementTree import fromstring

from cluefin_dart_notes import Heading, Paragraph, Table, extract_blocks, parse_document, table_to_rows
from cluefin_dart_notes.repair import DartXmlRepairer


def blocks_of(body: str):
    root, _ = DartXmlRepairer(strict=True).parse(f"<SECTION-2><TITLE>3. 제목</TITLE>{body}</SECTION-2>".encode())
    return extract_blocks(root)


def only(blocks, kind):
    return [block for block in blocks if isinstance(block, kind)]


class TestParagraphText:
    def test_source_newlines_between_runs_become_spaces_and_cr_becomes_newline(self):
        blocks = blocks_of("<P>\n<SPAN>주소 : </SPAN>\n<SPAN>가나시 다라구</SPAN>&cr;<SPAN>  둘째   줄 </SPAN>\n</P>")

        assert blocks == [Paragraph("주소 : 가나시 다라구\n둘째 줄")]

    def test_br_is_a_line_break_and_repeated_breaks_collapse(self):
        assert blocks_of("<P>첫 줄<BR/><BR/>둘째 줄&cr;&cr;</P>") == [Paragraph("첫 줄\n둘째 줄")]

    def test_empty_paragraphs_are_dropped(self):
        assert blocks_of("<P>&cr;&cr;</P><P> <SPAN></SPAN> </P><P>본문</P>") == [Paragraph("본문")]

    def test_bold_run_offsets(self):
        blocks = blocks_of(
            '<P>반영되었습니다.\n<SPAN USERMARK="F-10 B">16. 영업 현금</SPAN>당기 중 내용입니다.'
            '<SPAN USERMARK="BC0XDCDCDC">배경색은 굵게가 아님</SPAN></P>'
        )

        (paragraph,) = blocks
        assert paragraph.text == "반영되었습니다. 16. 영업 현금당기 중 내용입니다.배경색은 굵게가 아님"
        assert paragraph.bold_starts == (paragraph.text.index("16."),)

    def test_bold_paragraph_and_nested_bold_count_once(self):
        (paragraph,) = blocks_of('<P USERMARK="B"><SPAN USERMARK="B">1. 일반사항</SPAN></P>')

        assert paragraph.bold_starts == (0,)

    def test_empty_bold_span_leaves_no_mark(self):
        (paragraph,) = blocks_of('<P>앞<SPAN USERMARK="B"> </SPAN>뒤</P>')

        assert paragraph.bold_starts == ()


class TestStructure:
    def test_order_titles_and_nested_sections(self):
        blocks = blocks_of(
            "<P>머리말</P>"
            '<TABLE-GROUP><TITLE ATOC="Y" AASSOCNOTE="D-0-3-3-1" ATOCID="7">1. 일반사항 (연결)</TITLE>'
            "<P>노트 본문</P></TABLE-GROUP>"
            "<PGBRK/><IMAGE>a.jpg</IMAGE>"
            "<SECTION-3><TITLE>하위</TITLE><P>하위 본문</P></SECTION-3>"
            "<LIBRARY><P>꼬리말</P></LIBRARY>"
        )

        assert blocks == [
            Paragraph("머리말"),
            Heading("1. 일반사항 (연결)", "D-0-3-3-1", "7"),
            Paragraph("노트 본문"),
            Paragraph("꼬리말"),
        ]

    def test_section_blocks_property(self, periodic_legacy_bytes):
        document = parse_document(periodic_legacy_bytes)
        business = document.sections[1]

        assert business.blocks == (Paragraph("R&D 본문"),)
        assert document.sections[0].blocks == ()


class TestTables:
    def test_grid_expands_spans(self):
        (table,) = blocks_of(
            '<TABLE BORDER="1"><THEAD><TR><TH ROWSPAN="2">구분</TH><TH COLSPAN="2">당기</TH></TR>'
            "<TR><TH>1분기</TH><TH>2분기</TH></TR></THEAD>"
            '<TBODY><TR><TD>매출</TD><TE ACODE="ifrs_Revenue">1,000</TE><TE>(20)</TE></TR></TBODY></TABLE>'
        )

        assert table.bordered
        assert (table.n_rows, table.n_cols) == (3, 3)
        assert table_to_rows(table) == [["구분", "당기", "당기"], ["구분", "1분기", "2분기"], ["매출", "1,000", "(20)"]]
        assert table.grid[0][1] is table.grid[0][2]
        assert table.grid[0][0].row_span == 2 and table.grid[0][0].is_header
        assert table.grid[2][1].acode == "ifrs_Revenue" and not table.grid[2][1].is_header

    def test_ragged_rows_are_padded(self):
        (table,) = blocks_of('<TABLE BORDER="1"><TR><TD>a</TD><TD>b</TD></TR><TR><TD>c</TD></TR></TABLE>')

        assert table.grid[1][1] is None
        assert table.to_rows() == [["a", "b"], ["c", ""]]

    def test_tu_unit_attributes(self):
        (table,) = blocks_of(
            '<TABLE BORDER="1"><TR><TU AUNIT="UNIT_WON" AUNITVALUE="1000000">금액</TU><TD>x</TD></TR></TABLE>'
        )

        cell = table.grid[0][0]
        assert (cell.aunit, cell.aunit_value, cell.is_header) == ("UNIT_WON", "1000000", True)

    def test_cell_paragraphs_are_separate_lines(self):
        (table,) = blocks_of('<TABLE BORDER="1"><TR><TD><P>첫째</P>\n<P>둘째</P></TD><TD>x</TD></TR></TABLE>')

        assert table.grid[0][0].text == "첫째\n둘째"

    def test_caption_table_is_attached_to_next_data_table(self):
        blocks = blocks_of(
            '<TABLE BORDER="0"><TR><TD>(기준일 :</TD><TD>2026년 06월 30일</TD><TD>)</TD><TD>(단위 : 주, %)</TD></TR></TABLE>'
            '<TABLE BORDER="1"><TR><TD>a</TD><TD>1</TD></TR></TABLE>'
        )

        (table,) = blocks
        assert table.unit == "주, %"
        assert table.caption == "(기준일 : 2026년 06월 30일 ) (단위 : 주, %)"

    def test_statement_title_table_with_several_rows_is_a_caption(self):
        blocks = blocks_of(
            '<TABLE BORDER="0"><TR><TD>연결 재무상태표</TD></TR><TR><TD>제 2 기 반기말</TD></TR>'
            "<TR><TD>제 1 기말</TD></TR><TR><TD>(단위 : 백만원)</TD></TR></TABLE>"
            '<TABLE BORDER="1"><TR><TD>자산</TD><TD>1</TD></TR></TABLE>'
        )

        assert [b.unit for b in only(blocks, Table)] == ["백만원"]

    def test_unattached_caption_table_stays_a_block(self):
        blocks = blocks_of(
            '<TABLE BORDER="0"><TR><TD>(단위 : 원)</TD><TD>x</TD></TR></TABLE><P>표가 아닌 문단</P>'
            '<TABLE BORDER="0"><TR><TD>(단위 : 주)</TD><TD>y</TD></TR></TABLE>'
        )

        assert [type(b).__name__ for b in blocks] == ["Table", "Paragraph", "Table"]
        assert not any(b.bordered for b in only(blocks, Table))

    def test_unit_from_short_paragraph_or_last_line(self):
        blocks = blocks_of(
            '<P>(단위 : 백만원)</P><TABLE BORDER="1"><TR><TD>a</TD><TD>1</TD></TR></TABLE>'
            '<P>상기 금액은 설명입니다.&cr;(단위: 대)</P><TABLE BORDER="1"><TR><TD>b</TD><TD>2</TD></TR></TABLE>'
            "<P>긴 문단 안의 단위 : 원 언급은 표 단위가 아니고 그냥 문장의 일부입니다 정말로 그렇습니다</P>"
            '<TABLE BORDER="1"><TR><TD>c</TD><TD>3</TD></TR></TABLE>'
        )

        assert [b.unit for b in only(blocks, Table)] == ["백만원", "대", None]
        assert only(blocks, Paragraph)[0].text == "(단위 : 백만원)"

    def test_unit_from_first_row_of_data_table(self):
        (table,) = blocks_of(
            '<TABLE BORDER="1"><TR><TD COLSPAN="2">(단위: 천원)</TD></TR><TR><TD>a</TD><TD>1</TD></TR></TABLE>'
        )

        assert table.unit == "천원"

    def test_layout_table_is_unwrapped(self):
        blocks = blocks_of(
            '<TABLE BORDER="0"><TR><TD>안내 <SPAN USERMARK="B">굵게</SPAN><P>문단</P>꼬리'
            '<TABLE BORDER="1"><TR><TD>x</TD><TD>1</TD></TR></TABLE></TD></TR></TABLE>'
            '<TABLE BORDER="1"><TR><TD><P>1×1 상자</P></TD></TR></TABLE>'
            '<TABLE BORDER="1"><TR><TD> </TD></TR></TABLE>'
        )

        assert [type(b).__name__ for b in blocks] == ["Paragraph", "Paragraph", "Paragraph", "Table", "Paragraph"]
        assert blocks[0] == Paragraph("안내 굵게", (3,))
        assert [b.text for b in only(blocks, Paragraph)] == ["안내 굵게", "문단", "꼬리", "1×1 상자"]
        assert only(blocks, Table)[0].to_rows() == [["x", "1"]]


def test_extract_blocks_accepts_any_element():
    element = fromstring("<TD><P>a</P></TD>".encode())

    assert extract_blocks(element) == [Paragraph("a")]
