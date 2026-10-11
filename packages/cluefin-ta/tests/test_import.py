import cluefin_ta


def test_public_api_exports():
    """__all__에 선언된 모든 이름이 실제로 import 가능해야 한다."""
    assert cluefin_ta.__version__
    for name in cluefin_ta.__all__:
        assert getattr(cluefin_ta, name, None) is not None, f"missing export: {name}"
