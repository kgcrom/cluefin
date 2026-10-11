"""Item 시작 위치 탐지기. 신뢰도 높은 순으로 채택되는 캐스케이드다(`extract_items`)."""

from cluefin_sec_notes.detectors._base import Detection, DetectionContext, Detector
from cluefin_sec_notes.detectors._toc import TocAnchorDetector

DEFAULT_DETECTORS: tuple[Detector, ...] = (TocAnchorDetector(),)

__all__ = ["DEFAULT_DETECTORS", "Detection", "DetectionContext", "Detector", "TocAnchorDetector"]
