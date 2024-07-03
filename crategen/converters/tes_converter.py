from .abstract_converter import AbstractConverter
import datetime

class TESConverter(AbstractConverter):

    def convert_to_wrroc(self, tes_data):
        # Implement the conversion logic from TES to WRROC
        wrroc_data = {
            "@id": tes_data["id"],
            "name": tes_data.get("name", ""),
            "description": tes_data.get("description", ""),
            "instrument": tes_data["executors"][0]["image"] if tes_data.get("executors") else None,
            "object": [{"@id": input.get("url"), "name": input.get("path")} for input in tes_data.get("inputs", [])],
            "result": [{"@id": output.get("url"), "name": output.get("path")} for output in tes_data.get("outputs", [])],
            "startTime": self.convert_to_iso8601(tes_data.get("creation_time")),
            "endTime": self.convert_to_iso8601(tes_data.get("end_time")),
        }
        return wrroc_data

    def convert_from_wrroc(self, wrroc_data):
        # Implement the conversion logic from WRROC to TES
        tes_data = {
            "id": wrroc_data["@id"],
            "name": wrroc_data.get("name", ""),
            "description": wrroc_data.get("description", ""),
            "executors": [{"image": wrroc_data.get("instrument")}],
            "inputs": [{"url": obj["@id"], "path": obj["name"]} for obj in wrroc_data.get("object", [])],
            "outputs": [{"url": res["@id"], "path": res["name"]} for res in wrroc_data.get("result", [])],
            "creation_time": wrroc_data.get("startTime"),
            "end_time": wrroc_data.get("endTime"),
        }
        return tes_data

    def convert_to_iso8601(self, timestamp):
        if timestamp:
            try:
                return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").isoformat() + "Z"
            except ValueError:
                # Handle incorrect format or other issues
                return None
        return None
