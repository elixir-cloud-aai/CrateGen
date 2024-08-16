from pydantic import ValidationError
from typing import Union
from .models import WRROCProcess, WRROCWorkflow, WRROCProvenance
from urllib.parse import urlparse

def validate_wrroc(data: dict) -> Union[WRROCProvenance, WRROCWorkflow, WRROCProcess]:
    """
    Validate that the input data is a valid WRROC entity and determine which profile it adheres to.
    
    This function attempts to validate the input data against the WRROCProvenance model first.
    If that validation fails, it attempts validation against the WRROCWorkflow model.
    If that also fails, it finally attempts validation against the WRROCProcess model.
    
    Args:
        data (dict): The input data to validate.
    
    Returns:
        Union[WRROCProvenance, WRROCWorkflow, WRROCProcess]: The validated WRROC data, indicating the highest profile the data adheres to.
    
    Raises:
        ValueError: If the data does not adhere to any of the WRROC profiles.
    """
    # Convert '@id' to 'id' for validation purposes
    if '@id' in data:
        data['id'] = data.pop('@id')

    errors = []

    try:
        return WRROCProvenance(**data)
    except ValidationError as e:
        errors.extend(e.errors())

    try:
        return WRROCWorkflow(**data)
    except ValidationError as e:
        errors.extend(e.errors())

    try:
        return WRROCProcess(**data)
    except ValidationError as e:
        errors.extend(e.errors())
        raise ValueError(f"Invalid WRROC data: {errors}")

def validate_wrroc_tes(data: dict) -> WRROCProcess:
    """
    Validate that the input data contains the fields required for WRROC to TES conversion.

    This function first validates that the data is a valid WRROC entity by calling `validate_wrroc`.
    Then it checks that the data contains all necessary fields for TES conversion.

    Args:
        data (dict): The input data to validate.

    Returns:
        WRROCProcess: The validated WRROC data that is suitable for TES conversion.

    Raises:
        ValueError: If the data is not valid WRROC data or does not contain the necessary fields for TES conversion.
    """
    validated_data = validate_wrroc(data)
    required_fields = ["id", "name", "object", "result"]

    missing_fields = [field for field in required_fields if getattr(validated_data, field) is None]

    if missing_fields:
        raise ValueError(f"Missing required field(s) for TES conversion: {', '.join(missing_fields)}")

    return validated_data

def validate_wrroc_wes(data: dict) -> WRROCWorkflow:
    """
    Validate that the input data contains the fields required for WRROC to WES conversion.

    This function first validates that the data is a valid WRROCWorkflow entity by calling `validate_wrroc`.
    Then it checks that the data contains all necessary fields for WES conversion.

    Args:
        data (dict): The input data to validate.

    Returns:
        WRROCWorkflow: The validated WRROC data that is suitable for WES conversion.

    Raises:
        ValueError: If the data is not valid WRROC data or does not contain the necessary fields for WES conversion.
    """
    validated_data = validate_wrroc(data)

    if not isinstance(validated_data, WRROCWorkflow):
        raise ValueError("The validated data is not a WRROCWorkflow entity.")

    required_fields = ["id", "name", "workflowType", "workflowVersion", "result"]

    missing_fields = [field for field in required_fields if getattr(validated_data, field) is None]

    if missing_fields:
        raise ValueError(f"Missing required field(s) for WES conversion: {', '.join(missing_fields)}")

    # Validate URLs in the result field, only if result is not None
    if validated_data.result is not None:
        for result in validated_data.result:
            url = result['id']
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                raise ValueError(f"Invalid URL in result: {url}")

    return validated_data


