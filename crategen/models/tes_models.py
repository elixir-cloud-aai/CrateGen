"""
Each model in this module conforms to the corresponding TES model names as specified by the GA4GH schema (https://ga4gh.github.io/task-execution-schemas/docs/).
"""

import os
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseModel, root_validator, validator

from ..converters.utils import convert_to_iso8601


class TESFileType(str, Enum):
    FILE = "FILE"
    DIRECTORY = "DIRECTORY"


class TESState(str, Enum):
    UNKNOWN = "UNKNOWN"
    QUEUED = "QUEUED"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETE = "COMPLETE"
    EXECUTOR_ERROR = "EXECUTOR_ERROR"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    CANCELLED = "CANCELLED"


class TESOutputFileLog(BaseModel):
    """
    Information about all output files. Directory outputs are flattened into separate items.

    **Attributes:**

    - **url** (`str`): URL of the file in storage.
    - **path** (`str`): Path of the file inside the container. Must be an absolute path.
    - **size_bytes** (`str`): Size of the file in bytes. Note, this is currently coded as a string because official JSON doesn't support int64 numbers.

    **Reference:** https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    url: str
    path: str
    size_bytes: str


class TESExecutorLog(BaseModel):
    """
    Logs for each executor

    **Attributes:**

    - **start_time** (`Optional[str]`): Time the executor started, in RFC 3339 format.
    - **end_time** (`Optional[str]`): Time the executor ended, in RFC 3339 format.
    - **stdout** (`Optional[str]`): Stdout content.
    - **stderr** (`Optional[str]`): Stderr content.
    - **exit_code** (`int`): The exit code of the executor.

    **Reference:** https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: int

    @validator("start_time", "end_time", pre=True, always=True)
    def validate_datetime(cls, value):
        return convert_to_iso8601(value)


class TESExecutor(BaseModel):
    """
    An array of executors to be run

    **Attributes:**
    - **image** (`str`): Name of the container image.
    - **command** (`list[str]`): A sequence of program arguments to execute, where the first argument is the program to execute.
    - **workdir** (`Optional[str]`): The working directory that the command will be executed in.
    - **stdout** (`Optional[str]`): Path inside the container to a file where the executor's stdout will be written to. Must be an absolute path
    - **stderr** (`Optional[str]`): Path inside the container to a file where the executor's stderr will be written to. Must be an absolute path.
    - **stdin** (`Optional[str]`): Path inside the container to a file which will be piped to the executor's stdin. Must be an absolute path.
    - **env** (`Optional[dict[str, str]]`): Enviromental variables to set within the container

    **Reference:** https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    image: str
    command: list[str]
    workdir: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    stdin: Optional[str] = None
    env: Optional[dict[str, str]] = None

    @validator("stdin", "stdout")
    def validate_stdin_stdin(cls, value, field):
        """Ensure that 'stdin' and 'stdout' are absolute paths."""
        if value and not os.path.isabs(value):
            raise ValueError(f"The '{field.name}' attribute must contain an absolute path.")
        return value


class TESResources(BaseModel):
    """
    Represents the resources required by a TES task.

    **Attributes:**

    - **cpu_cores** (`Optional[int]`): Requested number of CPUs.
    - **preemptible** (`Optional[bool]`): Define if the task is allowed to run on preemptible compute instances, for example, AWS Spot.
    - **ram_gb** (`Optional[float]`): The amount of RAM in GB required.
    - **disk_gb** (`Optional[float]`): The amount of disk space in GB required.
    - **zones** (`Optional[list[str]]`): Request that the task be run in these compute zones.

    **Reference:** https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    cpu_cores: Optional[int] = None
    preemptible: Optional[bool] = None
    ram_gb: Optional[float] = None
    disk_gb: Optional[float] = None
    zones: Optional[list[str]] = None


