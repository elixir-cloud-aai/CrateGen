from pydantic import BaseModel
from typing import Optional


class Executor(BaseModel):
    """
    A model representing an executor in the Task Execution Service (TES).

    Attributes:
        image (str): The Docker image to be used.
        command (list[str]): The command to be executed.
    """
    image: str
    command: list[str]


class TESInputs(BaseModel):
    """
    A model representing input files in TES.

    Attributes:
        url (str): The URL of the input file.
        path (str): The path where the input file should be placed.
    """
    url: str
    path: str


class TESOutputs(BaseModel):
    """
    A model representing output files in TES.

    Attributes:
        url (str): The URL of the output file.
        path (str): The path where the output file is stored.
    """
    url: str
    path: str


class TESLogs(BaseModel):
    """
    A model representing logs in TES.

    Attributes:
        end_time (Optional[str]): The time the task ended.
    """
    end_time: Optional[str] = None


class TESData(BaseModel):
    """
    A model representing a TES task.

    Attributes:
        id (str): The unique identifier for the TES task.
        name (str): The name of the TES task.
        description (Optional[str]): A brief description of the TES task.
        executors (list[Executor]): The executors associated with the TES task.
        inputs (list[TESInputs]): The inputs to the TES task.
        outputs (list[TESOutputs]): The outputs of the TES task.
        creation_time (str): The time the task was created.
        logs (list[TESLogs]): Logs associated with the TES task.
    """
    id: str
    name: str
    description: Optional[str] = ""
    executors: list[Executor]
    inputs: list[TESInputs]
    outputs: list[TESOutputs]
    creation_time: str
    logs: list[TESLogs]

    class Config:
        extra = "forbid"


class WESRunLog(BaseModel):
    """
    A model representing a run log in the Workflow Execution Service (WES).

    Attributes:
        name (Optional[str]): The name of the run.
        start_time (Optional[str]): The start time of the run.
        end_time (Optional[str]): The end time of the run.
        cmd (Optional[list[str]]): The command executed in the run.
        stdout (Optional[str]): The path to the stdout log.
        stderr (Optional[str]): The path to the stderr log.
        exit_code (Optional[int]): The exit code of the run.
    """
    name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    cmd: Optional[list[str]] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None


class WESOutputs(BaseModel):
    """
    A model representing output files in WES.

    Attributes:
        location (str): The URL of the output file.
        name (str): The name of the output file.
    """
    location: str
    name: str


class WESRequest(BaseModel):
    """
    A model representing a workflow request in WES.

    Attributes:
        workflow_params (dict[str, str]): The parameters for the workflow.
        workflow_type (str): The type of the workflow (e.g., CWL).
        workflow_type_version (str): The version of the workflow type.
        tags (Optional[dict[str, str]]): Additional tags associated with the workflow.
    """
    workflow_params: dict[str, str]
    workflow_type: str
    workflow_type_version: str
    tags: Optional[dict[str, str]] = None


class WESData(BaseModel):
    """
    A model representing a WES run.

    Attributes:
        run_id (str): The unique identifier for the WES run.
        request (WESRequest): The request associated with the WES run.
        state (str): The state of the WES run.
        run_log (WESRunLog): The log of the WES run.
        task_logs (Optional[list[WESRunLog]]): The logs of individual tasks within the run.
        outputs (list[WESOutputs]): The outputs of the WES run.
    """
    run_id: str
    request: WESRequest
    state: str
    run_log: WESRunLog
    task_logs: Optional[list[WESRunLog]] = None
    outputs: list[WESOutputs]

    class Config:
        extra = "forbid"


class WRROCInputs(BaseModel):
    """
    A model representing inputs in WRROC.

    Attributes:
        id (str): The unique identifier for the input.
        name (str): The name of the input.
    """
    id: str
    name: str


class WRROCOutputs(BaseModel):
    """
    A model representing outputs in WRROC.

    Attributes:
        id (str): The unique identifier for the output.
        name (str): The name of the output.
    """
    id: str
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
        result (list[WRROCOutputs]): A list of output results related to the WRROC entity.
        startTime (Optional[str]): The start time of the WRROC entity.
        endTime (Optional[str]): The end time of the WRROC entity.
    """
    id: str
    name: str
    description: Optional[str] = ""
    instrument: Optional[str] = None
    object: list[WRROCInputs]
    result: list[WRROCOutputs]
    startTime: Optional[str] = None
    endTime: Optional[str] = None

    class Config:
        extra = "forbid"


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
    """
    id: str
    name: str
    description: Optional[str] = ""
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    object: Optional[list[dict[str, str]]] = None

    class Config:
        extra = "forbid"


class WRROCWorkflow(WRROCProcess):
    """
    A model representing the WRROC Workflow Run profile, inheriting from WRROCProcess.

    Attributes:
        workflowType (Optional[str]): The type of the workflow.
        workflowVersion (Optional[str]): The version of the workflow.
        result (Optional[list[dict[str, str]]]): A list of output results related to the workflow.
    """
    workflowType: Optional[str] = None
    workflowVersion: Optional[str] = None
    result: Optional[list[dict[str, str]]] = None

    class Config:
        extra = "forbid"


class WRROCProvenance(WRROCWorkflow):
    """
    A model representing the WRROC Provenance Run profile, inheriting from WRROCWorkflow.

    Attributes:
        provenanceData (Optional[str]): Data related to the provenance of the workflow.
        agents (Optional[list[dict[str, str]]]): A list of agents involved in the workflow.
    """
    provenanceData: Optional[str] = None
    agents: Optional[list[dict[str, str]]] = None

    class Config:
        extra = "forbid"
