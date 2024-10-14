"""Each model in this module conforms to the corresponding TES model names as specified by the GA4GH schema (https://ga4gh.github.io/task-execution-schemas/docs/)."""

import os
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseModel, root_validator, validator

from ..converters.utils import convert_to_iso8601


class TESFileType(str, Enum):
    """Enumeration of TES file types.
    Attributes:
        FILE: Represents a file.
        DIRECTORY: Represents a directory.
    """
    FILE = "FILE"
    DIRECTORY = "DIRECTORY"


class TESState(str, Enum):
    """Enumeration of TES task states.

    Attributes:
        UNKNOWN: The task state is unknown.
        QUEUED: The task is queued.
        INITIALIZING: The task is initializing.
        RUNNING: The task is running.
        PAUSED: The task is paused.
        COMPLETE: The task is complete.
        EXECUTOR_ERROR: The task encountered an executor error.
        SYSTEM_ERROR: The task encountered a system error.
        CANCELED: The task was canceled.
        CANCELING: The task is being canceled.
        PREEMPTED: The task was preempted.
    """
    UNKNOWN = "UNKNOWN"
    QUEUED = "QUEUED"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETE = "COMPLETE"
    EXECUTOR_ERROR = "EXECUTOR_ERROR"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    CANCELED = "CANCELED"
    CANCELING = "CANCELING"
    PREEMPTED = "PREEMPTED" 


class TESOutputFileLog(BaseModel):
    """Information about all output files. Directory outputs are flattened into separate items.

    Attributes:

        url: URL of the file in storage.
        path: Path of the file inside the container. Must be an absolute path.
        size_bytes: Size of the file in bytes. Note, this is currently coded as a string because official JSON doesn't support int64 numbers.

    Reference: https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    url: str
    path: str
    size_bytes: str


class TESExecutorLog(BaseModel):
    """Logs for each executor.

    Attributes:

        start_time: Time the executor started, in RFC 3339 format.
        end_time: Time the executor ended, in RFC 3339 format.
        stdout: Stdout content.
        stderr: Stderr content.
        exit_code: The exit code of the executor.

    Reference: https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: int

    @validator("start_time", "end_time", pre=True, always=True)
    def validate_datetime(cls, value):
        """Convert start and end times to RFC 3339 format."""
        return convert_to_iso8601(value)


class TESExecutor(BaseModel):
    """An array of executors to be run.

    Attributes:
        image: Name of the container image.
        command: A sequence of program arguments to execute, where the first argument is the program to execute.
        workdir: The working directory that the command will be executed in.
        stdout: Path inside the container to a file where the executor's stdout will be written to. Must be an absolute path
        stderr: Path inside the container to a file where the executor's stderr will be written to. Must be an absolute path.
        stdin: Path inside the container to a file which will be piped to the executor's stdin. Must be an absolute path.
        env: Enviromental variables to set within the container
        ignore_error: If true, errors in this executor will be ignored.

    Reference: https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    image: str
    command: list[str]
    workdir: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    stdin: Optional[str] = None
    env: Optional[dict[str, str]] = None
    ignore_error: Optional[bool] = False

    @validator("stdin", "stdout")
    def validate_stdin_stdin(cls, value, field):
        """Ensure that 'stdin' and 'stdout' are absolute paths."""
        if value and not os.path.isabs(value):
            raise ValueError(f"The '{field.name}' attribute must contain an absolute path.")
        return value


class TESResources(BaseModel):
    """Represents the resources required by a TES task.

    Attributes:

        cpu_cores: Requested number of CPUs.
        preemptible: Define if the task is allowed to run on preemptible compute instances, for example, AWS Spot.
        ram_gb: The amount of RAM in GB required.
        disk_gb: The amount of disk space in GB required.
        zones: Request that the task be run in these compute zones.

    Reference: https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    cpu_cores: Optional[int] = None
    preemptible: Optional[bool] = None
    ram_gb: Optional[float] = None
    disk_gb: Optional[float] = None
    zones: Optional[list[str]] = None


