"""
Stock inquiry command - redirects to the inquiry subdirectory module.

This file maintains backward compatibility while the actual implementation
is organized in the inquiry/ subdirectory.
"""

from .inquiry import inquiry

__all__ = ["inquiry"]
