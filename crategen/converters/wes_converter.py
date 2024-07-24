from .abstract_converter import AbstractConverter
from .utils import convert_to_iso8601

class WESConverter(AbstractConverter):

    def convert_to_wrroc(self, wes_data):
        # Validate and extract data with defaults
        run_id = wes_data.get("run_id", "")
        name = wes_data.get("run_log", {}).get("name", "")
        state = wes_data.get("state", "")
        start_time = wes_data.get("run_log", {}).get("start_time", "")
        end_time = wes_data.get("run_log", {}).get("end_time", "")
        outputs = wes_data.get("outputs", {})

        # Convert to WRROC
        wrroc_data = {
            "@id": run_id,
            "name": name,
            "status": state,
            "startTime": convert_to_iso8601(start_time),
            "endTime": convert_to_iso8601(end_time),
            "result": [{"@id": output.get("location", ""), "name": output.get("name", "")} for output in outputs],
        }
        return wrroc_data

    def convert_from_wrroc(self, wrroc_data):
        # Validate and extract data with defaults
        run_id = wrroc_data.get("@id", "")
        name = wrroc_data.get("name", "")
        start_time = wrroc_data.get("startTime", "")
        end_time = wrroc_data.get("endTime", "")
        state = wrroc_data.get("status", "")
        result_data = wrroc_data.get("result", [])
        
        # Convert from WRROC to WES
        wes_data = {
            "run_id": run_id,
            "run_log": {
                "name": name,
                "start_time": start_time,
                "end_time": end_time,
            },
            "state": state,
            "outputs": [{"location": res.get("@id", ""), "name": res.get("name", "")} for res in result_data],
        }
        return wes_data
