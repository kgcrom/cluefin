from cluefin_desk.formatting import pad


class TestPad:
    def test_ascii_pads_to_width(self):
        assert pad("ROE", 6) == "ROE   "
        assert pad("ROE", 6, "right") == "   ROE"

    def test_korean_is_measured_in_terminal_cells(self):
        # 4 글자 = 8 셀이므로 폭 10 이면 두 칸만 채워야 한다 (파이썬 포맷은 6 칸을 채운다)
        assert pad("삼성전자", 10) == "삼성전자  "
        assert len(pad("삼성전자", 10)) == 6

    def test_none_becomes_dash(self):
        assert pad(None, 3) == "-  "

    def test_longer_than_width_is_not_truncated(self):
        assert pad("아주긴종목이름입니다", 4) == "아주긴종목이름입니다"

    def test_non_string_is_coerced(self):
        assert pad(12, 4, "right") == "  12"
