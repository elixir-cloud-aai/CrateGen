import unittest
from crategen.converters.tes_converter import TESConverter

class TestTESConverter(unittest.TestCase):

    def setUp(self):
        self.converter = TESConverter()

    def test_convert_to_wrroc(self):
        tes_data = {}  # Add sample TES data here
        result = self.converter.convert_to_wrroc(tes_data)
        # Add assertions here

    def test_convert_from_wrroc(self):
        wrroc_data = {}  # Add sample WRROC data here
        result = self.converter.convert_from_wrroc(wrroc_data)
        # Add assertions here

if __name__ == '__main__':
    unittest.main()
