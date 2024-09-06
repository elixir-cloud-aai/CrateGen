"""
Each model in this module conforms to the corresponding WES model names as specified by the GA4GH schema (https://ga4gh.github.io/workflow-execution-service-schemas/docs/).
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator

from ..utils import convert_to_rfc3339_format


class State(str, Enum):
    UNKNOWN = "UNKNOWN"
    QUEUED = "QUEUED"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETE = "COMPLETE"
    EXECUTOR_ERROR = "EXECUTOR_ERROR"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    CANCELLED = "CANCELLED"
    CANCELING = "CANCELING"
    PREEMPTED = "PREEMPTED"


class Log(BaseModel):
    """
    Represents a run log in the Workflow Execution Service (WES).

    **Attributes:**

    - **name** (`Optional[str]`): The task or workflow name.
    - **cmd** (`Optional[list[str]]`): The command line that was executed.
    - **start_time** (`Optional[str]`): When the command started executing, in ISO 8601 format.
    - **end_time** (`Optional[str]`): When the command stopped executing, in ISO 8601 format.
    - **stdout** (`Optional[str]`): A URL to retrieve standard output logs of the workflow run or task..
    - **stderr** (`Optional[str]`): A URL to retrieve standard error logs of the workflow run or task.
    - **exit_code** (`Optional[int]`): The exit code of the program.
    - **system_logs** (`optional[list[str]]`):  Any logs the system decides are relevant, which are not tied directly to a workflow.

    **Reference:** https://ga4gh.github.io/workflow-execution-service-schemas/docs/#tag/runlog_model
    """

    name: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    cmd: Optional[list[str]]
    stdout: Optional[str]
    stderr: Optional[str]
    exit_code: Optional[int]
    system_logs: Optional[list[str]]

    @validator("start_time", "end_time")
    def validate_datetime(value):
        return convert_to_rfc3339_format(value)


class TaskLog(Log):
    """
    Represents a task log in the Workflow Execution Service (WES).

    **Attributes:**

    - **name** (`str`): The task or workflow name.
    - **cmd** (`Optional[list[str]]`): The command line that was executed.
    - **start_time** (`Optional[str]`): When the command started executing, in ISO 8601 format.
    - **end_time** (`Optional[str]`): When the command stopped executing, in ISO 8601 format.
    - **stdout** (`Optional[str]`): A URL to retrieve standard output logs of the workflow run or task..
    - **stderr** (`Optional[str]`): A URL to retrieve standard error logs of the workflow run or task.
    - **exit_code** (`Optional[int]`): The exit code of the program.
    - **system_logs** (`Optional[list[str]]`):  Any logs the system decides are relevant, which are not tied directly to a workflow.
    - **id** (`str`): A unique identifier which maybe used to reference the task
    - **tes_uri** (`Optional[str]`): An optional URL pointing to an extended task definition defined by a TES api

    **Reference:** https://ga4gh.github.io/workflow-execution-service-schemas/docs/#tag/runlog_model
    """

    id: str
    tes_uri: Optional[str]
    name: str = Field(
        ...
    )  # test if adding Field makes a diff, gemini says no on specific questioning.


class RunRequest(BaseModel):
    """
    Represents a workflow request in WES.

    **Attributes:**

    - **workflow_params** (`Optional[dict[str, str]]`): The workflow run parameterizations(JSON encoded), including input and output file locations.
    - **workflow_type** (`str`): The workflow descriptor type.
    - **workflow_type_version** (`str`): The workflow descriptor type version.
    - **tags** (`Optional[dict[str, str]]`): Additional tags associated with the workflow.
    - **workflow_engine_parameters** (Optional[dict[str, str]]): Input values specific to the workflow engine.
    - **workflow_engine** (`Optional[str]`): The workflow engine.
    - **workflow_engine_version (`Optional[str]`): The workflow engine version.
    - **workflow_url** (`str`): The workflow url

    **Reference:** https://ga4gh.github.io/workflow-execution-service-schemas/docs/#tag/runlog_model
    """

    workflow_params: dict[str, str]
    workflow_type: str
    workflow_type_version: str
    tags: Optional[dict[str, str]] = {}
    workflow_engine_parameters: Optional[dict[str, str]]
    workflow_engine: Optional[str]
    workflow_engine_version: Optional[str]
    workflow_url: str

    @root_validator()
    def validate_workflow_engine(values):
        """
        - If workflow_engine_version is set the workflow_engine must be set.
        """
        engine_version = values.get("workflow_engine_version")
        engine = values.get("wokflow_engine")

        if engine_version is not None and engine is None:
            raise ValueError(
                "The 'workflow_engine' attribute is required when the 'workflow_engine_verision' attribute is set"
            )
        return values


class WESData(BaseModel):
    """
    Represents a WES run.

    **Attributes:**

    - **run_id** (`str`): The unique identifier for the WES run.
    - **request** (`Optional[RunRequest]`): The request associated with the WES run.
    - **state** (`Optional[State]`): The state of the WES run.
    - **run_log** (`Object`): The log of the WES run.
    - **task_logs_url** (`Optional[str]`): A reference to the complete url which may be used to obtain a paginated list of task logs for this workflow.
    - **task_logs** (`Optional[list[Log | RunLog] | None]`): The logs of individual tasks within the run. This attribute is deprecated.
    - **outputs** (`dict[str, str]`): The outputs of the WES run.

    **Reference:** https://ga4gh.github.io/workflow-execution-service-schemas/docs/#tag/runlog_model
    """

    run_id: str
    request: Optional[RunRequest]
    state: Optional[State]
    run_log: Optional[Log]
    task_logs_url: Optional[str]
    task_logs: Optional[list[Log | TaskLog] | None]
    outputs: dict[str, str]

    @root_validator
    def check_deprecated_fields(cls, values):
        if values.get("task_logs") is not None:
            print(
                "DeprecationWarning: The 'task_logs' field is deprecated and will be removed in future versions. Use 'tes_logs_url' instead."
            )
        return values
