import unittest
from crategen.converters.wes_converter import WESConverter

class TestWESConverter(unittest.TestCase):

    def setUp(self):
        self.converter = WESConverter()

    def test_convert_to_wrroc(self):
        wes_data = {}  # Add sample WES data here
        result = self.converter.convert_to_wrroc(wes_data)
        # Add assertions here

    def test_convert_from_wrroc(self):
        wrroc_data = {}  # Add sample WRROC data here
        result = self.converter.convert_from_wrroc(wrroc_data)
        # Add assertions here

if __name__ == '__main__':
    unittest.main()
