import unittest
from crategen.converter_manager import ConverterManager

class TestConversionIntegration(unittest.TestCase):

    def setUp(self):
        self.manager = ConverterManager()

    def test_tes_to_wrroc_integration(self):
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
        result = self.manager.convert_tes_to_wrroc(tes_data)
        self.assertEqual(result["@id"], "tes-12345")
        self.assertEqual(result["name"], "example-task")
        self.assertEqual(result["description"], "This is a sample TES task.")

if __name__ == '__main__':
    unittest.main()
