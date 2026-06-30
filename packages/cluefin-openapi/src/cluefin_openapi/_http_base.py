"""Shared HTTP-client infrastructure for kis, dart, and kiwoom clients."""

import json
from typing import Dict, Optional

import requests


class BaseHttpClient:
    """Mixin holding request helpers shared by all broker HTTP clients.

    Phase 2 adds the shared retry/dispatch loop (`_execute_with_retry`) here.
    For now it only owns the two byte-identical helpers that were copy-pasted
    across dart/_client.py, kis/_http_client.py, and kiwoom/_client.py.
    """

    def _safe_json(self, response: requests.Response) -> Optional[Dict]:
        """Safely parse a JSON response, returning None if parsing fails."""
        try:
            return response.json()
        except (ValueError, json.JSONDecodeError):
            return None

    def _get_retry_after(self, response: requests.Response) -> Optional[int]:
        """Extract the Retry-After header as an int, or None."""
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return int(retry_after)
            except ValueError:
                pass
        return None
