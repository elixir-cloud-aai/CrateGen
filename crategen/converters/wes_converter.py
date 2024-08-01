from pydantic import ValidationError
from .abstract_converter import AbstractConverter
from ..models import WESData, WRROCDataWES
from .utils import convert_to_iso8601

class WESConverter(AbstractConverter):

    def convert_to_wrroc(self, wes_data):
        try:
            wes_model = WESData(**wes_data)
        except ValidationError as e:
            raise ValueError(f"Invalid WES data: {e}")
        outputs = wes_model.outputs

        wrroc_data = {
            "@id": wes_model.run_id,
            "name": wes_model.run_log.name,
            "status": wes_model.state,
            "startTime": convert_to_iso8601(wes_model.run_log.start_time),
            "endTime": convert_to_iso8601(wes_model.run_log.end_time),
            "result": [{"@id": output.location, "name": output.name} for output in outputs],
        }
        return wrroc_data

    def convert_from_wrroc(self, wrroc_data):
        try:
            wrroc_model = WRROCDataWES(**wrroc_data)
        except ValidationError as e:
            raise ValueError(f"Invalid WRROC data: {e}")

        result_data = wrroc_model.result

        wes_data = {
            "run_id": wrroc_model.id,
            "run_log": {
                "name": wrroc_model.name,
                "start_time": wrroc_model.startTime,
                "end_time": wrroc_model.endTime,
            },
            "state": wrroc_model.status,
            "outputs": [{"location": res.id, "name": res.name} for res in result_data],
        }
        return wes_data
