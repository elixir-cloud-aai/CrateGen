import datetime
import json

def convert_tes_to_wrroc(tes_data):
    wrroc = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {
                "@type": "Dataset",
                "conformsTo": "https://w3id.org/ro/wfrun/process/0.4"
            },
            {
                "@type": "CreateAction",
                "@id": tes_data["id"],
                "name": tes_data.get("name", ""),
                "description": tes_data.get("description", ""),
                "instrument": tes_data["executors"][0]["image"],
                "object": [{"@id": input["url"], "name": input["path"]} for input in tes_data["inputs"]],
                "result": [{"@id": output["url"], "name": output["path"]} for output in tes_data["outputs"]],
                "startTime": convert_to_iso8601(tes_data["logs"][0]["start_time"]),
                "endTime": convert_to_iso8601(tes_data["logs"][0]["end_time"]),
                "actionStatus": convert_status(tes_data["state"]),
            },
            {
                "@type": "SoftwareApplication",
                "@id": tes_data["executors"][0]["image"],
                "name": tes_data.get("name", "")
            }
        ]
    }

    return json.dumps(wrroc, indent=2)


def convert_wes_to_wrroc(wes_data):
    wrroc = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {
                "@type": "Dataset",
                "conformsTo": "https://w3id.org/ro/wfrun/workflow/0.4"
            },
            {
                "@type": "CreateAction",
                "@id": wes_data["run_id"],
                "name": wes_data["run_log"].get("name", ""),
                "description": wes_data["run_log"].get("description", ""),
                "object": [{"@id": input["location"], "name": input["name"]} for input in wes_data["request"]["workflow_params"]],
                "result": [{"@id": output["location"], "name": output["name"]} for output in wes_data["run_log"]["outputs"]],
                "startTime": convert_to_iso8601(wes_data["run_log"]["start_time"]),
                "endTime": convert_to_iso8601(wes_data["run_log"]["end_time"]),
                "actionStatus": convert_status(wes_data["run_log"]["state"]),
            },
            {
                "@type": "SoftwareApplication",
                "@id": wes_data["request"]["workflow_url"],
                "name": wes_data["request"].get("workflow_name", "")
            }
        ]
    }

    return json.dumps(wrroc, indent=2)


def convert_to_iso8601(timestamp):
    # Assuming timestamp is in RFC 3339 format, convert to ISO 8601
    return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").isoformat() + "Z"


def convert_status(wes_status):
    # Convert WES run status to CreateAction actionStatus
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
    return status_mapping.get(wes_status, "schema:PotentialActionStatus")


# Example usage
if __name__ == "__main__":
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
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2024-01-01T01:00:00Z"
        }
    }
    wrroc = convert_wes_to_wrroc(wes_run_example)
    print(wrroc)
