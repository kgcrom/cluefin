"""cluefin-sec-notes: SEC EDGAR 공시 원문(10-K/10-Q/8-K HTML) 파서"""

__version__ = "0.1.0"

from cluefin_sec_notes._blocks import Block, Cell, Link, PageBreak, Paragraph, Table
from cluefin_sec_notes._document import SecDocument, block_text, load_filing, parse_filing
from cluefin_sec_notes._report import (
    ENCODING_FALLBACK,
    FIX_KINDS,
    HIDDEN_CONTENT,
    IMPLICIT_CLOSE,
    LAYOUT_TABLE,
    MISNESTED_END,
    STRAY_END_TAG,
    UNCLOSED_AT_EOF,
    UNKNOWN_TAG,
    ParseFix,
    ParseReport,
    SourceSample,
)

__all__ = [
    "Block",
    "Cell",
    "ENCODING_FALLBACK",
    "FIX_KINDS",
    "HIDDEN_CONTENT",
    "IMPLICIT_CLOSE",
    "LAYOUT_TABLE",
    "Link",
    "MISNESTED_END",
    "PageBreak",
    "Paragraph",
    "ParseFix",
    "ParseReport",
    "STRAY_END_TAG",
    "SecDocument",
    "SourceSample",
    "Table",
    "UNCLOSED_AT_EOF",
    "UNKNOWN_TAG",
    "block_text",
    "load_filing",
    "parse_filing",
]
