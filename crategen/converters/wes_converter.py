from pydantic import ValidationError
from .abstract_converter import AbstractConverter
from ..models import WESData
from .utils import convert_to_iso8601
from ..validators import validate_wrroc_wes

class WESConverter(AbstractConverter):

    def convert_to_wrroc(self, wes_data: dict) -> dict:
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


    def convert_from_wrroc(self, data: dict) -> dict:
        try:
            data_validated = validate_wrroc_wes(data)
        except ValidationError as e:
            raise ValueError(f"Invalid WRROC data: {e}")

        wes_data = {
            "run_id": data_validated.id,
            "run_log": {
                "name": data_validated.name,
                "start_time": data_validated.startTime,
                "end_time": data_validated.endTime,
            },
            "state": data_validated.status,
            "outputs": [{"location": res.id, "name": res.name} for res in data_validated.result],
        }
        return wes_data