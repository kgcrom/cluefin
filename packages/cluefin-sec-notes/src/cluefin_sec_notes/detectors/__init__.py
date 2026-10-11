"""Item 시작 위치 탐지기. 신뢰도 높은 순으로 채택되는 캐스케이드다(`extract_items`)."""

from cluefin_sec_notes.detectors._base import Detection, DetectionContext, Detector
from cluefin_sec_notes.detectors._pattern import PatternDetector
from cluefin_sec_notes.detectors._style import HeadingStyleDetector
from cluefin_sec_notes.detectors._toc import TocAnchorDetector
from cluefin_sec_notes.detectors._xref import CrossReferenceDetector

DEFAULT_DETECTORS: tuple[Detector, ...] = (
    TocAnchorDetector(),
    CrossReferenceDetector(),
    PatternDetector(),
    HeadingStyleDetector(),
)

__all__ = [
    "DEFAULT_DETECTORS",
    "CrossReferenceDetector",
    "Detection",
    "DetectionContext",
    "Detector",
    "HeadingStyleDetector",
    "PatternDetector",
    "TocAnchorDetector",
]
