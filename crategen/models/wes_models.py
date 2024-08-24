from typing import Optional

from pydantic import BaseModel, Field, root_validator


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
    task_logs: Optional[list[WESRunLog]] = Field(
        None, description="This field is deprecated. Use tes_logs_url instead."
    )
    outputs: list[WESOutputs]

    class Config:
        extra = "allow"

    @root_validator
    def check_deprecated_fields(cls, values):
        if values.get("task_logs") is not None:
            print(
                "DeprecationWarning: The 'task_logs' field is deprecated and will be removed in future versions. Use 'tes_logs_url' instead."
            )
        return values
