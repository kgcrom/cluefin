"""
Stock inquiry command module for Korean financial markets.

This module provides interactive CLI commands for exploring Korean financial markets
through various ranking systems, sector analysis, and detailed stock information
using Kiwoom Securities APIs.
"""

from .main import inquiry

__all__ = ["inquiry"]