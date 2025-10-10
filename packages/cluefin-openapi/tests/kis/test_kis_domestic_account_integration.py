"""Integration tests for the KIS domestic account module.

These tests hit the real KIS sandbox API and therefore require valid
credentials and account/order configuration to be present in the
environment (or in `.env.test`).
"""

import os
import time
from typing import Dict, Optional

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._client import Client
from cluefin_openapi.kis._domestic_account_types import StockQuoteCurrent

# TODO: integration test
