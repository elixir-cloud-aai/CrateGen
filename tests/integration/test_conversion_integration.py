import unittest
from crategen.converter_manager import ConverterManager

class TestConversionIntegration(unittest.TestCase):

    def setUp(self):
        self.manager = ConverterManager()

    def test_tes_to_wrroc_integration(self):
        tes_data = {}  # Add sample TES data here
        result = self.manager.convert_tes_to_wrroc(tes_data)
        # Add assertions here

    def test_wes_to_wrroc_integration(self):
        wes_data = {}  # Add sample WES data here
        result = self.manager.convert_wes_to_wrroc(wes_data)
        # Add assertions here

if __name__ == '__main__':
    unittest.main()
