from pydantic import ValidationError
from .models import WRROCData, WRROCDataTES, WRROCDataWES

def validate_wrroc(data: dict, target_model) -> WRROCData:
    """
    Validate that the input data is a valid WRROC entity.

    Args:
        data (dict): The input data to validate.
        target_model (Type[BaseModel]): The target Pydantic model to validate against.

    Returns:
        WRROCData: The validated WRROC data.

    Raises:
        ValueError: If the data is not valid WRROC data.
    """
    try:
        return target_model(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid WRROC data: {e}")

def validate_wrroc_tes(data: dict) -> WRROCDataTES:
    return validate_wrroc(data, WRROCDataTES)

def validate_wrroc_wes(data: dict) -> WRROCDataWES:
    return validate_wrroc(data, WRROCDataWES)
