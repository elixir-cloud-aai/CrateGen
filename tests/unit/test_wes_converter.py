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
                "start_time": "2024-07-10T14:30:00Z",
                "end_time": "2024-07-10T15:30:00Z"
            },
            "state": "COMPLETED",
            "outputs": [{"location": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "name": "LICENSE"}]
        }

        expected_wrroc_data = {
            "@id": "run-id",
            "name": "test-run",
            "status": "COMPLETED",
            "startTime": "2024-07-10T14:30:00Z",
            "endTime": "2024-07-10T15:30:00Z",
            "result": [{"@id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "name": "LICENSE"}]
        }

        result = self.converter.convert_to_wrroc(wes_data)
        self.assertEqual(result, expected_wrroc_data)

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "@id": "run-id",
            "name": "test-run",
            "startTime": "2024-07-10T14:30:00Z",
            "endTime": "2024-07-10T15:30:00Z",
            "status": "COMPLETED",
            "result": [{"@id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "name": "LICENSE"}]
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

    def test_convert_to_wrroc_invalid_data(self):
        invalid_wes_data = {
            "run_id": 123,  # run_id should be a string
            "run_log": None,  # run_log should be a dictionary
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_to_wrroc(invalid_wes_data)
        self.assertIn("Invalid run_id type", str(context.exception))

    def test_convert_from_wrroc_invalid_data(self):
        invalid_wrroc_data = {
            "@id": 123,  # @id should be a string
            "name": None,  # name should be a string
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_from_wrroc(invalid_wrroc_data)
        self.assertIn("Invalid @id type", str(context.exception))

    def test_convert_to_wrroc_missing_fields(self):
        wes_data = {
            "run_id": "run-id-2",
            "state": "COMPLETED"
        }
        result = self.converter.convert_to_wrroc(wes_data)
        self.assertIsNotNone(result)
        self.assertIn("@id", result)
        self.assertIn("status", result)
        self.assertNotIn("name", result)
        self.assertNotIn("startTime", result)
        self.assertNotIn("endTime", result)

    def test_convert_from_wrroc_missing_fields(self):
        wrroc_data = {
            "@id": "run-id-2",
            "status": "COMPLETED"
        }
        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertIsNotNone(result)
        self.assertIn("run_id", result)
        self.assertIn("state", result)
        self.assertNotIn("name", result)
        self.assertNotIn("run_log", result)

    def test_convert_from_wrroc_invalid_nested_structure(self):
        wrroc_data = {
            "@id": "run-id-4",
            "name": "nested-run",
            "startTime": "2024-07-10T14:30:00Z",
            "endTime": "2024-07-10T15:30:00Z",
            "status": "COMPLETED",
            "result": [
                {
                    "@id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "name": "LICENSE"
                }
            ],
            "nested": {
                "unexpected_field": "unexpected_value"
            }
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_from_wrroc(wrroc_data)
        self.assertIn("Invalid nested structure", str(context.exception))

    def test_convert_to_wrroc_with_nested_structures(self):
        wes_data = {
            "run_id": "run-id-1",
            "run_log": {
                "name": "test-run",
                "start_time": "2024-07-10T14:30:00Z",
                "end_time": "2024-07-10T15:30:00Z",
                "nested": {
                    "unexpected_field": "unexpected_value"
                }
            },
            "state": "COMPLETED",
            "outputs": [{"location": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "name": "LICENSE"}]
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_to_wrroc(wes_data)
        self.assertIn("Invalid nested structure", str(context.exception))

if __name__ == "__main__":
    unittest.main()
