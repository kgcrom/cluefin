from datetime import datetime

import pytest


@pytest.mark.integration
def test_generate_token(auth):
    response = auth.generate_token()

    assert response.token is not None
    assert response.token_type.startswith("Bearer")
    assert isinstance(response.expires_dt, datetime)
