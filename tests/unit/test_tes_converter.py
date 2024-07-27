import unittest
from crategen.converters.tes_converter import TESConverter

class TestTESConverter(unittest.TestCase):

    def setUp(self):
        self.converter = TESConverter()

    def test_convert_to_wrroc(self):
        tes_data = {
            "id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "executors": [{"image": "alpine:latest"}],
            "inputs": [{"url": "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/main/README.md", "path": "/input/README.md"}],
            "outputs": [{"url": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "path": "/output/LICENSE"}],
            "creation_time": "2023-07-10T14:30:00Z",
        }

        expected_wrroc_data = {
            "@id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "instrument": "alpine:latest",
            "object": [{"@id": "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/main/README.md", "name": "/input/README.md"}],
            "result": [{"@id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "name": "/output/LICENSE"}],
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": None
        }

        result = self.converter.convert_to_wrroc(tes_data)
        self.assertEqual(result, expected_wrroc_data)

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "@id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "instrument": "alpine:latest",
            "object": [
                {
                    "@id": "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/main/README.md",
                    "name": "/input/README.md"
                }
            ],
            "result": [
                {
                    "@id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "name": "/output/LICENSE"
                }
            ],
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z"
        }

        expected_tes_data = {
            "id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "executors": [
                {
                    "image": "alpine:latest",
                }
            ],
            "inputs": [
                {
                    "url": "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/main/README.md",
                    "path": "/input/README.md"
                }
            ],
            "outputs": [
                {
                    "url": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "path": "/output/LICENSE"
                }
            ],
            "creation_time": "2023-07-10T14:30:00Z",
            "logs": [
                {
                    "end_time": "2023-07-10T15:30:00Z"
                }
            ]
        }

        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result, expected_tes_data)

    def test_convert_to_wrroc_invalid_data(self):
        invalid_tes_data = {
            "id": 123,  # id should be a string
            "name": None,  # name should be a string
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_to_wrroc(invalid_tes_data)
        self.assertIn("Invalid id type", str(context.exception))

    def test_convert_from_wrroc_invalid_data(self):
        invalid_wrroc_data = {
            "@id": 123,  # @id should be a string
            "name": None,  # name should be a string
        }
        with self.assertRaises(ValueError) as context:
            self.converter.convert_from_wrroc(invalid_wrroc_data)
        self.assertIn("Invalid @id type", str(context.exception))

    def test_convert_to_wrroc_missing_fields(self):
        tes_data = {
            "id": "task-id-2",
            "name": "example-task"
        }
        result = self.converter.convert_to_wrroc(tes_data)
        self.assertIsNotNone(result)
        self.assertIn("@id", result)
        self.assertIn("name", result)
        self.assertIn("description", result)
        self.assertIn("instrument", result)
        self.assertIn("object", result)
        self.assertIn("result", result)
        self.assertIn("startTime", result)
        self.assertIn("endTime", result)

    def test_convert_from_wrroc_missing_fields(self):
        wrroc_data = {
            "@id": "task-id-2",
            "name": "example-task"
        }
        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertIsNotNone(result)
        self.assertIn("id", result)
        self.assertIn("name", result)
        self.assertIn("description", result)
        self.assertIn("executors", result)
        self.assertIn("inputs", result)
        self.assertIn("outputs", result)
        self.assertIn("creation_time", result)
        self.assertIn("logs", result)

if __name__ == "__main__":
    unittest.main()
