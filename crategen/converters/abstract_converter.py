"""Abstract base class for converters between TES/WES and WRROC formats."""

from abc import ABC, abstractmethod


class AbstractConverter(ABC):
    """Abstract converter for TES/WES to WRROC and vice versa."""

    @abstractmethod
    def convert_to_wrroc(self, data):
        """
        Convert data to WRROC format.

        Args:
            data: The data to be converted.

        Returns:
            The data converted to WRROC format.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """

    @abstractmethod
    def convert_from_wrroc(self, wrroc_data):
        """
        Convert WRROC data to the original format.

        Args:
            wrroc_data: The WRROC data to be converted.

        Returns:
            The data converted back to the original format.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
