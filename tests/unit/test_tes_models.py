"""Unit tests for the TES models."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from crategen.models.tes_models import (
    TESData,
    TESExecutor,
    TESFileType,
    TESInput,
    TESOutput,
    TESResources,
    TESState,
)

EXPECTED_CPU_CORES = 2
EXPECTED_RAM_GB = 4.0
EXPECTED_DISK_GB = 10.0
EXPECTED_PREEMPTIBLE = False

def test_tes_input_with_url():
    """Test TESInput model with a valid URL and absolute path."""
    input_data = TESInput(
        name="Test Input",
        description="An example input file.",
        url="https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/README.md",
        path="/data/input/README.md",
        type=TESFileType.FILE,
    )
    assert input_data.url == "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/README.md"
    assert input_data.path == "/data/input/README.md"
    assert input_data.type == TESFileType.FILE


def test_tes_input_with_content():
    """Test TESInput model with inline content instead of a URL."""
    input_data = TESInput(
        name="Inline Input",
        description="An input with inline content.",
        content="Sample data content.",
        path="/data/input/inline.txt",
        type=TESFileType.FILE,
    )
    assert input_data.content == "Sample data content."
    assert input_data.url is None
    assert input_data.path == "/data/input/inline.txt"


def test_tes_input_missing_url_and_content():
    """Test TESInput model when neither URL nor content is provided."""
    with pytest.raises(ValidationError) as exc_info:
        TESInput(
            name="Invalid Input",
            description="An input missing both URL and content.",
            path="/data/input/missing.txt",
            type=TESFileType.FILE,
        )
    assert "The 'url' attribute is required when the 'content' attribute is empty" in str(exc_info.value)


def test_tes_input_with_relative_path():
    """Test TESInput model with a relative path (should raise ValidationError)."""
    with pytest.raises(ValidationError) as exc_info:
        TESInput(
            name="Relative Path Input",
            description="An input with a relative path.",
            url="https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/README.md",
            path="data/input/README.md",
            type=TESFileType.FILE,
        )
    assert "The 'path' attribute must contain an absolute path." in str(exc_info.value)


def test_tes_input_content_and_url_conflict():
    """Test TESInput model when both content and URL are provided (URL should be ignored)."""
    input_data = TESInput(
        name="Input with Content and URL",
        description="Input with both content and URL.",
        url="https://example.com/should_be_ignored.txt",
        content="This content should override the URL.",
        path="/data/input/content.txt",
        type=TESFileType.FILE,
    )
    assert input_data.content == "This content should override the URL."
    assert input_data.url is None  # URL should be set to None


def test_tes_output_valid():
    """Test TESOutput model with valid data."""
    output_data = TESOutput(
        name="Test Output",
        description="An example output file.",
        url="https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/LICENSE",
        path="/data/output/LICENSE",
        type=TESFileType.FILE,
    )
    assert output_data.url == "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/LICENSE"
    assert output_data.path == "/data/output/LICENSE"
    assert output_data.type == TESFileType.FILE


def test_tes_output_with_relative_path():
    """Test TESOutput model with a relative path (should raise ValidationError)."""
    with pytest.raises(ValidationError) as exc_info:
        TESOutput(
            name="Relative Path Output",
            description="An output with a relative path.",
            url="https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/LICENSE",
            path="data/output/LICENSE",
            type=TESFileType.FILE,
        )
    assert "The 'path' attribute must contain an absolute path." in str(exc_info.value)


def test_tes_executor_valid():
    """Test TESExecutor model with valid data."""
    executor = TESExecutor(
        image="python:3.8-slim",
        command=["python", "script.py"],
        workdir="/app",
        stdout="/logs/stdout.log",
        stderr="/logs/stderr.log",
        stdin="/input/input.txt",
        env={"ENV_VAR": "value"},
    )
    assert executor.image == "python:3.8-slim"
    assert executor.command == ["python", "script.py"]
    assert executor.workdir == "/app"
    assert executor.stdout == "/logs/stdout.log"
    assert executor.stderr == "/logs/stderr.log"
    assert executor.stdin == "/input/input.txt"
    assert executor.env == {"ENV_VAR": "value"}


def test_tes_executor_with_relative_stdin():
    """Test TESExecutor model with a relative stdin path (should raise ValidationError)."""
    with pytest.raises(ValidationError) as exc_info:
        TESExecutor(
            image="python:3.8-slim",
            command=["python", "script.py"],
            stdin="input.txt",
        )
    assert "The 'stdin' attribute must contain an absolute path." in str(exc_info.value)


def test_tes_data_valid():
    """Test TESData model with valid data."""
    tes_data = TESData(
        id="task-123",
        name="Test Task",
        description="An example TES task.",
        creation_time=datetime.utcnow().replace(tzinfo=timezone.utc),
        state=TESState.QUEUED,
        inputs=[
            TESInput(
                name="Test Input",
                description="An example input file.",
                url="https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/README.md",
                path="/data/input/README.md",
                type=TESFileType.FILE,
            )
        ],
        outputs=[
            TESOutput(
                name="Test Output",
                description="An example output file.",
                url="https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/LICENSE",
                path="/data/output/LICENSE",
                type=TESFileType.FILE,
            )
        ],
        executors=[
            TESExecutor(
                image="python:3.8-slim",
                command=["python", "script.py"],
            )
        ],
        resources=TESResources(
            cpu_cores=EXPECTED_CPU_CORES,
            ram_gb=EXPECTED_RAM_GB,
            disk_gb=EXPECTED_DISK_GB,
            preemptible=EXPECTED_PREEMPTIBLE,
        ),
        volumes=["/data"],
        tags={"project": "CrateGen"},
    )
    assert tes_data.id == "task-123"
    assert tes_data.inputs[0].url == "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/README.md"
    assert tes_data.outputs[0].path == "/data/output/LICENSE"
    assert tes_data.executors[0].image == "python:3.8-slim"
    assert tes_data.resources.cpu_cores == EXPECTED_CPU_CORES
    assert tes_data.volumes == ["/data"]
    assert tes_data.tags == {"project": "CrateGen"}


def test_tes_data_missing_required_fields():
    """Test TESData model missing required fields (should raise ValidationError)."""
    with pytest.raises(ValidationError) as exc_info:
        TESData(
            inputs=[],
            outputs=[],
            executors=[],
        )
    assert "field required" in str(exc_info.value)
