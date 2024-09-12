from typing import Optional, Annotated

from datetime import datetime

from pydantic import AnyUrl, BaseModel, Field

WRROC_ID = Annotated[str, Field(alias="@id")]


class WRROCInputs(BaseModel):
    """
    A model representing inputs in WRROC.

    Attributes:
        id (str): The unique identifier for the input.
        name (str): The name of the input.
    """

    id: WRROC_ID
    name: str


class WRROCOutputs(BaseModel):
    """
    A model representing outputs in WRROC.

    Attributes:
        id (str): The unique identifier for the output.
        name (str): The name of the output.
    """

    id: WRROC_ID
    name: str


class WRROCDataBase(BaseModel):
    """
    A base model representing common fields for WRROC entities.

    Attributes:
        id (str): The unique identifier for the WRROC entity.
        name (str): The name of the WRROC entity.
        description (Optional[str]): A brief description of the WRROC entity.
        instrument (Optional[str]): The instrument used in the WRROC entity.
        object (list[WRROCInputs]): A list of input objects related to the WRROC entity.
        result (WRROCOutputs): A list of output results related to the WRROC entity.
        startTime (Optional[datetime]): The start time of the WRROC entity.
        endTime (Optional[datetime]): The end time of the WRROC entity.
        version (Optional[str]): The version of the WRROC entity.
    """

    id: WRROC_ID
    name: str
    description: Optional[str] = ""
    instrument: Optional[str] = None
    object: list[WRROCInputs] = Field(default_factory=list)
    result: Optional[WRROCOutputs] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    version: Optional[str] = None

    class Config:
        extra = "allow"
        allow_population_by_field_name = True  # Allows using field name for input data


class WRROCData(WRROCDataBase):
    """
    A model representing a WRROC entity, inheriting from WRROCDataBase.
    """

    pass


class WRROCDataTES(WRROCDataBase):
    """
    A model representing WRROC data specifically for TES conversion.

    This model inherits from WRROCDataBase and includes all the necessary fields required for TES conversion.
    """

    pass


class WRROCDataWES(WRROCDataBase):
    """
    A model representing WRROC data specifically for WES conversion.

    This model inherits from WRROCDataBase and includes additional fields required for WES conversion.
    """

    status: str


class WRROCProcess(BaseModel):
    """
    A model representing the WRROC Process Run profile.

    Attributes:
        id (str): The unique identifier for the WRROC entity.
        name (str): The name of the WRROC entity.
        description (Optional[str]): A brief description of the WRROC entity.
        startTime (Optional[str]): The start time of the process.
        endTime (Optional[str]): The end time of the process.
        object (Optional[list[dict[str, str]]]): A list of input objects related to the process.
        profiles (Optional[list[AnyUrl]]): URLs to the RO-Crate profiles used.
    """

    id: WRROC_ID
    name: str
    description: Optional[str] = ""
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    object: Optional[list[dict[str, str]]] = None
    profiles: Optional[list[AnyUrl]] = None

    class Config:
        extra = "allow"
        allow_population_by_field_name = True


class WRROCWorkflow(WRROCProcess):
    """
    A model representing the WRROC Workflow Run profile, inheriting from WRROCProcess.

    Attributes:
        workflowType (Optional[str]): The type of the workflow.
        workflowVersion (Optional[str]): The version of the workflow.
        result (Optional[list[dict[str, str]]]): A list of output results related to the workflow.
        hasPart (Optional[list[AnyUrl]]): A list of parts or steps within the workflow.
    """

    workflowType: Optional[str] = None
    workflowVersion: Optional[str] = None
    result: Optional[list[dict[str, str]]] = None
    hasPart: Optional[list[AnyUrl]] = None

    class Config:
        extra = "allow"
        allow_population_by_field_name = True


class WRROCProvenance(WRROCWorkflow):
    """
    A model representing the WRROC Provenance Run profile, inheriting from WRROCWorkflow.

    Attributes:
        provenanceData (Optional[str]): Data related to the provenance of the workflow.
        agents (Optional[list[dict[str, str]]]): A list of agents involved in the workflow.
        activity (Optional[list[dict[str, str]]]): Activities related to the provenance.
        generatedBy (Optional[list[AnyUrl]]): URLs of the entities that generated the data.
        used (Optional[list[AnyUrl]]): URLs of the entities that were used in the data generation.
    """

    provenanceData: Optional[str] = None
    agents: Optional[list[dict[str, str]]] = None
    activity: Optional[list[dict[str, str]]] = None
    generatedBy: Optional[list[AnyUrl]] = None
    used: Optional[list[AnyUrl]] = None

    class Config:
        extra = "allow"
        allow_population_by_field_name = True
