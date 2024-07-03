from .abstract_converter import AbstractConverter
import datetime

class WESConverter(AbstractConverter):

    def convert_to_wrroc(self, wes_data):
        # Implement the conversion logic from WES to WRROC
        wrroc_data = {
            "@id": wes_data["run_id"],
            "name": wes_data.get("run_log", {}).get("name", ""),
            "status": wes_data["state"],
            "startTime": self.convert_to_iso8601(wes_data.get("run_log", {}).get("start_time")),
            "endTime": self.convert_to_iso8601(wes_data.get("run_log", {}).get("end_time")),
            "result": [{"@id": output.get("location"), "name": output.get("name")} for output in wes_data.get("outputs", [])],
        }
        return wrroc_data

    def convert_from_wrroc(self, wrroc_data):
        # Implement the conversion logic from WRROC to WES
        wes_data = {
            "run_id": wrroc_data["@id"],
            "run_log": {
                "name": wrroc_data.get("name", ""),
                "start_time": wrroc_data.get("startTime"),
                "end_time": wrroc_data.get("endTime"),
            },
            "state": wrroc_data.get("status"),
            "outputs": [{"location": res["@id"], "name": res["name"]} for res in wrroc_data.get("result", [])],
        }
        return wes_data

    def convert_to_iso8601(self, timestamp):
        if timestamp:
            try:
                return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").isoformat() + "Z"
            except ValueError:
                # Handle incorrect format or other issues
                return None
        return None
