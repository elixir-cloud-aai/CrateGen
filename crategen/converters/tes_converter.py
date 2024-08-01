from pydantic import ValidationError
from .abstract_converter import AbstractConverter
from .utils import convert_to_iso8601
from ..models import TESData, WRROCData

class TESConverter(AbstractConverter):

    def convert_to_wrroc(self, tes_data):
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

    def convert_from_wrroc(self, wrroc_data):
        try:
            validated_wrroc_data = WRROCData(**wrroc_data)
        except ValidationError as e:
            raise ValueError(f"Invalid WRROC data: {e}")

        tes_data = {
            "id": validated_wrroc_data.id,
            "name": validated_wrroc_data.name,
            "description": validated_wrroc_data.description,
            "executors": [{"image": validated_wrroc_data.instrument}],
            "inputs": [{"url": obj.id, "path": obj.name} for obj in validated_wrroc_data.object],
            "outputs": [{"url": res.id, "path": res.name} for res in validated_wrroc_data.result],
            "creation_time": validated_wrroc_data.startTime,
            "logs": [{"end_time": validated_wrroc_data.endTime}],
        }
        return tes_data
