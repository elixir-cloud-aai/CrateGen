from pydantic import ValidationError

from ..models.wrroc_models import WRROCDataWES
from ..models.wes_models import WESData
from ..utils import convert_to_iso8601
from .abstract_converter import AbstractConverter


class WESConverter(AbstractConverter):
    def convert_to_wrroc(self, wes_data):
        # Validate WES data
        try:
            validated_wes_data = WESData(**wes_data)
        except ValidationError as e:
            raise ValueError(f"Invalid WES data: {e}") from e

        # Extract validated data
        run_id = validated_wes_data.run_id
        name = validated_wes_data.run_log.name
        state = validated_wes_data.state
        start_time = validated_wes_data.run_log.start_time
        end_time = validated_wes_data.run_log.end_time
        outputs = validated_wes_data.outputs

        # Convert to WRROC
        wrroc_data = {
            "@id": run_id,
            "name": name,
            "status": state,
            "startTime": convert_to_iso8601(start_time),
            "endTime": convert_to_iso8601(end_time),
            "result": [
                {"@id": output.location, "name": output.name} for output in outputs
            ],
        }
        return wrroc_data

    def convert_from_wrroc(self, data):
        # Validate WRROC data
        try:
            validated_data = WRROCDataWES(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid WRROC data for WES conversion: {e}") from e

        # Extract validated data
        run_id = validated_data.id
        name = validated_data.name
        start_time = validated_data.startTime
        end_time = validated_data.endTime
        state = validated_data.status
        result_data = validated_data.result

        # Convert from WRROC to WES
        wes_data = {
            "run_id": run_id,
            "run_log": {"name": name, "start_time": start_time, "end_time": end_time},
            "state": state,
            "outputs": [{"location": res.id, "name": res.name} for res in result_data],
        }
        return wes_data
