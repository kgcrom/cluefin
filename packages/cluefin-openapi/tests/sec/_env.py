"""SEC integration tests take SEC_USER_AGENT from `.env.test`, like every other integration suite.

Loaded at import (collection) time so the module-level skip below sees it.
"""

import os
from pathlib import Path

import dotenv
import pytest

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[4] / ".env.test")

SEC_USER_AGENT = os.getenv("SEC_USER_AGENT")

requires_user_agent = pytest.mark.skipif(not SEC_USER_AGENT, reason="SEC_USER_AGENT 미설정 (.env.test)")
