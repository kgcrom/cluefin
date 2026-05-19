from pathlib import Path


def test_cluefin_cli_does_not_import_deleted_cli_packages() -> None:
    source_root = Path("apps/cluefin-cli/src/cluefin_cli")
    forbidden = ("cluefin_openapi_cli", "cluefin_ta_cli")

    for path in source_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for name in forbidden:
            assert name not in text, f"{path} must not import or reference {name}"
