from .abstract_converter import AbstractConverter
from .utils import convert_to_iso8601

class WESConverter(AbstractConverter):

    def convert_to_wrroc(self, wes_data):
        if "run_id" in wes_data and not isinstance(wes_data["run_id"], str):
            raise ValueError("Invalid run_id type")
        if "run_log" in wes_data and not isinstance(wes_data["run_log"], dict):
            raise ValueError("Invalid run_log type")
        if "run_log" in wes_data and "nested" in wes_data["run_log"]:
            raise ValueError("Invalid nested structure in run_log")

        wrroc_data = {
            "@id": wes_data.get("run_id", ""),
            "status": wes_data.get("state", ""),
            "result": [{"@id": output.get("location", ""), "name": output.get("name", "")} for output in wes_data.get("outputs", [])],
        }

        start_time = convert_to_iso8601(wes_data.get("run_log", {}).get("start_time"))
        end_time = convert_to_iso8601(wes_data.get("run_log", {}).get("end_time"))

        if start_time:
            wrroc_data["startTime"] = start_time
        if end_time:
            wrroc_data["endTime"] = end_time

        if "run_log" in wes_data and "name" in wes_data["run_log"] and wes_data["run_log"]["name"]:
            wrroc_data["name"] = wes_data["run_log"]["name"]

        return wrroc_data

    def convert_from_wrroc(self, wrroc_data):
        if "@id" in wrroc_data and not isinstance(wrroc_data["@id"], str):
            raise ValueError("Invalid @id type")
        if "name" in wrroc_data and not isinstance(wrroc_data["name"], str):
            raise ValueError("Invalid name type")
        if "nested" in wrroc_data:
            raise ValueError("Invalid nested structure")

        wes_data = {
            "run_id": wrroc_data.get("@id", ""),
            "state": wrroc_data.get("status", ""),
            "outputs": [{"location": res.get("@id", ""), "name": res.get("name", "")} for res in wrroc_data.get("result", [])],
            "run_log": {
                "start_time": wrroc_data.get("startTime", ""),
                "end_time": wrroc_data.get("endTime", ""),
            },
        }

        if "name" in wrroc_data and wrroc_data["name"]:
            wes_data["run_log"]["name"] = wrroc_data["name"]

        if not wes_data["run_log"]["start_time"] and not wes_data["run_log"]["end_time"] and "name" not in wes_data["run_log"]:
            wes_data.pop("run_log")

        return wes_data
