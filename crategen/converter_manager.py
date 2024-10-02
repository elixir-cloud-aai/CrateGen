"""Manager for handling TES and WES to WRROC conversions."""

from typing import Any, Dict

from .converters.tes_converter import TESConverter
from .converters.wes_converter import WESConverter


class ConverterManager:
    """Manages conversion between TES/WES and WRROC formats."""

    def __init__(self) -> None:
        """Initializes the converters for TES and WES."""
        self.tes_converter = TESConverter()
        self.wes_converter = WESConverter()

    def convert_tes_to_wrroc(self, tes_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts TES data to WRROC format."""
        return self.tes_converter.convert_to_wrroc(tes_data)

    def convert_wes_to_wrroc(self, wes_data: Dict[str, Any]) -> Dict[str, Any]:
        """Converts WES data to WRROC format."""
        return self.wes_converter.convert_to_wrroc(wes_data)
