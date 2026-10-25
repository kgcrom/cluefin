import cluefin_dart_notes


def test_public_api_exports():
    """__all__에 선언된 모든 이름이 실제로 import 가능해야 한다."""
    assert cluefin_dart_notes.__version__
    for name in cluefin_dart_notes.__all__:
        assert getattr(cluefin_dart_notes, name, None) is not None, f"missing export: {name}"
