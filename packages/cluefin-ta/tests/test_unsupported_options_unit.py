"""
ta-lib options that are not implemented must fail loudly.

Code ported from ta-lib by changing only the import would otherwise get an SMA where it
asked for another MA type, with no error. Does not import talib.
"""

import numpy as np
import pytest

from cluefin_ta import BBANDS, STOCH, STOCHF

N = 40
CLOSE = np.linspace(100.0, 140.0, N)
HIGH = CLOSE + 1.0
LOW = CLOSE - 1.0


@pytest.mark.parametrize(
    ("call", "option"),
    [
        (lambda: BBANDS(CLOSE, matype=1), "matype=1"),
        (lambda: STOCH(HIGH, LOW, CLOSE, slowk_matype=1), "slowk_matype=1"),
        (lambda: STOCH(HIGH, LOW, CLOSE, slowd_matype=2), "slowd_matype=2"),
        (lambda: STOCHF(HIGH, LOW, CLOSE, fastd_matype=1), "fastd_matype=1"),
    ],
)
def test_non_sma_matype_raises(call, option):
    with pytest.raises(ValueError, match=option):
        call()


def test_sma_matype_is_accepted():
    BBANDS(CLOSE, matype=0)
    STOCH(HIGH, LOW, CLOSE, slowk_matype=0, slowd_matype=0)
    STOCHF(HIGH, LOW, CLOSE, fastd_matype=0)
