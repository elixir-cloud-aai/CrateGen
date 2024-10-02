import datetime
from typing import Optional

def convert_to_iso8601(timestamp: Optional[str]) -> Optional[str]:
    """
    Convert a given timestamp to ISO 8601 format.
    Handles multiple formats including RFC 3339, ISO 8601 with and without fractional seconds.

    Args:
        timestamp (Optional[str]): The timestamp to be converted.

    Returns:
        Optional[str]: The converted timestamp in ISO 8601 format, or None if the input format is incorrect.
    """
    if timestamp:
        # List of supported formats
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",    # RFC 3339 with fractional seconds
            "%Y-%m-%dT%H:%M:%SZ",       # RFC 3339 without fractional seconds
            "%Y-%m-%dT%H:%M:%S%z",      # ISO 8601 with timezone
            "%Y-%m-%dT%H:%M:%S.%f%z",   # ISO 8601 with fractional seconds and timezone
        ]
        for fmt in formats:
            try:
                return datetime.datetime.strptime(timestamp, fmt).isoformat() + "Z"
            except ValueError:
                continue
        return None
    return None
