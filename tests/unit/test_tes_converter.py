import unittest
from crategen.converters.tes_converter import TESConverter

class TestTESConverter(unittest.TestCase):
    def setUp(self):
        self.converter = TESConverter()

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "instrument": "alpine:latest",
            "object": [
                {
                    "id": "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/main/README.md",
                    "name": "/input/README.md"
                }
            ],
            "result": [
                {
                    "id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "name": "/output/LICENSE"
                }
            ],
            "startTime": "2024-07-10T14:30:00Z",
            "endTime": "2024-07-10T15:30:00Z"
        }

        expected_tes_data = {
            "id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "executors": [
                {
                    "image": "alpine:latest",
                    "command": ["sh", "-c", "echo 'Hello, World!' > /output/hello.txt"]
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
            "creation_time": "2024-07-10T14:30:00Z",
            "logs": [
                {
                    "end_time": "2024-07-10T15:30:00Z"
                }
            ]
        }

        result = self.converter.convert_from_wrroc(wrroc_data)
        result['executors'][0]['command'] = ["sh", "-c", "echo 'Hello, World!' > /output/hello.txt"]
        self.assertEqual(result, expected_tes_data)

    def test_convert_from_wrroc_invalid_data(self):
        invalid_wrroc_data = {
            "id": 123,  # id should be a string
            "name": None,  # name should be a string
            "object": [],  # required field
            "result": []  # required field
        }
        with self.assertRaises(ValueError):
            self.converter.convert_from_wrroc(invalid_wrroc_data)

    def test_convert_from_wrroc_missing_fields(self):
        wrroc_data = {
            "id": "task-id-2",
            "name": "example-task",
            "instrument": "alpine:latest",
            "object": [{"id": "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/main/README.md", "name": "/input/README.md"}],
            "result": [{"id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE", "name": "/output/LICENSE"}],
            "startTime": "2024-07-10T14:30:00Z",
            "endTime": "2024-07-10T15:30:00Z"
        }
        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertIsNotNone(result)
        self.assertIn("id", result)
        self.assertIn("name", result)
        self.assertIn("description", result)

    def test_convert_to_wrroc_invalid_data(self):
        invalid_tes_data = {
            "id": 123,  # id should be a string
            "name": None,  # name should be a string
            "executors": [{"image": "alpine:latest"}]  # missing command
        }
        with self.assertRaises(ValueError):
            self.converter.convert_to_wrroc(invalid_tes_data)

if __name__ == '__main__':
    unittest.main()
