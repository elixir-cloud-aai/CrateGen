import unittest
from crategen.converters.wes_converter import WESConverter

class TestWESConverter(unittest.TestCase):
    def setUp(self):
        self.converter = WESConverter()

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "id": "run-id",
            "name": "test-run",
            "startTime": "2024-07-10T14:30:00Z",
            "endTime": "2024-07-10T15:30:00Z",
            "status": "COMPLETED",
            "result": [{"id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "name": "LICENSE"}]
        }

        expected_wes_data = {
            "run_id": "run-id",
            "run_log": {
                "name": "test-run",
                "start_time": "2024-07-10T14:30:00Z",
                "end_time": "2024-07-10T15:30:00Z"
            },
            "state": "COMPLETED",
            "outputs": [{"location": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "name": "LICENSE"}]
        }

        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result, expected_wes_data)

    def test_convert_from_wrroc_invalid_data(self):
        invalid_wrroc_data = {
            "id": 123,  # id should be a string
            "name": None,  # name should be a string
            "status": "COMPLETED",
            "result": []
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_from_wrroc(invalid_wrroc_data)
        self.assertIn("Invalid WRROC data", str(context.exception))

    def test_convert_from_wrroc_invalid_nested_structure(self):
        wrroc_data = {
            "id": "run-id-4",
            "name": "nested-run",
            "startTime": "2024-07-10T14:30:00Z",
            "endTime": "2024-07-10T15:30:00Z",
            "status": "COMPLETED",
            "result": [
                {
                    "id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "name": "LICENSE"
                }
            ],
            "nested": {
                "unexpected_field": "unexpected_value"
            }
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_from_wrroc(wrroc_data)
        self.assertIn("extra fields not permitted", str(context.exception))

    def test_convert_from_wrroc_missing_fields(self):
        wrroc_data = {
            "id": "run-id-2",
            "status": "COMPLETED",
            "result": []
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_from_wrroc(wrroc_data)
        self.assertIn("Invalid WRROC data", str(context.exception))

    def test_convert_to_wrroc_invalid_data(self):
        invalid_wes_data = {
            "run_id": 123,  # run_id should be a string
            "run_log": None,  # run_log should be a dictionary
            "state": "COMPLETED",
            "outputs": []
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_to_wrroc(invalid_wes_data)
        self.assertIn("Invalid WES data", str(context.exception))

    def test_convert_to_wrroc_missing_fields(self):
        wes_data = {
            "run_id": "run-id-2",
            "state": "COMPLETED"
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_to_wrroc(wes_data)
        self.assertIn("Invalid WES data", str(context.exception))

if __name__ == "__main__":
    unittest.main()
