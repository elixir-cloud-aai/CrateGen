from pydantic import BaseModel, AnyUrl, Field, root_validator
from typing import Optional


class Executor(BaseModel):
    """
    Represents an executor in the Task Execution Service (TES).

    Attributes:
        image (str): The Docker image to be used.
        command (list[str]): The command to be executed.
        workdir (Optional[str]): The working directory for the command.
        stdout (Optional[str]): The path to the stdout log.
        stderr (Optional[str]): The path to the stderr log.
        stdin (Optional[str]): The path to the stdin input.
        env (Optional[dict[str, str]]): Environment variables for the command.
    """
    image: str
    command: list[str]
    workdir: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    stdin: Optional[str] = None
    env: Optional[dict[str, str]] = None


class TESResources(BaseModel):
    """
    Represents the resources required by a TES task.

    Attributes:
        cpu_cores (Optional[int]): The number of CPU cores required.
        preemptible (Optional[bool]): Whether the task can run on preemptible instances.
        ram_gb (Optional[float]): The amount of RAM in GB required.
        disk_gb (Optional[float]): The amount of disk space in GB required.
        zones (Optional[list[str]]): The zones where the task can run.
    """
    cpu_cores: Optional[int] = None
    preemptible: Optional[bool] = None
    ram_gb: Optional[float] = None
    disk_gb: Optional[float] = None
    zones: Optional[list[str]] = None


class TESInputs(BaseModel):
    """
    Represents input files in TES.

    Attributes:
        name (Optional[str]): The name of the input file.
        description (Optional[str]): A brief description of the input.
        url (AnyUrl): The URL of the input file.
        path (str): The path where the input file should be placed.
        type (Optional[str]): The type of input (e.g., FILE, DIRECTORY).
        content (Optional[str]): The content of the input file, if provided inline.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    url: AnyUrl
    path: str
    type: Optional[str] = None
    content: Optional[str] = None


class TESOutputs(BaseModel):
    """
    Represents output files in TES.

    Attributes:
        name (Optional[str]): The name of the output file.
        description (Optional[str]): A brief description of the output.
        url (AnyUrl): The URL of the output file.
        path (str): The path where the output file is stored.
        type (Optional[str]): The type of output (e.g., FILE, DIRECTORY).
    """
    name: Optional[str] = None
    description: Optional[str] = None
    url: AnyUrl
    path: str
    type: Optional[str] = None


class TESLogs(BaseModel):
    """
    Represents logs in TES.

    Attributes:
        start_time (Optional[str]): The time the task started.
        end_time (Optional[str]): The time the task ended.
        stdout (Optional[str]): The path to the stdout log.
        stderr (Optional[str]): The path to the stderr log.
        exit_code (Optional[int]): The exit code of the task.
        host_ip (Optional[str]): The IP address of the host running the task.
        metadata (Optional[dict[str, str]]): Additional metadata associated with the task.
    """
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    host_ip: Optional[str] = None
    metadata: Optional[dict[str, str]] = None


class TESData(BaseModel):
    """
    Represents a TES task.

    Attributes:
        id (str): The unique identifier for the TES task.
        name (Optional[str]): The name of the TES task.
        description (Optional[str]): A brief description of the TES task.
        creation_time (Optional[str]): The time the task was created.
        state (Optional[str]): The current state of the task.
        inputs (list[TESInputs]): The inputs to the TES task.
        outputs (list[TESOutputs]): The outputs of the TES task.
        executors (list[Executor]): The executors associated with the TES task.
        resources (Optional[TESResources]): The resources required by the TES task.
        volumes (Optional[list[str]]): The volumes to be mounted in the task.
        logs (Optional[list[TESLogs]]): Logs associated with the TES task.
        tags (Optional[dict[str, str]]): Tags associated with the task.
        error (Optional[dict[str, str]]): Error information if the task failed.
    """
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    creation_time: Optional[str] = None
    state: Optional[str] = None
    inputs: list[TESInputs]
    outputs: list[TESOutputs]
    executors: list[Executor]
    resources: Optional[TESResources] = None
    volumes: Optional[list[str]] = None
    logs: Optional[list[TESLogs]] = None
    tags: Optional[dict[str, str]] = None
    error: Optional[dict[str, str]] = None

    class Config:
        extra = "allow"


class WESRunLog(BaseModel):
    """
    Represents a run log in the Workflow Execution Service (WES).

    Attributes:
        name (Optional[str]): The name of the run.
        start_time (Optional[str]): The start time of the run.
        end_time (Optional[str]): The end time of the run.
        cmd (Optional[list[str]]): The command executed in the run.
        stdout (Optional[str]): The path to the stdout log.
        stderr (Optional[str]): The path to the stderr log.
        exit_code (Optional[int]): The exit code of the run.
        tes_logs_url (Optional[str]): The URL of the TES logs.
    """
    name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    cmd: Optional[list[str]] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    tes_logs_url: Optional[str] = None


class WESOutputs(BaseModel):
    """
    Represents output files in WES.

    Attributes:
        location (str): The URL of the output file.
        name (str): The name of the output file.
    """
    location: str
    name: str


class WESRequest(BaseModel):
    """
    Represents a workflow request in WES.

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
    Represents a WES run.

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
    task_logs: Optional[list[WESRunLog]] = Field(None, description="This field is deprecated. Use tes_logs_url instead.")
    outputs: list[WESOutputs]

    class Config:
        extra = "allow"
        
    @root_validator
    def check_deprecated_fields(cls, values):
        if values.get('task_logs') is not None:
            print("DeprecationWarning: The 'task_logs' field is deprecated and will be removed in future versions. Use 'tes_logs_url' instead.")
        return values

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
        version (Optional[str]): The version of the WRROC entity.
    """
    id: str
    name: str
    description: Optional[str] = ""
    instrument: Optional[str] = None
    object: list[WRROCInputs]
    result: list[WRROCOutputs]
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    version: Optional[str] = None

    class Config:
        extra = "allow"


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
    id: str
    name: str
    description: Optional[str] = ""
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    object: Optional[list[dict[str, str]]] = None
    profiles: Optional[list[AnyUrl]] = None

    class Config:
        extra = "allow"


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

