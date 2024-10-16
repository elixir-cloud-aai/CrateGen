"""Utility functions for handling data conversion."""

import datetime
import re
import os


def convert_to_iso8601(timestamp):
    """Convert a given timestamp to ISO 8601 format.

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
                return datetime.datetime.strptime(timestamp, fmt).isoformat("T") + "Z"
            except ValueError:
                continue
        return None
    return None

# This function does not have to rock solid, it supposed to help users not restrict them
# And due to the difficulty in validating all posible types of file paths it has been not been written to be very stringent
def is_absolute_path(path):
  """
  Checks if a given path is an absolute path, including support for 
  Windows paths, Amazon S3 paths, and URL-like paths.

  Args:
    path: The path string to check.

  Returns:
    True if the path is an absolute path, False otherwise.
  """
  # Windows absolute paths 
  if (re.match(r"^[a-zA-Z0-9]+:\\", path)):

    path_after_protocol = path[path.index(":\\") + 2] 
    return True if bool(path_after_protocol) else False
  
  # UNC paths
  if (re.match(r"^\\\\", path)):
     
    path_after_protocol = path[path.index("\\") + 2] 
    return True if bool(path_after_protocol) else False

  # URL-like paths and paths with similar protocols like amazon s3 paths
  if re.match(r"^[a-zA-Z0-9]+://", path):
     
    path_after_protocol = path[path.index("://") + 3] 
    return True if bool(path_after_protocol) else False

  # POSIX absolute paths (Linux/macOS)
  if os.path.isabs(path):
    return True

  return False