class TESInput(BaseModel):
    """
    Input files that will be used by the task. Inputs will be downloaded and mounted into the executor container as defined by the task request document.

    **Attributes:**

    - **name** (`Optional[str]`): The name of the input file.
    - **description** (`Optional[str]`): A brief description of the input.
    - **url** (`AnyUrl`): The URL of the input file. Must be an absolute path
    - **path** (`str`): TPath of the file inside the container. Must be an absolute path.
    - **type** (`TESFileType`): The type of input ('FILE' or 'DIRECTORY'). Default is 'FILE'
    - **content** (`Optional[str]`): The content of the input file, if provided inline.

    Reference: https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[AnyUrl]
    path: str
    type: TESFileType = TESFileType.FILE
    content: Optional[str] = None

    @root_validator()
    def validate_content_and_url(cls, values):
        """
        - If content is set url should be ignored
        - If content is not set then url should be present
        """
        content_is_set = (
            values.get("content") and len(values.get("content").strip()) > 0
        )
        url_is_set = values.get("url") and len(values.get("url").strip()) > 0

        if content_is_set:
            values["url"] = None
        elif not content_is_set and not url_is_set:
            raise ValueError(
                "The 'url' attribute is required when the 'content' attribute is empty"
            )
        return values

    @validator("path")
    def validate_path(cls, value):
        if not os.path.isabs(value):
            raise ValueError("The 'path' attribute must contain an absolute path.")
        return value


class TESOutput(BaseModel):
    """
    Output files. Outputs will be uploaded from the executor container to long-term storage.

    **Attributes:**

    - **name** (`Optional[str]`): User-provided name of output file
    - **description** (`Optional[str]`): Optional users provided description field, can be used for documentation.
    - **url** (`AnyUrl`): URL for the file to be copied by the TES server after the task is complete
    - **path** (`str`): Path of the file inside the container. Must be an absolute path.
    - **type** (`TESFileType`): The type of output (e.g., FILE, DIRECTORY).

    Reference: https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    name: Optional[str] = None
    description: Optional[str] = None
    url: AnyUrl
    path: str
    type: TESFileType = TESFileType.FILE

    @validator("path")
    def validate_path(cls, value):
        if not os.path.isabs(value):
            raise ValueError("The 'path' attribute must contain an absolute path.")
        return value


class TESTaskLog(BaseModel):
    """
    Task logging information. Normally, this will contain only one entry, but in the case where a task fails and is retried, an entry will be appended to this list.

    **Attributes:**

    - **logs** (`list[TESExecutorLog]`): Logs for each executor.
    - **metadata** (`Optional[dict[str, str]]`): Arbitrary logging metadata included by the implementation.
    - **start_time** (`Optional[datetime]`): When the task started, in RFC 3339 format.
    - **end_time** (`Optional[datetime]`): When the task ended, in RFC 3339 format.
    - **outputs** (`list[TESOutputFileLog]`): Information about all output files. Directory outputs are flattened into separate items.
    - **system_logs** (`Optional[list[str]]`): System logs are any logs the system decides are relevant, which are not tied directly to an Executor process. Content is implementation specific: format, size, etc.
    - **status** (`Optional[str]`): The status of the task.

    **Reference:** [https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask](https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask)
    """

    logs: list[TESExecutorLog]
    metadata: Optional[dict[str, str]]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    outputs: list[TESOutputFileLog]
    system_logs: Optional[list[str]]

    @validator("start_time", "end_time", pre=True, always=True)
    def validate_datetime(cls, value):
        return convert_to_iso8601(value)


class TESData(BaseModel):
    """
    Represents a TES task.

    **Attributes:**

    - **id** (`str`): Task identifier assigned by the server.
    - **name** (`Optional[str]`): User-provided task name.
    - **description** (`Optional[str]`): Optional user-provided description of task for documentation purposes.
    - **creation_time** (`Optional[str]`): The time the task was created.
    - **state** (`Optional[str]`): Task state as defined by the server
    - **inputs** (`list[TESInput]`): Input files that will be used by the task.
    - **outputs** (`list[TESOutput]`): Output files that will be uploaded from the executor container to long-term storage.
    - **executors** (`list[Executor]`): An array of executors to be run.
    - **resources** (`Optional[TESResources]`): The resources required by the TES task.
    - **volumes** (`Optional[list[str]]`): Volumes are directories which may be used to share data between Executors..
    - **logs** (`Optional[list[TESLogs]]`): Task logging information
    - **tags** (`Optional[[str, str]]`): A key-value map of arbitrary tags.

    **Reference:** [https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask](https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask)
    """

    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    creation_time: Optional[datetime] = None
    state: Optional[TESState] = TESState.UNKNOWN
    inputs: list[TESInput]
    outputs: list[TESOutput]
    executors: list[TESExecutor]
    resources: Optional[TESResources] = None
    volumes: Optional[list[str]] = None
    logs: Optional[list[TESTaskLog]] = None
    tags: Optional[dict[str, str]] = None
