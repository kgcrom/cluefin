"""
Core implementation dispatcher for cluefin-ta.

Automatically selects Numba-accelerated implementations when available,
falling back to pure NumPy implementations otherwise.
"""

try:
    from numba import jit  # noqa: F401

    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False


_impl = None


def get_impl():
    """
    Get the implementation module (cached).

    Returns the Numba-accelerated module if Numba is installed,
    otherwise returns the pure NumPy module.
    """
    global _impl
    if _impl is None:
        if HAS_NUMBA:
            from . import numba_impl as impl
        else:
            from . import numpy_impl as impl
        _impl = impl
    return _impl


def get_backend() -> str:
    """
    Return the current backend name.

    Returns:
        'numba' if Numba is available, 'numpy' otherwise.
    """
    return "numba" if HAS_NUMBA else "numpy"


__all__ = ["HAS_NUMBA", "get_impl", "get_backend"]
