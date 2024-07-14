import unittest
from crategen.converters.wes_converter import WESConverter

class TestWESConverter(unittest.TestCase):

    def setUp(self):
        self.converter = WESConverter()

    def test_convert_to_wrroc(self):
        wes_data = {
            "run_id": "run-id",
            "run_log": {
                "name": "test-run",
                "start_time": "2023-07-10T14:30:00Z",
                "end_time": "2023-07-10T15:30:00Z"
            },
            "state": "COMPLETED",
            "outputs": [{"location": "output-location", "name": "output-name"}]
        }
    
        expected_wrroc_data = {
            "@id": "run-id",
            "name": "test-run",
            "status": "COMPLETED",
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z",
            "result": [{"@id": "output-location", "name": "output-name"}]
        }
    
        result = self.converter.convert_to_wrroc(wes_data)
        self.assertEqual(result, expected_wrroc_data)

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "@id": "run-id",
            "name": "test-run",
            "status": "COMPLETED",
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z",
            "result": [{"@id": "output-location", "name": "output-name"}]
        }

        expected_wes_data = {
            "run_id": "run-id",
            "run_log": {
                "name": "test-run",
                "start_time": "2023-07-10T14:30:00Z",
                "end_time": "2023-07-10T15:30:00Z"
            },
            "state": "COMPLETED",
            "outputs": [{"location": "output-location", "name": "output-name"}]
        }

        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result, expected_wes_data)

if __name__ == '__main__':
    unittest.main()
