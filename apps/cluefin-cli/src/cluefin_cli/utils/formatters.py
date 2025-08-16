"""Formatting utilities for numbers and currency."""

from typing import Union


def format_number(value: Union[str, int, float]) -> str:
    """
    Format a number with commas for thousands separators.

    Args:
        value: Number to format (can be string, int, or float)

    Returns:
        Formatted string with comma separators

    Examples:
        >>> format_number(1000)
        '1,000'
        >>> format_number("1000000")
        '1,000,000'
        >>> format_number(1234.56)
        '1,234.56'
    """
    try:
        # Convert string to number if needed
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return "0"
            # Remove existing commas if present
            value = value.replace(",", "")
            # Check if it's a float or int
            if "." in value:
                num = float(value)
            else:
                num = int(value)
        else:
            num = value

        # Format with commas
        if isinstance(num, float):
            # Keep decimal places
            return f"{num:,.2f}" if num % 1 != 0 else f"{int(num):,}"
        else:
            return f"{num:,}"
    except (ValueError, TypeError):
        # Return original value if it can't be formatted
        return str(value)


def format_currency(value: Union[str, int, float], unit: str = "") -> str:
    """
    Format a number as Korean currency with commas.

    Args:
        value: Number to format
        unit: Optional unit to append (e.g., '천원', '백만원')

    Returns:
        Formatted currency string with ₩ symbol

    Examples:
        >>> format_currency(1000000)
        '₩1,000,000'
        >>> format_currency(1000000, "천원")
        '₩1,000,000천원'
    """
    formatted = format_number(value)
    if formatted == str(value):
        # If formatting failed, just add the symbol
        return f"₩ {value}{unit}"
    return f"₩ {formatted}{unit}"
