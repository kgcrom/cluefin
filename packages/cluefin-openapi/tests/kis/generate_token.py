"""Utility script to generate and cache a KIS API token.

Run this script once to generate a token that will be cached for ~24 hours.
This allows you to run integration tests without hitting the 1-minute rate limit.
"""

import os
import sys
from pathlib import Path

import dotenv
from pydantic import SecretStr

# Add the parent directory to the path so we can import the token cache
sys.path.insert(0, str(Path(__file__).parent))

from _token_cache import TokenCache
from cluefin_openapi.kis._auth import Auth


def main():
    """Generate and cache a KIS API token."""
    # Load environment variables
    dotenv.load_dotenv(dotenv_path=".env.test")

    app_key = os.getenv("KIS_APP_KEY")
    secret_key = os.getenv("KIS_SECRET_KEY")
    env = os.getenv("KIS_ENV", "dev")

    if not app_key or not secret_key:
        print("Error: KIS_APP_KEY and KIS_SECRET_KEY must be set in .env.test")
        sys.exit(1)

    print(f"Generating token for KIS API ({env} environment)...")

    # Create auth and token cache
    auth = Auth(app_key=app_key, secret_key=SecretStr(secret_key), env=env)
    cache = TokenCache(auth)

    # Generate and cache token
    token = cache.get()

    print(f"✓ Token generated successfully!")
    print(f"  Access token: {token.access_token[:20]}...")
    print(f"  Expires at: {token.access_token_token_expired}")
    print(f"  Token type: {token.token_type}")
    print(f"  Cached to: {cache._cache_file}")
    print(f"\nYou can now run integration tests without waiting for rate limits.")


if __name__ == "__main__":
    main()
