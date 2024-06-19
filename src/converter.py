import datetime
import json

def convert_tes_to_wrroc(tes_data):
    try:
        if not tes_data or not isinstance(tes_data, dict):
            raise ValueError("Invalid TES data provided")

        if not tes_data.get("executors"):
            raise ValueError("TES data missing 'executors' list or 'executors' list is empty")

        wrroc = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "Dataset",
                    "conformsTo": "https://w3id.org/ro/wfrun/process/0.4"
                },
                {
                    "@type": "CreateAction",
                    "@id": tes_data.get("id"),
                    "name": tes_data.get("name", ""),
                    "description": tes_data.get("description", ""),
                    "instrument": tes_data["executors"][0].get("image"),
                    "object": [{"@id": input.get("url"), "name": input.get("path")} for input in tes_data.get("inputs", []) if input.get("url") and input.get("path")],
                    "result": [{"@id": output.get("url"), "name": output.get("path")} for output in tes_data.get("outputs", []) if output.get("url") and output.get("path")],
                    "startTime": convert_to_iso8601(tes_data["logs"][0].get("start_time")),
                    "endTime": convert_to_iso8601(tes_data["logs"][0].get("end_time")),
                    "actionStatus": convert_status(tes_data.get("state")),
                },
                {
                    "@type": "SoftwareApplication",
                    "@id": tes_data["executors"][0].get("image"),
                    "name": tes_data.get("name", "")
                }
            ]
        }

        return json.dumps(wrroc, indent=2)
    except KeyError as e:
        raise ValueError(f"Missing expected key: {e}")
    except IndexError as e:
        raise ValueError(f"Missing expected index: {e}")
    except Exception as e:
        raise ValueError(f"An error occurred during TES to WRROC conversion: {e}")

def convert_wes_to_wrroc(wes_data):
    try:
        if not wes_data or not isinstance(wes_data, dict):
            raise ValueError("Invalid WES data provided")

        if not wes_data.get("run_log") or not wes_data["run_log"].get("outputs"):
            raise ValueError("WES data missing 'run_log' or 'outputs'")

        wrroc = {
            "@context": "https://w3id.org/ro/crate/1.1/context",
            "@graph": [
                {
                    "@type": "Dataset",
                    "conformsTo": "https://w3id.org/ro/wfrun/workflow/0.4"
                },
                {
                    "@type": "CreateAction",
                    "@id": wes_data.get("run_id"),
                    "name": wes_data["run_log"].get("name", ""),
                    "description": wes_data["run_log"].get("description", ""),
                    "object": [{"@id": input.get("location"), "name": input.get("name")} for input in wes_data["request"].get("workflow_params", []) if input.get("location") and input.get("name")],
                    "result": [{"@id": output.get("location"), "name": output.get("name")} for output in wes_data["run_log"].get("outputs", []) if output.get("location") and output.get("name")],
                    "startTime": convert_to_iso8601(wes_data["run_log"].get("start_time")),
                    "endTime": convert_to_iso8601(wes_data["run_log"].get("end_time")),
                    "actionStatus": convert_status(wes_data["run_log"].get("state")),
                },
                {
                    "@type": "SoftwareApplication",
                    "@id": wes_data["request"].get("workflow_url"),
                    "name": wes_data["request"].get("workflow_name", "")
                }
            ]
        }

        return json.dumps(wrroc, indent=2)
    except KeyError as e:
        raise ValueError(f"Missing expected key: {e}")
    except IndexError as e:
        raise ValueError(f"Missing expected index: {e}")
    except Exception as e:
        raise ValueError(f"An error occurred during WES to WRROC conversion: {e}")

def convert_to_iso8601(timestamp):
    try:
        if not timestamp:
            raise ValueError("Timestamp is missing")
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").isoformat() + "Z"
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {timestamp}. Error: {e}")

def convert_status(status):
    try:
        status_mapping = {
            "COMPLETE": "schema:CompletedActionStatus",
            "EXECUTOR_ERROR": "schema:FailedActionStatus",
            "SYSTEM_ERROR": "schema:FailedActionStatus",
            "CANCELED": "schema:CanceledActionStatus",
            "RUNNING": "schema:ActiveActionStatus",
            "QUEUED": "schema:PotentialActionStatus",
            "INITIALIZING": "schema:PotentialActionStatus",
            "PAUSED": "schema:PotentialActionStatus"
        }
        return status_mapping.get(status, "schema:PotentialActionStatus")
    except KeyError:
        raise ValueError(f"Invalid status value: {status}")

# Example usage
if __name__ == "__main__":
    tes_task_example = {
        "id": "task123",
        "name": "Example Task",
        "description": "This is an example task",
        "state": "COMPLETE",
        "executors": [
            {
                "image": "example/image:1.0"
            }
        ],
        "inputs": [
            {
                "url": "http://example.com/input1",
                "path": "/data/input1"
            }
        ],
        "outputs": [
            {
                "url": "http://example.com/output1",
                "path": "/data/output1"
            }
        ],
        "logs": [
            {
                "start_time": "2022-01-01T00:00:00Z",
                "end_time": "2022-01-01T01:00:00Z"
            }
        ]
    }

    wes_run_example = {
        "run_id": "run123",
        "request": {
            "workflow_url": "http://example.com/workflow",
            "workflow_name": "Example Workflow",
            "workflow_params": [
                {
                    "location": "http://example.com/input1",
                    "name": "input1"
                }
            ]
        },
        "run_log": {
            "name": "Example Run",
            "description": "This is an example workflow run",
            "state": "COMPLETE",
            "outputs": [
                {
                    "location": "http://example.com/output1",
                    "name": "output1"
                }
            ],
            "start_time": "2022-01-01T00:00:00Z",
            "end_time": "2022-01-01T01:00:00Z"
        }
    }

    print(convert_tes_to_wrroc(tes_task_example))
    print(convert_wes_to_wrroc(wes_run_example))
