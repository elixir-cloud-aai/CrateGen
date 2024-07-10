import unittest
from crategen.converters.tes_converter import TESConverter

class TestTESConverter(unittest.TestCase):

    def setUp(self):
        self.converter = TESConverter()

    def test_convert_to_wrroc(self):
        tes_data = {
            "id": "tes-12345",
            "name": "example-task",
            "description": "This is a sample TES task.",
            "executors": [
                {
                    "image": "python:3.8",
                    "command": ["python", "script.py"],
                    "workdir": "/workspace",
                    "stdout": "/workspace/output.log",
                    "stderr": "/workspace/error.log"
                }
            ],
            "inputs": [
                {
                    "url": "s3://example-bucket/input-file.txt",
                    "path": "/workspace/input-file.txt",
                    "type": "FILE"
                }
            ],
            "outputs": [
                {
                    "url": "s3://example-bucket/output-file.txt",
                    "path": "/workspace/output-file.txt",
                    "type": "FILE"
                }
            ],
            "creation_time": "2023-07-01T12:00:00Z",
            "end_time": "2023-07-01T12:30:00Z"
        }
        result = self.converter.convert_to_wrroc(tes_data)
        self.assertEqual(result["@id"], "tes-12345")
        self.assertEqual(result["name"], "example-task")
        self.assertEqual(result["description"], "This is a sample TES task.")

    def test_convert_from_wrroc(self):
        wrroc_data = {
            "@id": "tes-12345",
            "name": "example-task",
            "description": "This is a sample TES task.",
            "instrument": "python:3.8",
            "object": [
                {
                    "@id": "s3://example-bucket/input-file.txt",
                    "name": "/workspace/input-file.txt"
                }
            ],
            "result": [
                {
                    "@id": "s3://example-bucket/output-file.txt",
                    "name": "/workspace/output-file.txt"
                }
            ],
            "startTime": "2023-07-01T12:00:00Z",
            "endTime": "2023-07-01T12:30:00Z"
        }
        result = self.converter.convert_from_wrroc(wrroc_data)
        self.assertEqual(result["id"], "tes-12345")
        self.assertEqual(result["name"], "example-task")
        self.assertEqual(result["description"], "This is a sample TES task.")

if __name__ == '__main__':
    unittest.main()
