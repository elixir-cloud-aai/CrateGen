from pydantic import ValidationError

from ..models.wes_models import WESData, WESOutputs, RunRequest, Log
from ..models.wrroc_models import WRROCDataWES
from ..utils import convert_to_iso8601
from ..validators import validate_wrroc_wes
from .abstract_converter import AbstractConverter


class WESConverter(AbstractConverter):
    def convert_to_wrroc(self, data: dict) -> dict:
        """
        Convert WES data to WRROC format.

        Args:
            data: The input WES data.

        Returns:
            The converted WRROC data.

        Raises:
            ValidationError: If WES data is invalid.
        """
        # Validate WES data
        try:
            data_wes = WESData(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid WES data: {e.errors()}") from e

        # create the object using the model
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
            data: The input WRROC data.

        Returns:
            The converted WES data.

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

        wes_outputs = [
            WESOutputs(location=res.id, name=res.name) for res in data_wrroc.result
        ]
        wes_run_log = Log(
            name=data_wrroc.name,
            start_time=data_wrroc.startTime,
            end_time=data_wrroc.endTime,
        )
        wes_request = RunRequest(
            workflow_params={},  # Adjust as necessary
            workflow_type="CWL",  # Example type, adjust as necessary
            workflow_type_version="v1.0",  # Example version, adjust as necessary
        )

        wes_data = WESData(
            run_id=data_wrroc.id,
            request=wes_request,
            state=data_wrroc.status,
            run_log=wes_run_log,
            task_logs=None,  # Provide appropriate value
            outputs=wes_outputs,
        )

        # Validate WES data before returning
        wes_data = WESData(**wes_data.dict())
        return wes_data.dict()
