"""Module for converting WES data to WRROC format and vice versa."""

from .abstract_converter import AbstractConverter
from .utils import convert_to_iso8601


class WESConverter(AbstractConverter):
    """Converter for WES data to WRROC and vice versa."""

    def convert_to_wrroc(self, wes_data):
        """Convert WES data to WRROC format.

        Args:
            data: The input WES data.

        Returns:
            The converted WRROC data.

        Raises:
            ValidationError: If WES data is invalid.
        """
        run_id = wes_data.get("run_id", "")
        name = wes_data.get("run_log", {}).get("name", "")
        state = wes_data.get("state", "")
        start_time = wes_data.get("run_log", {}).get("start_time", "")
        end_time = wes_data.get("run_log", {}).get("end_time", "")
        outputs = wes_data.get("outputs", {})

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
        """Convert WRROC data to WES format.

        Args:
            data: The input WRROC data.

        Returns:
            The converted WES data.

        Raises:
            ValidationError: If WRROC data is invalid.
        """
        run_id = wrroc_data.get("@id", "")
        name = wrroc_data.get("name", "")
        start_time = wrroc_data.get("startTime", "")
        end_time = wrroc_data.get("endTime", "")
        state = wrroc_data.get("status", "")
        result_data = wrroc_data.get("result", [])

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
