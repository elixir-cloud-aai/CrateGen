from .converters.tes_converter import TESConverter
from .converters.wes_converter import WESConverter

class ConverterManager:
    def __init__(self):
        self.tes_converter = TESConverter()
        self.wes_converter = WESConverter()

    def convert_tes_to_wrroc(self, tes_data):
        return self.tes_converter.convert_to_wrroc(tes_data)

    def convert_wes_to_wrroc(self, wes_data):
        return self.wes_converter.convert_to_wrroc(wes_data)

    def convert_wrroc_to_tes(self, wrroc_data):
        return self.tes_converter.convert_from_wrroc(wrroc_data)

    def convert_wrroc_to_wes(self, wrroc_data):
        return self.wes_converter.convert_from_wrroc(wrroc_data)
