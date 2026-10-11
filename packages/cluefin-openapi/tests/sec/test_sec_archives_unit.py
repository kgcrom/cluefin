"""Unit tests for SEC Archives: filing folder index and file downloads."""

from datetime import datetime
from pathlib import Path

import pytest
import requests_mock

from cluefin_openapi.sec import Client, FilingIndex, SecAPIError

USER_AGENT = "Cluefin Test test@example.com"
FOLDER = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106"


@pytest.fixture
def client() -> Client:
    return Client(user_agent=USER_AGENT)


def _item(name: str, size: str = "100", type_: str = "text.gif") -> dict:
    return {"last-modified": "2023-11-02 18:08:27", "name": name, "type": type_, "size": size}


INLINE_10K_INDEX = {
    "directory": {
        "item": [
            _item("0000320193-23-000106-index-headers.html"),
            _item("0000320193-23-000106-index.html"),
            _item("0000320193-23-000106.txt"),
            _item("Financial_Report.xlsx"),
            _item("FilingSummary.xml"),
            _item("MetaLinks.json"),
            _item("R1.htm"),
            _item("R2.htm"),
            _item("aapl-20230930.htm"),
            _item("aapl-20230930.xsd"),
            _item("aapl-20230930_cal.xml"),
            _item("aapl-20230930_def.xml"),
            _item("aapl-20230930_htm.xml"),
            _item("aapl-20230930_lab.xml"),
            _item("aapl-20230930_pre.xml"),
            _item("a10-kexhibit2119.htm"),
            _item("report.css"),
            _item("graphic", size="", type_="folder.gif"),
        ],
        "name": "/Archives/edgar/data/320193/000032019323000106",
        "parent-dir": "/Archives/edgar/data/320193/",
    }
}
XBRL_NAMES = [
    "aapl-20230930.xsd",
    "aapl-20230930_cal.xml",
    "aapl-20230930_def.xml",
    "aapl-20230930_htm.xml",
    "aapl-20230930_lab.xml",
    "aapl-20230930_pre.xml",
]


def test_filing_index(client: Client):
    with requests_mock.Mocker() as m:
        m.get(f"{FOLDER}/index.json", json=INLINE_10K_INDEX)
        index = client.archives.filing_index(320193, "0000320193-23-000106")

    assert isinstance(index, FilingIndex)
    assert index.name == "/Archives/edgar/data/320193/000032019323000106"
    assert index.parent_dir == "/Archives/edgar/data/320193/"
    by_name = {item.name: item for item in index.items}
    assert by_name["aapl-20230930.htm"].size == 100
    assert by_name["aapl-20230930.htm"].last_modified == datetime(2023, 11, 2, 18, 8, 27)
    assert by_name["graphic"].size is None


def test_filing_index_without_directory_fails_loudly(client: Client):
    with requests_mock.Mocker() as m:
        m.get(f"{FOLDER}/index.json", json={"error": "x"})
        with pytest.raises(SecAPIError, match="directory"):
            client.archives.filing_index(320193, "000032019323000106")


def test_download_filing_document(client: Client, tmp_path: Path):
    with requests_mock.Mocker() as m:
        m.get(f"{FOLDER}/aapl-20230930.htm", content=b"<html>10-K</html>")
        path = client.archives.download_filing_document(
            "0000320193", "0000320193-23-000106", "aapl-20230930.htm", destination=tmp_path / "out"
        )
    assert path == tmp_path / "out" / "aapl-20230930.htm"
    assert path.read_bytes() == b"<html>10-K</html>"


def test_download_filing_document_refuses_to_overwrite(client: Client, tmp_path: Path):
    (tmp_path / "aapl-20230930.htm").write_bytes(b"old")
    with requests_mock.Mocker() as m:
        with pytest.raises(FileExistsError):
            client.archives.download_filing_document(
                320193, "0000320193-23-000106", "aapl-20230930.htm", destination=tmp_path
            )
        assert m.call_count == 0

        m.get(f"{FOLDER}/aapl-20230930.htm", content=b"new")
        client.archives.download_filing_document(
            320193, "0000320193-23-000106", "aapl-20230930.htm", destination=tmp_path, overwrite=True
        )
    assert (tmp_path / "aapl-20230930.htm").read_bytes() == b"new"


@pytest.mark.parametrize("name", ["../index.json", "xslF345X05/form4.xml", ""])
def test_download_filing_document_rejects_paths(client: Client, tmp_path: Path, name: str):
    with pytest.raises(ValueError, match="파일명"):
        client.archives.download_filing_document(320193, "0000320193-23-000106", name, destination=tmp_path)


def test_download_xbrl_files_picks_instance_schema_and_linkbases(client: Client, tmp_path: Path):
    with requests_mock.Mocker() as m:
        m.get(f"{FOLDER}/index.json", json=INLINE_10K_INDEX)
        for name in XBRL_NAMES:
            m.get(f"{FOLDER}/{name}", content=name.encode())
        paths = client.archives.download_xbrl_files(320193, "0000320193-23-000106", destination=tmp_path)

    assert [p.name for p in paths] == XBRL_NAMES
    assert all(p.read_bytes() == p.name.encode() for p in paths)


def test_download_xbrl_files_keeps_pre_2019_instance_and_skips_r_files(client: Client, tmp_path: Path):
    index = {
        "directory": {
            "item": [
                _item("FilingSummary.xml"),
                _item("R1.xml"),
                _item("R22.xml"),
                _item("aapl-20100925.xml"),
                _item("aapl-20100925.xsd"),
                _item("aapl-20100925_pre.xml"),
                _item("d10k.htm"),
            ],
            "name": "/Archives/edgar/data/320193/000119312510238044",
        }
    }
    folder = "https://www.sec.gov/Archives/edgar/data/320193/000119312510238044"
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, content=b"x")  # registered first: later matchers take precedence
        m.get(f"{folder}/index.json", json=index)
        paths = client.archives.download_xbrl_files(320193, "0001193125-10-238044", destination=tmp_path)
    assert [p.name for p in paths] == ["aapl-20100925.xml", "aapl-20100925.xsd", "aapl-20100925_pre.xml"]


def test_download_xbrl_files_without_schema_raises(client: Client, tmp_path: Path):
    index = {"directory": {"item": [_item("wk-form4_1700519405.xml"), _item("0000320193-23-000110.txt")], "name": "x"}}
    with requests_mock.Mocker() as m:
        m.get(f"{FOLDER}/index.json", json=index)
        with pytest.raises(SecAPIError, match="XBRL"):
            client.archives.download_xbrl_files(320193, "0000320193-23-000106", destination=tmp_path)
        assert m.call_count == 1


def test_download_xbrl_files_checks_every_target_before_downloading(client: Client, tmp_path: Path):
    (tmp_path / "aapl-20230930_pre.xml").write_bytes(b"old")
    with requests_mock.Mocker() as m:
        m.get(f"{FOLDER}/index.json", json=INLINE_10K_INDEX)
        with pytest.raises(FileExistsError, match="_pre.xml"):
            client.archives.download_xbrl_files(320193, "0000320193-23-000106", destination=tmp_path)
        assert m.call_count == 1
    assert sorted(p.name for p in tmp_path.iterdir()) == ["aapl-20230930_pre.xml"]
