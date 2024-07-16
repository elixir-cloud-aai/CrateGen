from .abstract_converter import AbstractConverter
from .utils import convert_to_iso8601

class TESConverter(AbstractConverter):

    def convert_to_wrroc(self, tes_data):
        # Validate and extract data with defaults
        id = tes_data.get("id", "")
        name = tes_data.get("name", "")
        description = tes_data.get("description", "")
        executors = tes_data.get("executors", [{}])
        inputs = tes_data.get("inputs", [])
        outputs = tes_data.get("outputs", [])
        creation_time = tes_data.get("creation_time", "")
        end_time = tes_data.get("logs", [{}])[0].get("end_time", "")  # Corrected to fetch from logs

        # Convert to WRROC
        wrroc_data = {
            "@id": id,
            "name": name,
            "description": description,
            "instrument": executors[0].get("image", None) if executors else None,
            "object": [{"@id": input.get("url", ""), "name": input.get("path", "")} for input in inputs],
            "result": [{"@id": output.get("url", ""), "name": output.get("path", "")} for output in outputs],
            "startTime": convert_to_iso8601(creation_time),
            "endTime": convert_to_iso8601(end_time),
        }
        return wrroc_data

    def convert_from_wrroc(self, wrroc_data):
        # Validate and extract data with defaults
        id = wrroc_data.get("@id", "")
        name = wrroc_data.get("name", "")
        description = wrroc_data.get("description", "")
        instrument = wrroc_data.get("instrument", "")
        object_data = wrroc_data.get("object", [])
        result_data = wrroc_data.get("result", [])
        start_time = wrroc_data.get("startTime", "")
        end_time = wrroc_data.get("endTime", "")

        # Convert from WRROC to TES
        tes_data = {
            "id": id,
            "name": name,
            "description": description,
            "executors": [{"image": instrument}],
            "inputs": [{"url": obj.get("@id", ""), "path": obj.get("name", "")} for obj in object_data],
            "outputs": [{"url": res.get("@id", ""), "path": res.get("name", "")} for res in result_data],
            "creation_time": start_time,
            "logs": [{"end_time": end_time}],  # Added to logs
        }
        return tes_data
