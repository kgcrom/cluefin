"""SEC integration tests read SEC_USER_AGENT only.

`.env` is the production pair for the brokers too, so it is read with
``dotenv_values`` instead of ``load_dotenv``: loading it would push KIS/Kiwoom prod
settings into ``os.environ`` for every test collected after this module.
"""

import os
from pathlib import Path

import dotenv
import pytest

_REPO_ROOT = Path(__file__).resolve().parents[4]

SEC_USER_AGENT = os.environ.get("SEC_USER_AGENT") or dotenv.dotenv_values(_REPO_ROOT / ".env").get("SEC_USER_AGENT")

requires_user_agent = pytest.mark.skipif(not SEC_USER_AGENT, reason="SEC_USER_AGENT 미설정 (.env)")
