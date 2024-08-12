from pydantic import ValidationError
from typing import Dict, Union

# Import the WRROC models
from .models import WRROCProcess, WRROCWorkflow, WRROCProvenance

def validate_wrroc(data: Dict) -> Union[WRROCProvenance, WRROCWorkflow, WRROCProcess]:
    """
    Validate that the input data is a valid WRROC entity and determine which profile it adheres to.
    
    This function attempts to validate the input data against the WRROCProvenance model first.
    If that validation fails, it attempts validation against the WRROCWorkflow model.
    If that also fails, it finally attempts validation against the WRROCProcess model.
    
    Args:
        data (Dict): The input data to validate.
    
    Returns:
        Union[WRROCProvenance, WRROCWorkflow, WRROCProcess]: The validated WRROC data, indicating the highest profile the data adheres to.
    
    Raises:
        ValueError: If the data does not adhere to any of the WRROC profiles.
    """
    # Convert '@id' to 'id' for validation purposes
    if '@id' in data:
        data['id'] = data.pop('@id')

    try:
        return WRROCProvenance(**data)
    except ValidationError:
        try:
            return WRROCWorkflow(**data)
        except ValidationError:
            try:
                return WRROCProcess(**data)
            except ValidationError as e:
                raise ValueError(f"Invalid WRROC data: {e}")

def validate_wrroc_tes(data: Dict) -> WRROCProcess:
    """
    Validate that the input data contains the fields required for WRROC to TES conversion.

    This function first validates that the data is a valid WRROC entity by calling `validate_wrroc`.
    Then it checks that the data contains all necessary fields for TES conversion.

    Args:
        data (Dict): The input data to validate.

    Returns:
        WRROCProcess: The validated WRROC data that is suitable for TES conversion.

    Raises:
        ValueError: If the data is not valid WRROC data or does not contain the necessary fields for TES conversion.
    """
    validated_data = validate_wrroc(data)
    required_fields = ["id", "name", "object", "result"]

    for field in required_fields:
        if not getattr(validated_data, field, None):
            raise ValueError(f"Missing required field for TES conversion: {field}")

    return validated_data

def validate_wrroc_wes(data: Dict) -> WRROCWorkflow:
    """
    Validate that the input data contains the fields required for WRROC to WES conversion.

    This function first validates that the data is a valid WRROC entity by calling `validate_wrroc`.
    Then it checks that the data contains all necessary fields for WES conversion.

    Args:
        data (Dict): The input data to validate.

    Returns:
        WRROCWorkflow: The validated WRROC data that is suitable for WES conversion.

    Raises:
        ValueError: If the data is not valid WRROC data or does not contain the necessary fields for WES conversion.
    """
    validated_data = validate_wrroc(data)
    
    # Check for unexpected fields
    allowed_fields = {"id", "name", "status", "workflowType", "workflowVersion", "result", "startTime", "endTime"}
    unexpected_fields = set(data.keys()) - allowed_fields
    if unexpected_fields:
        raise ValueError(f"Unexpected fields in WRROC data: {unexpected_fields}")
    
    required_fields = ["id", "name", "workflowType", "workflowVersion", "result"]
    for field in required_fields:
        if not getattr(validated_data, field, None):
            raise ValueError(f"Missing required field for WES conversion: {field}")

    return validated_data

