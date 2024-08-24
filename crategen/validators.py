from typing import Union
from urllib.parse import urlparse

from pydantic import ValidationError

from .models.wrroc_models import (
    WRROCProcess,
    WRROCProvenance,
    WRROCWorkflow,
    WRROCDataTES,
    WRROCDataWES,
)


def validate_wrroc(data: dict) -> Union[WRROCProvenance, WRROCWorkflow, WRROCProcess]:
    """
    Validate that the input data is a valid WRROC entity and determine which profile it adheres to.


    This function attempts to validate the input data against the WRROCProvenance model first.
    If that validation fails, it attempts validation against the WRROCWorkflow model.
    If that also fails, it finally attempts validation against the WRROCProcess model.

    Returns:
        Union[WRROCProvenance, WRROCWorkflow, WRROCProcess]: The validated WRROC data, indicating the highest profile the data adheres to.

    Raises:
        ValueError: If the data does not adhere to any of the WRROC profiles.
    """
    try:
        return WRROCProvenance(**data)
    except ValidationError:
        pass

    try:
        return WRROCWorkflow(**data)
    except ValidationError:
        pass

    try:
        return WRROCProcess(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid WRROC data: {e.errors()}") from e


def validate_wrroc_tes(data: dict) -> WRROCDataTES:
    """
    Validate that the input data contains the fields required for WRROC to TES conversion.

    Returns:
        WRROCDataTES: The validated WRROC data that is suitable for TES conversion.

    Raises:
        ValueError: If the data is not valid WRROC data or does not contain the necessary fields for TES conversion.
    """
    data_validated = validate_wrroc(data)

    try:
        data_wrroc_tes = WRROCDataTES(**data_validated.dict())
    except ValidationError as exc:
        raise ValueError(
            f"WRROC data insufficient for TES conversion: {exc.errors()}"
        ) from exc

    return data_wrroc_tes


def validate_wrroc_wes(data: dict) -> WRROCDataWES:
    """
    Validate that the input data contains the fields required for WRROC to WES conversion.

    Returns:
        WRROCDataWES: The validated WRROC data that is suitable for WES conversion.

    Raises:
        ValueError: If the data is not valid WRROC data or does not contain the necessary fields for WES conversion.
    """
    data_validated = validate_wrroc(data)

    try:
        data_wrroc_wes = WRROCDataWES(**data_validated.dict())
    except ValidationError as exc:
        raise ValueError(
            f"WRROC data insufficient for WES conversion: {exc.errors()}"
        ) from exc

    # Validate URLs in the result field, only if result is not None
    if data_wrroc_wes.result is not None:
        for result in data_wrroc_wes.result:
            parsed_url = urlparse(result.id)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                raise ValueError(f"Invalid URL in result: {result.id}")

    return data_wrroc_wes
