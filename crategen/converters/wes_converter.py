from pydantic import ValidationError

from ..models.wes_models import WESData
from ..models.wrroc_models import WRROCDataWES
from ..utils import convert_to_iso8601
from .abstract_converter import AbstractConverter


class WESConverter(AbstractConverter):
    def convert_to_wrroc(self, data: dict) -> dict:
        """
        Convert WES data to WRROC format.

        Args:
            data (dict): The input WES data.

        Returns:
            dict: The converted WRROC data.

        Raises:
            ValidationError: If WES data is invalid.
        """
        # Validate WES data
        try:
            data_wes = WESData(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid WES data: {e.errors()}") from e

        # Convert to WRROC format
        wrroc_data = {
            "@id": data_wes.run_id,
            "name": data_wes.run_log.name,
            "status": data_wes.state,
            "startTime": convert_to_iso8601(data_wes.run_log.start_time),
            "endTime": convert_to_iso8601(data_wes.run_log.end_time),
            "result": [
                {"@id": output.location, "name": output.name}
                for output in data_wes.outputs
            ],
        }
        return wrroc_data

    def convert_from_wrroc(self, data: dict) -> dict:
        """
        Convert WRROC data to WES format.

        Args:
            data (dict): The input WRROC data.

        Returns:
            dict: The converted WES data.

        Raises:
            ValidationError: If WRROC data is invalid.
        """
        # Validate WRROC data
        try:
            data_wrroc = WRROCDataWES(**data)
        except ValidationError as e:
            raise ValueError(
                f"Invalid WRROC data for WES conversion: {e.errors()}"
            ) from e

        # Convert from WRROC to WES format
        # Convert from WRROC to WES format
        wes_data = {
            "run_id": data_wrroc.id,
            "run_log": {
                "name": data_wrroc.name,
                "start_time": data_wrroc.startTime,
                "end_time": data_wrroc.endTime,
            },
            "state": data_wrroc.status,
            "outputs": [
                {"location": res.id, "name": res.name} for res in data_wrroc.result
            ],
        }
        return wes_data
