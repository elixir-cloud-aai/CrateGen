"""Manager for handling TES and WES to WRROC conversions."""

from .converters.tes_converter import TESConverter
from .converters.wes_converter import WESConverter


class ConverterManager:
    """Manages conversion between TES/WES and WRROC formats.

    Attributes:
        tes_converter: An instance of TESConverter for TES data conversions.
        wes_converter: An instance of WESConverter for WES data conversions.
    """

    def __init__(self):
        """Initializes the converters for TES and WES."""
        self.tes_converter = TESConverter()
        self.wes_converter = WESConverter()

    def convert_tes_to_wrroc(self, tes_data):
        """Converts TES data to WRROC format.

        Args:
            tes_data: The TES data to be converted.

        Returns:
            The converted data in WRROC format.
        """
        return self.tes_converter.convert_to_wrroc(tes_data)

    def convert_wes_to_wrroc(self, wes_data):
        """Converts WES data to WRROC format.

        Args:
            wes_data: The WES data to be converted.

        Returns:
            The converted data in WRROC format.
        """
        return self.wes_converter.convert_to_wrroc(wes_data)
