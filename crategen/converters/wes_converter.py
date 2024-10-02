"""Module for converting WES data to WRROC format and vice versa."""

from typing import Any, Dict

from .abstract_converter import AbstractConverter
from .utils import convert_to_iso8601


class WESConverter(AbstractConverter):
    """Converter for WES data to WRROC and vice versa."""

    def convert_to_wrroc(self, wes_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert WES data to WRROC format.

        Args:
            wes_data (Dict[str, Any]): The WES data to be converted.

        Returns:
            Dict[str, Any]: The converted WRROC data.
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

    def convert_from_wrroc(self, wrroc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert WRROC data to WES format.

        Args:
            wrroc_data (Dict[str, Any]): The WRROC data to be converted.

        Returns:
            Dict[str, Any]: The converted WES data.
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