class TESInput(BaseModel):
    """Input files that will be used by the task. Inputs will be downloaded and mounted into the executor container as defined by the task request document.

    Attributes:

        name: The name of the input file.
        description: A brief description of the input.
        url: The URL of the input file. Must be an absolute path
        path: TPath of the file inside the container. Must be an absolute path.
        type: The type of input ('FILE' or 'DIRECTORY'). Default is 'FILE'
        content: The content of the input file, if provided inline.

    Reference: https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[AnyUrl]
    path: str
    type: Optional[TESFileType] = None
    content: Optional[str] = None

    @root_validator()
    def validate_content_and_url(cls, values):
        """ If content is set url should be ignored.

            If content is not set then url should be present.
        """
        content_is_set = values.get("content") and values.get("content").strip()
        url_is_set = values.get("url") and values.get("url").strip()

        if content_is_set:
            values["url"] = None
        elif not url_is_set:
            raise ValueError(
                "The 'url' attribute is required when the 'content' attribute is empty"
            )
        return values

    @validator("path")
    def validate_path(cls, value):
        """Validate that the path is an absolute path."""
        if not os.path.isabs(value):
            raise ValueError("The 'path' attribute must contain an absolute path.")
        return value


class TESOutput(BaseModel):
    """Output files. Outputs will be uploaded from the executor container to long-term storage.

    Attributes:

        name: User-provided name of output file
        description: Optional users provided description field, can be used for documentation.
        url: URL for the file to be copied by the TES server after the task is complete
        path_prefix: The path prefix used when 'path' contains wildcards.
        path: Path of the file inside the container. Must be an absolute path.
        type: The type of output (e.g., FILE, DIRECTORY).

    Reference: https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask
    """

    name: Optional[str] = None
    description: Optional[str] = None
    url: AnyUrl
    path_prefix: Optional[str] = None
    path: str
    type: Optional[TESFileType] = None

    @validator("path")
    def validate_path(cls, value, values):
        """Ensure that 'path' is an absolute path and handle wildcards."""
        if not os.path.isabs(value):
            raise ValueError("The 'path' attribute must contain an absolute path.")
        if any(char in value for char in ['*', '?', '[', ']']) and not values.get("path_prefix"):
            raise ValueError("When 'path' contains wildcards, 'path_prefix' is required.")
        return value


class TESTaskLog(BaseModel):
    """Task logging information. Normally, this will contain only one entry, but in the case where a task fails and is retried, an entry will be appended to this list.

    Attributes:

        logs: Logs for each executor.
        metadata: Arbitrary logging metadata included by the implementation.
        start_time: When the task started, in RFC 3339 format.
        end_time: When the task ended, in RFC 3339 format.
        outputs: Information about all output files. Directory outputs are flattened into separate items.
        system_logs: System logs are any logs the system decides are relevant, which are not tied directly to an Executor process. Content is implementation specific: format, size, etc.
        ignore_error: If true, errors in this executor will be ignored.

    Reference: [https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask](https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask)
    """

    logs: list[TESExecutorLog]
    metadata: Optional[dict[str, str]]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    outputs: list[TESOutputFileLog]
    system_logs: Optional[list[str]]
    ignore_error: Optional[bool] = False

    @validator("start_time", "end_time", pre=True, always=True)
    def validate_datetime(cls, value):
        """Convert start and end times to RFC 3339 format."""
        return convert_to_iso8601(value)


class TESData(BaseModel):
    """Represents a TES task.

    Attributes:

        id: Task identifier assigned by the server.
        name: User-provided task name.
        description: Optional user-provided description of task for documentation purposes.
        creation_time: The time the task was created.
        state: Task state as defined by the server
        inputs: Input files that will be used by the task.
        outputs: Output files that will be uploaded from the executor container to long-term storage.
        executors: An array of executors to be run.
        resources: The resources required by the TES task.
        volumes: Volumes are directories which may be used to share data between Executors..
        logs: Task logging information
        tags: A key-value map of arbitrary tags.

    Reference: [https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask](https://ga4gh.github.io/task-execution-schemas/docs/#operation/GetTask)
    """

    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    creation_time: Optional[datetime] = None
    state: Optional[TESState] = TESState.UNKNOWN
    inputs: Optional[list[TESInput]] = None
    outputs: Optional[list[TESOutput]] = None
    executors: list[TESExecutor]
    resources: Optional[TESResources] = None
    volumes: Optional[list[str]] = None
    logs: Optional[list[TESTaskLog]] = None
    tags: Optional[dict[str, str]] = None
