import unittest

from pydantic import ValidationError

from crategen.models.wrroc_models import WRROCProcess, WRROCProvenance, WRROCWorkflow
from crategen.validators import validate_wrroc, validate_wrroc_tes, validate_wrroc_wes


class TestWRROCModels(unittest.TestCase):
    """
    Unit tests for the WRROC models to ensure they work as expected.
    """

    def test_wrroc_process_model(self):
        """
        Test that the WRROCProcess model correctly validates data.
        """
        data = {
            "id": "process-id",
            "name": "Test Process",
            "description": "A simple process",
            "startTime": "2024-07-10T14:30:00Z",
            "endTime": "2024-07-10T15:30:00Z",
            "object": [
                {
                    "id": "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/main/README.md",
                    "name": "Input 1",
                }
            ],
        }
        model = WRROCProcess(**data)
        self.assertEqual(model.id, "process-id")
        self.assertEqual(model.name, "Test Process")

    def test_wrroc_process_empty_object_list(self):
        """
        Test that the WRROCProcess model handles empty object lists correctly.
        """
        data = {"id": "process-id", "name": "Test Process", "object": []}
        model = WRROCProcess(**data)
        self.assertEqual(model.object, [])

    def test_wrroc_workflow_model(self):
        """
        Test that the WRROCWorkflow model correctly validates data and includes additional workflow fields.
        """
        data = {
            "id": "workflow-id",
            "name": "Test Workflow",
            "workflowType": "CWL",
            "workflowVersion": "v1.0",
            "result": [
                {
                    "id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "name": "Output 1",
                }
            ],
        }
        model = WRROCWorkflow(**data)
        self.assertEqual(model.workflowType, "CWL")
        self.assertEqual(model.result[0]["name"], "Output 1")

    def test_wrroc_workflow_missing_optional_fields(self):
        """
        Test that the WRROCWorkflow model handles missing optional fields correctly.
        """
        data = {"id": "workflow-id", "name": "Test Workflow"}
        model = WRROCWorkflow(**data)
        self.assertIsNone(model.workflowType)
        self.assertIsNone(model.workflowVersion)

    def test_wrroc_provenance_model(self):
        """
        Test that the WRROCProvenance model correctly validates data and includes additional provenance fields.
        """
        data = {
            "id": "provenance-id",
            "name": "Test Provenance",
            "provenanceData": "Provenance information",
            "agents": [{"id": "agent1", "name": "Agent 1"}],
        }
        model = WRROCProvenance(**data)
        self.assertEqual(model.provenanceData, "Provenance information")
        self.assertEqual(model.agents[0]["name"], "Agent 1")

    def test_wrroc_provenance_empty_agents_list(self):
        """
        Test that the WRROCProvenance model handles empty agents lists correctly.
        """
        data = {"id": "provenance-id", "name": "Test Provenance", "agents": []}
        model = WRROCProvenance(**data)
        self.assertEqual(model.agents, [])

    def test_wrroc_process_invalid_data(self):
        """
        Test that the WRROCProcess model raises a ValidationError with invalid data.
        """
        data = {
            "id": 123,  # id should be a string
            "name": None,  # name should be a string
        }
        with self.assertRaises(ValidationError):
            WRROCProcess(**data)


class TestWRROCValidators(unittest.TestCase):
    """
    Unit tests for the WRROC validators to ensure they work as expected.
    """

    def test_validate_wrroc_process(self):
        """
        Test that validate_wrroc correctly identifies a WRROCProcess entity.
        """
        data = {"id": "process-id", "name": "Test Process"}
        model = validate_wrroc(data)
        self.assertIsInstance(model, WRROCProcess)

    def test_validate_wrroc_workflow(self):
        """
        Test that validate_wrroc correctly identifies a WRROCWorkflow entity.
        """
        data = {
            "id": "workflow-id",
            "name": "Test Workflow",
            "workflowType": "CWL",
            "workflowVersion": "v1.0",
        }
        model = validate_wrroc(data)
        self.assertIsInstance(model, WRROCWorkflow)

    def test_validate_wrroc_provenance(self):
        """
        Test that validate_wrroc correctly identifies a WRROCProvenance entity.
        """
        data = {
            "id": "provenance-id",
            "name": "Test Provenance",
            "provenanceData": "Provenance information",
        }
        model = validate_wrroc(data)
        self.assertIsInstance(model, WRROCProvenance)

    def test_validate_wrroc_invalid(self):
        """
        Test that validate_wrroc raises a ValueError for invalid WRROC data.
        """
        data = {"unknown_field": "unexpected"}
        with self.assertRaises(ValueError):
            validate_wrroc(data)

    def test_validate_wrroc_tes(self):
        """
        Test that validate_wrroc_tes correctly validates a WRROC entity for TES conversion.
        """
        data = {
            "id": "process-id",
            "name": "Test Process",
            "object": [
                {
                    "id": "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/main/README.md",
                    "name": "Input 1",
                }
            ],
            "result": [
                {
                    "id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "name": "Output 1",
                }
            ],
        }
        model = validate_wrroc_tes(data)
        self.assertEqual(model.id, "process-id")
        self.assertEqual(model.name, "Test Process")

    def test_validate_wrroc_tes_empty_object_list(self):
        """
        Test that validate_wrroc_tes correctly validates a WRROC entity with an empty object list for TES conversion.
        """
        data = {
            "id": "process-id",
            "name": "Test Process",
            "object": [],
            "result": [
                {
                    "id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "name": "Output 1",
                }
            ],
        }
        model = validate_wrroc_tes(data)
        self.assertEqual(model.object, [])

    def test_validate_wrroc_tes_missing_fields(self):
        """
        Test that validate_wrroc_tes raises a ValueError if required fields for TES conversion are missing.
        """
        data = {"id": "process-id", "name": "Test Process"}
        with self.assertRaises(ValueError):
            validate_wrroc_tes(data)

    def test_validate_wrroc_wes(self):
        """
        Test that validate_wrroc_wes correctly validates a WRROC entity for WES conversion.
        """
        data = {
            "id": "workflow-id",
            "name": "Test Workflow",
            "workflowType": "CWL",
            "workflowVersion": "v1.0",
            "result": [
                {
                    "id": "https://github.com/elixir-cloud-aai/CrateGen/blob/main/LICENSE",
                    "name": "Output 1",
                }
            ],
        }
        model = validate_wrroc_wes(data)
        self.assertEqual(model.workflowType, "CWL")
        self.assertEqual(model.workflowVersion, "v1.0")

    def test_validate_wrroc_wes_invalid_url(self):
        """
        Test that validate_wrroc_wes raises a ValueError if a result URL is invalid.
        """
        data = {
            "id": "workflow-id",
            "name": "Test Workflow",
            "workflowType": "CWL",
            "workflowVersion": "v1.0",
            "result": [{"id": "invalid_url", "name": "Output 1"}],
        }
        with self.assertRaises(ValueError):
            validate_wrroc_wes(data)

    def test_validate_wrroc_wes_missing_fields(self):
        """
        Test that validate_wrroc_wes raises a ValueError if required fields for WES conversion are missing.
        """
        data = {"id": "workflow-id", "name": "Test Workflow"}
        with self.assertRaises(ValueError):
            validate_wrroc_wes(data)


if __name__ == "__main__":
    unittest.main()
