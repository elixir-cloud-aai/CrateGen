import unittest
from crategen.converters.wes_converter import WESConverter

class TestWESConverter(unittest.TestCase):

    def setUp(self):
        self.converter = WESConverter()

    def test_convert_to_wrroc(self):
        wes_data = {
            "run_id": "run-id-1",
            "run_log": {
                "name": "example-run-1",
                "start_time": "2023-07-10T14:30:00Z",
                "end_time": "2023-07-10T15:30:00Z"
            },
            "state": "COMPLETED",
            "outputs": [{"location": "output-location-1", "name": "output-name-1"}]
        }

        expected_wrroc_data = {
            "@id": "run-id-1",
            "name": "example-run-1",
            "status": "COMPLETED",
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z",
            "result": [{"@id": "output-location-1", "name": "output-name-1"}]
        }

        result = self.converter.convert_to_wrroc(wes_data)
        self.assertEqual(result, expected_wrroc_data)

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "@id": "run-id-1",
            "name": "example-run-1",
            "status": "COMPLETED",
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z",
            "result": [{"@id": "output-location-1", "name": "output-name-1"}]
        }

        expected_wes_data = {
            "run_id": "run-id-1",
            "run_log": {
                "name": "example-run-1",
                "start_time": "2023-07-10T14:30:00Z",
                "end_time": "2023-07-10T15:30:00Z"
            },
            "state": "COMPLETED",
            "outputs": [{"location": "output-location-1", "name": "output-name-1"}]
        }

        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result, expected_wes_data)

    def test_convert_to_wrroc_missing_fields(self):
        wes_data = {
            "run_id": "run-id-2",
            "run_log": {
                "name": "example-run-2"
            }
        }

        expected_wrroc_data = {
            "@id": "run-id-2",
            "name": "example-run-2",
            "status": "",
            "startTime": None,
            "endTime": None,
            "result": []
        }

        result = self.converter.convert_to_wrroc(wes_data)
        self.assertEqual(result, expected_wrroc_data)

    def test_convert_from_wrroc_missing_fields(self):
        wrroc_data = {
            "@id": "run-id-2",
            "name": "example-run-2"
        }

        expected_wes_data = {
            "run_id": "run-id-2",
            "run_log": {
                "name": "example-run-2",
                "start_time": "",
                "end_time": ""
            },
            "state": "",
            "outputs": []
        }

        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result, expected_wes_data)

if __name__ == '__main__':
    unittest.main()
