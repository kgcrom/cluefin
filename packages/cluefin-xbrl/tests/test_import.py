def test_package_importable():
    import cluefin_xbrl

    assert cluefin_xbrl.__version__


def test_public_api_exports():
    """__all__에 선언된 모든 이름이 실제로 import 가능해야 한다."""
    import cluefin_xbrl

    for name in cluefin_xbrl.__all__:
        assert getattr(cluefin_xbrl, name, None) is not None, f"missing export: {name}"
