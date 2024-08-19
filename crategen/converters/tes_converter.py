from .abstract_converter import AbstractConverter
from .utils import convert_to_iso8601
from ..models import TESData, WRROCDataTES
from pydantic import ValidationError

class TESConverter(AbstractConverter):

    def convert_to_wrroc(self, tes_data):
        # Validate TES data
        try:
            validated_tes_data = TESData(**tes_data)
        except ValidationError as e:
            raise ValueError(f"Invalid TES data: {e}")

        # Extract validated data
        id = validated_tes_data.id
        name = validated_tes_data.name
        description = validated_tes_data.description
        executors = validated_tes_data.executors
        inputs = validated_tes_data.inputs
        outputs = validated_tes_data.outputs
        creation_time = validated_tes_data.creation_time
        end_time = validated_tes_data.logs[0].end_time if validated_tes_data.logs else ""

        # Convert to WRROC
        wrroc_data = {
            "@id": id,
            "name": name,
            "description": description,
            "instrument": executors[0].image if executors else None,
            "object": [{"@id": input.url, "name": input.path} for input in inputs],
            "result": [{"@id": output.url, "name": output.path} for output in outputs],
            "startTime": convert_to_iso8601(creation_time),
            "endTime": convert_to_iso8601(end_time),
        }
        return wrroc_data

    def convert_from_wrroc(self, data):
        # Validate WRROC data
        try:
            validated_data = WRROCDataTES(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid WRROC data for TES conversion: {e}")

        # Extract validated data
        id = validated_data.id
        name = validated_data.name
        description = validated_data.description
        instrument = validated_data.instrument
        object_data = validated_data.object
        result_data = validated_data.result
        start_time = validated_data.startTime
        end_time = validated_data.endTime

        # Convert from WRROC to TES
        tes_data = {
            "id": id,
            "name": name,
            "description": description,
            "executors": [{"image": instrument}],
            "inputs": [{"url": obj.id, "path": obj.name} for obj in object_data],
            "outputs": [{"url": res.id, "path": res.name} for res in result_data],
            "creation_time": start_time,
            "logs": [{"end_time": end_time}],
        }
        return tes_data
