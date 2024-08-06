from pydantic import ValidationError
from .abstract_converter import AbstractConverter
from .utils import convert_to_iso8601
from ..models import TESData
from ..validators import validate_wrroc_tes

class TESConverter(AbstractConverter):

    def convert_to_wrroc(self, tes_data: dict) -> dict:
        try:
            validated_tes_data = TESData(**tes_data)
        except ValidationError as e:
            raise ValueError(f"Invalid TES data: {e}")

        wrroc_data = {
            "@id": validated_tes_data.id,
            "name": validated_tes_data.name,
            "description": validated_tes_data.description,
            "instrument": validated_tes_data.executors[0].image if validated_tes_data.executors else None,
            "object": [{"@id": input.url, "name": input.path} for input in validated_tes_data.inputs],
            "result": [{"@id": output.url, "name": output.path} for output in validated_tes_data.outputs],
            "startTime": convert_to_iso8601(validated_tes_data.creation_time),
            "endTime": convert_to_iso8601(validated_tes_data.logs[0].end_time) if validated_tes_data.logs else None,
        }
        return wrroc_data

    def convert_from_wrroc(self, data: dict) -> dict:
        try:
            data_validated = validate_wrroc_tes(data)
        except ValidationError as e:
            raise ValueError(f"Invalid WRROC data: {e}")

        tes_data = {
            "id": data_validated.id,
            "name": data_validated.name,
            "description": data_validated.description,
            "executors": [{"image": data_validated.instrument}],
            "inputs": [{"url": obj.id, "path": obj.name} for obj in data_validated.object],
            "outputs": [{"url": res.id, "path": res.name} for res in data_validated.result],
            "creation_time": data_validated.startTime,
            "logs": [{"end_time": data_validated.endTime}],
        }
        return tes_data