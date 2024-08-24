from pydantic import ValidationError

from ..models.tes_models import TESData
from ..models.wrroc_models import WRROCDataTES
from .abstract_converter import AbstractConverter


class TESConverter(AbstractConverter):
    def convert_to_wrroc(self, data: dict) -> dict:
        """
        Convert TES data to WRROC format.

        Args:
            data (dict): The input TES data.

        Returns:
            dict: The converted WRROC data.

        Raises:
            ValidationError: If TES data is invalid.
        """
        # Validate TES data
        try:
            data_tes = TESData(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid TES data: {e.errors()}") from e

        # Extract validated data
        (
            id,
            name,
            description,
            creation_time,
            state,
            inputs,
            outputs,
            executors,
            resources,
            volumes,
            logs,
            tags,
        ) = data_tes.dict().values()
        end_time = logs[0].end_time

        # Convert to WRROC format
        wrroc_data = {
            "@id": id,
            "name": name,
            "description": description,
            "instrument": executors[0]["image"] if executors else None,
            "object": [
                {"@id": input["url"], "name": input["path"], "type": input["type"]}
                for input in inputs
            ],
            "result": [
                {"@id": output["url"], "name": output["path"]} for output in outputs
            ],
            "startTime": creation_time,
            "endTime": end_time,
        }
        return wrroc_data

    def convert_from_wrroc(self, data: dict) -> dict:
        """
        Convert WRROC data to TES format.

        Args:
            data (dict): The input WRROC data.

        Returns:
            dict: The converted TES data.

        Raises:
            ValidationError: If WRROC data is invalid.
        """
        # Validate WRROC data
        try:
            data_wrroc = WRROCDataTES(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid WRROC data: {e.errors()}") from e

        # Convert from WRROC to TES format
        tes_data = {
            "id": data_wrroc.id,
            "name": data_wrroc.name,
            "description": data_wrroc.description,
            "executors": [{"image": data_wrroc.instrument}],
            "inputs": [{"url": obj.id, "path": obj.name} for obj in data_wrroc.object],
            "outputs": [{"url": res.id, "path": res.name} for res in data_wrroc.result],
            "creation_time": data_wrroc.startTime,
            "logs": [{"end_time": data_wrroc.endTime}],
        }
        return tes_data
