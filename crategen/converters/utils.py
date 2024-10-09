"""Utility functions for handling data conversion."""

import datetime


def convert_to_iso8601(timestamp):
    """
    Convert a given timestamp to ISO 8601 format.

    Handles multiple formats including RFC 3339, ISO 8601 with and without fractional seconds.
    
    Args:
        timestamp (str): The timestamp to be converted.

    Returns:
        str: The converted timestamp in ISO 8601 format, or None if the input format is incorrect.
    """
    if timestamp:
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",    
            "%Y-%m-%dT%H:%M:%SZ",       
            "%Y-%m-%dT%H:%M:%S%z",     
            "%Y-%m-%dT%H:%M:%S.%f%z",
        ]
        for fmt in formats:
            try:
                return datetime.datetime.strptime(timestamp, fmt).isoformat() + "Z"
            except ValueError:
                continue
        return None
    return None
