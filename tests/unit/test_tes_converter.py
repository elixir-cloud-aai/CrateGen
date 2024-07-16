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
            "executors": [{"image": "executor-image"}],
            "inputs": [{"url": "input-url", "path": "input-path"}],
            "outputs": [{"url": "output-url", "path": "output-path"}],
            "creation_time": "2023-07-10T14:30:00Z",
            "logs": [{"end_time": "2023-07-10T15:30:00Z"}]
        }
    
        expected_wrroc_data = {
            "@id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "instrument": "executor-image",
            "object": [{"@id": "input-url", "name": "input-path"}],
            "result": [{"@id": "output-url", "name": "output-path"}],
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z"
        }
    
        result = self.converter.convert_to_wrroc(tes_data)
        self.assertEqual(result, expected_wrroc_data)

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "@id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "instrument": "executor-image",
            "object": [{"@id": "input-url", "name": "input-path"}],
            "result": [{"@id": "output-url", "name": "output-path"}],
            "startTime": "2023-07-10T14:30:00Z",
            "endTime": "2023-07-10T15:30:00Z"
        }
    
        expected_tes_data = {
            "id": "task-id",
            "name": "test-task",
            "description": "test-description",
            "executors": [{"image": "executor-image"}],
            "inputs": [{"url": "input-url", "path": "input-path"}],
            "outputs": [{"url": "output-url", "path": "output-path"}],
            "creation_time": "2023-07-10T14:30:00Z",
            "logs": [{"end_time": "2023-07-10T15:30:00Z"}]
        }
    
        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result, expected_tes_data)

if __name__ == "__main__":
    unittest.main()
