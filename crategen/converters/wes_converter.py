from pydantic import ValidationError

from ..models.wes_models import Log, RunRequest, WESData, WESOutputs, State
from ..models.wrroc_models import WRROCDataWES, WRROCOutputs
from ..utils import convert_to_iso8601
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

        wrroc_output = (
            WRROCOutputs(
                id=data_wes.outputs.get("location"), name=data_wes.outputs.get("name")
            )
            if data_wes.outputs.get("location")
            else None
        )

        wrroc_data = WRROCDataWES(
            id=data_wes.run_id,
            name=data_wes.run_log.name,
            status=data_wes.state,
            startTime=convert_to_iso8601(data_wes.run_log.start_time),
            endTime=convert_to_iso8601(data_wes.run_log.end_time),
            result=wrroc_output,
        )

        return wrroc_data.dict(exclude_none=True)

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

        wes_run_log = Log(
            name=data_wrroc.name,
            start_time=data_wrroc.startTime,
            end_time=data_wrroc.endTime,
        )
        wes_request = RunRequest(
            workflow_params={},  # Adjust as necessary
            workflow_type="CWL",  # Example type, adjust as necessary
            workflow_type_version="v1.0",  # Example version, adjust as necessary
            workflow_url="",
        )

        state = State(data_wrroc.status)

        wes_data = WESData(
            run_id=data_wrroc.id,
            request=wes_request,
            state=state,
            run_log=wes_run_log,
            task_logs=None,  # Provide appropriate value
            outputs={"location": data_wrroc.result.id, "name": data_wrroc.result.name},
        )

        # Validate WES data before returning
        wes_data = WESData(**wes_data.dict())
        return wes_data.dict()
