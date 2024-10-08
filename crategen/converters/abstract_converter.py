"""Abstract base class for converters between TES/WES and WRROC formats."""

from abc import ABC, abstractmethod


class AbstractConverter(ABC):
    """Abstract converter for TES/WES to WRROC and vice versa."""

    @abstractmethod
    def convert_to_wrroc(self, data):
        """Convert data to WRROC format."""

    @abstractmethod
    def convert_from_wrroc(self, wrroc_data):
        """Convert WRROC data to the original format."""
