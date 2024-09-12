from datetime import datetime

from pydantic import AnyUrl, ValidationError

from ..models.tes_models import (
    TESData,
    TESExecutor,
    TESInput,
    TESOutput,
    TESState,
    TESTaskLog,
)
from ..models.wrroc_models import WRROCDataTES
from ..validators import validate_wrroc_tes
from .abstract_converter import AbstractConverter


class TESConverter(AbstractConverter):
    def convert_to_wrroc(self, data: dict) -> dict:
        """
        Convert TES data to WRROC format.

        Args:
            data: The input TES data.

        Returns:
            The converted WRROC data.

        Raises:
            ValidationError: If TES data is invalid.
        """
        # Validate TES data
        try:
            data_tes = TESData(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid TES data: {e.errors()}") from e

        executors = data_tes.executors
        end_time = data_tes.logs[0].end_time if data_tes.logs else None

        wrroc_data = {
            "@id": data_tes.id,
            "name": data_tes.name,
            "description": data_tes.description,
            "instrument": executors[0].image if executors else None,
            "object": [
                {"@id": input.url, "name": input.path} for input in data_tes.inputs
            ],
            "result": [
                {"@id": output.url, "name": output.path} for output in data_tes.outputs
            ],
            "startTime": data_tes.creation_time,
            "endTime": end_time,
        }

        validate_wrroc_tes(wrroc_data)
        return wrroc_data

    def convert_from_wrroc(self, data: dict) -> dict:
        """
        Convert WRROC data to TES format.

        Args:
            data: The input WRROC data.

        Returns:
            The converted TES data.

        Raises:
            ValidationError: If WRROC data is invalid.
        """
        # Validate WRROC data
        try:
            data_wrroc = WRROCDataTES(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid WRROC data: {e.errors()}") from e

        # Convert URL strings to AnyUrl
        tes_inputs = [
            TESInput(url=AnyUrl(url=obj.id), path=obj.name) for obj in data_wrroc.object
        ]
        tes_outputs = [
            TESOutput(url=AnyUrl(url=data_wrroc.result.id), path=data_wrroc.result.name)
        ]

        # Ensure 'image' and 'command' fields are provided
        tes_executors = [
            TESExecutor(image=data_wrroc.instrument or "", command=[])
        ]  # Provide default empty list for command

        # Ensure correct type for end_time (datetime)

        tes_logs = [
            TESTaskLog(
                logs=[],
                metadata=None,
                start_time=None,
                end_time=data_wrroc.endTime,
                outputs=[],
                system_logs=None,
            )
        ]

        tes_data = TESData(
            id=data_wrroc.id,
            name=data_wrroc.name,
            description=data_wrroc.description,
            executors=tes_executors,
            inputs=tes_inputs,
            outputs=tes_outputs,
            creation_time=None,
            logs=tes_logs,
            state=TESState.UNKNOWN,
        )

        # Validate TES data before returning
        tes_data = TESData(**tes_data.dict())
        return tes_data.dict()
