"""Tests for cluefin-openapi integration."""

import shutil
from pathlib import Path
from unittest.mock import MagicMock

from cluefin_xbrl.integration import download_and_extract_statements, download_and_parse_xbrl

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _mock_download(destination, **kwargs):
    """Simulate DART download by copying fixture files to destination."""
    dest = Path(destination)
    dest.mkdir(parents=True, exist_ok=True)
    for f in FIXTURES_DIR.iterdir():
        if f.is_file():
            shutil.copy2(f, dest / f.name)
    return dest


class TestDownloadAndParseXbrl:
    def test_mock_download_and_parse(self, tmp_path):
        mock_client = MagicMock()
        mock_client.download_financial_statement_xbrl.side_effect = (
            lambda rcept_no, reprt_code, destination, overwrite: _mock_download(destination)
        )

        doc = download_and_parse_xbrl(
            mock_client,
            rcept_no="20240401000123",
            reprt_code="11011",
            destination=tmp_path / "xbrl_output",
            include_taxonomy=True,
        )

        assert len(doc.facts) == 3
        assert doc.entity_id == "00126380"
        assert doc.taxonomy is not None
        assert "Assets" in doc.taxonomy.labels

        mock_client.download_financial_statement_xbrl.assert_called_once()

    def test_default_temp_destination(self):
        mock_client = MagicMock()
        mock_client.download_financial_statement_xbrl.side_effect = (
            lambda rcept_no, reprt_code, destination, overwrite: _mock_download(destination)
        )

        doc = download_and_parse_xbrl(
            mock_client,
            rcept_no="20240401000123",
            reprt_code="11011",
        )

        assert len(doc.facts) == 3

        # Verify temp dir was used
        call_args = mock_client.download_financial_statement_xbrl.call_args
        dest_arg = call_args.kwargs.get("destination") or call_args[1].get("destination")
        assert "cluefin_xbrl_" in str(dest_arg)

        # Cleanup temp dir
        shutil.rmtree(dest_arg, ignore_errors=True)


class TestDownloadAndExtractStatements:
    def test_mock_extract(self, tmp_path):
        mock_client = MagicMock()
        mock_client.download_financial_statement_xbrl.side_effect = (
            lambda rcept_no, reprt_code, destination, overwrite: _mock_download(destination)
        )

        result = download_and_extract_statements(
            mock_client,
            rcept_no="20240401000123",
            reprt_code="11011",
            destination=tmp_path / "xbrl_output",
        )

        assert result.entity_id == "00126380"
        assert "BS" in result.statements
        bs = result.statements["BS"]
        concepts = [item.concept_local_name for item in bs.line_items]
        assert "Assets" in concepts
