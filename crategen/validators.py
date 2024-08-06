from pydantic import ValidationError
from .models import WRROCData, WRROCDataTES, WRROCDataWES

def validate_wrroc(data: dict) -> WRROCData:
    """
    Validate that the input data is a valid WRROC entity.

    Args:
        data (dict): The input data to validate.

    Returns:
        WRROCData: The validated WRROC data.

    Raises:
        ValueError: If the data is not valid WRROC data.
    """
    try:
        return WRROCData(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid WRROC data: {e}")

def validate_wrroc_tes(data: dict) -> WRROCDataTES:
    """
    Validate that the input data is a valid WRROC entity for TES.

    Args:
        data (dict): The input data to validate.

    Returns:
        WRROCDataTES: The validated WRROC data for TES.

    Raises:
        ValueError: If the data is not valid WRROC data for TES.
    """
    try:
        return WRROCDataTES(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid WRROC data: {e}")

def validate_wrroc_wes(data: dict) -> WRROCDataWES:
    """
    Validate that the input data is a valid WRROC entity for WES.

    Args:
        data (dict): The input data to validate.

    Returns:
        WRROCDataWES: The validated WRROC data for WES.

    Raises:
        ValueError: If the data is not valid WRROC data for WES.
    """
    try:
        return WRROCDataWES(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid WRROC data: {e}")
