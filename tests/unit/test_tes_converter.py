import unittest
from crategen.converters.tes_converter import TESConverter

class TestTESConverter(unittest.TestCase):

    def setUp(self):
        self.converter = TESConverter()

    def test_convert_to_wrroc(self):
        tes_data = {
            "id": "task-id-1",
            "name": "example-task-1",
            "description": "Example task description 1",
            "executors": [{"image": "executor-image-1"}],
            "inputs": [
                {"url": "input-url-1", "path": "input-path-1"},
                {"url": "input-url-2", "path": "input-path-2"}
            ],
            "outputs": [
                {"url": "output-url-1", "path": "output-path-1"}
            ],
            "creation_time": "2023-07-10T14:30:00Z",
            "logs": [{"end_time": "2023-07-10T15:30:00Z"}]
        }

        expected_wrroc_data = {
            "@id": "task-id-1",
            "name": "example-task-1",
            "description": "Example task description 1",
            "instrument": "executor-image-1",
            "object": [
                {"@id": "input-url-1", "name": "input-path-1"},
                {"@id": "input-url-2", "name": "input-path-2"}
            ],
            "result": [
                {"@id": "output-url-1", "name": "output-path-1"}
            ],
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z"
        }

        result = self.converter.convert_to_wrroc(tes_data)
        self.assertEqual(result, expected_wrroc_data)

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "@id": "task-id-1",
            "name": "example-task-1",
            "description": "Example task description 1",
            "instrument": "executor-image-1",
            "object": [
                {"@id": "input-url-1", "name": "input-path-1"},
                {"@id": "input-url-2", "name": "input-path-2"}
            ],
            "result": [
                {"@id": "output-url-1", "name": "output-path-1"}
            ],
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z"
        }

        expected_tes_data = {
            "id": "task-id-1",
            "name": "example-task-1",
            "description": "Example task description 1",
            "executors": [{"image": "executor-image-1"}],
            "inputs": [
                {"url": "input-url-1", "path": "input-path-1"},
                {"url": "input-url-2", "path": "input-path-2"}
            ],
            "outputs": [
                {"url": "output-url-1", "path": "output-path-1"}
            ],
            "creation_time": "2023-07-10T14:30:00Z",
            "logs": [{"end_time": "2023-07-10T15:30:00Z"}]
        }

        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result, expected_tes_data)

    def test_convert_to_wrroc_missing_fields(self):
        tes_data = {
            "id": "task-id-2",
            "name": "example-task-2"
        }

        expected_wrroc_data = {
            "@id": "task-id-2",
            "name": "example-task-2",
            "description": "",
            "instrument": None,
            "object": [],
            "result": [],
            "startTime": None,
            "endTime": None
        }

        result = self.converter.convert_to_wrroc(tes_data)
        self.assertEqual(result, expected_wrroc_data)

    def test_convert_from_wrroc_missing_fields(self):
        wrroc_data = {
            "@id": "task-id-2",
            "name": "example-task-2"
        }

        expected_tes_data = {
            "id": "task-id-2",
            "name": "example-task-2",
            "description": "",
            "executors": [{"image": ""}],
            "inputs": [],
            "outputs": [],
            "creation_time": "",
            "logs": [{"end_time": ""}]
        }

        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result, expected_tes_data)

if __name__ == '__main__':
    unittest.main()
