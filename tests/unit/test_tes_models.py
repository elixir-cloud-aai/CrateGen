"""Unit tests for the TES models."""


import pytest
from pydantic import ValidationError

from crategen.models.tes_models import (
    TESData,
    TESExecutor,
    TESFileType,
    TESInput,
    TESOutput,
    TESResources,
)

EXPECTED_CPU_CORES = 2
EXPECTED_RAM_GB = 4.0
EXPECTED_DISK_GB = 10.0
EXPECTED_PREEMPTIBLE = False

def test_tes_executor_minimal():
    """Test TESExecutor model with minimal required fields."""
    executor = TESExecutor(
        image="python:3.8-slim",
        command=["python", "script.py"]
    )
    assert executor.image == "python:3.8-slim"
    assert executor.command == ["python", "script.py"]
    assert executor.workdir is None
    assert executor.stdout is None
    assert executor.stderr is None
    assert executor.stdin is None
    assert executor.env is None
    assert executor.ignore_error is False  # Since default is False

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

def test_tes_data_with_inputs():
    """Test TESData model with inputs only."""
    tes_data = TESData(
        id="task-123",
        executors=[
            TESExecutor(
                image="python:3.8-slim",
                command=["python", "script.py"]
            )
        ],
        inputs=[
            TESInput(
                name="Test Input",
                url="https://example.com/input.txt",
                path="/data/input/input.txt"
            )
        ]
    )
    assert tes_data.inputs is not None
    assert len(tes_data.inputs) == 1


def test_tes_data_with_outputs():
    """Test TESData model with outputs only."""
    tes_data = TESData(
        id="task-123",
        executors=[
            TESExecutor(
                image="python:3.8-slim",
                command=["python", "script.py"]
            )
        ],
        outputs=[
            TESOutput(
                name="Test Output",
                url="https://example.com/output.txt",
                path="/data/output/output.txt"
            )
        ]
    )
    assert tes_data.outputs is not None
    assert len(tes_data.outputs) == 1

def test_tes_data_with_resources():
    """Test TESData model with resources."""
    tes_data = TESData(
        id="task-123",
        executors=[
            TESExecutor(
                image="python:3.8-slim",
                command=["python", "script.py"]
            )
        ],
        resources=TESResources(
            cpu_cores=EXPECTED_CPU_CORES,
            ram_gb=EXPECTED_RAM_GB
        )
    )
    assert tes_data.resources.cpu_cores == EXPECTED_CPU_CORES
    assert tes_data.resources.ram_gb == EXPECTED_RAM_GB

def test_tes_data_missing_required_fields():
    """Test TESData model missing required fields (should raise ValidationError)."""
    with pytest.raises(ValidationError) as exc_info:
        TESData()
    errors = exc_info.value.errors()
    required_fields = [error['loc'][0] for error in errors if error['type'] == 'value_error.missing']
    assert 'executors' in required_fields

def test_tes_output_with_wildcards_missing_path_prefix():
    """Test TESOutput with wildcards in 'path' without 'path_prefix'."""
    with pytest.raises(ValidationError) as exc_info:
        TESOutput(
            name="Wildcard Output",
            url="https://example.com/output/*",
            path="/data/output/*",
        )
    assert "When 'path' contains wildcards, 'path_prefix' is required." in str(exc_info.value)

def test_tes_output_with_wildcards_and_path_prefix():
    """Test TESOutput with wildcards in 'path' and provided 'path_prefix'."""
    output_data = TESOutput(
        name="Wildcard Output",
        url="https://example.com/output/*",
        path="/data/output/*",
        path_prefix="/data/output",
    )
    assert output_data.path_prefix == "/data/output"

def test_tes_executor_with_ignore_error():
    """Test TESExecutor model with 'ignore_error' field set to True."""
    executor = TESExecutor(
        image="python:3.8-slim",
        command=["python", "script.py"],
        ignore_error=True
    )
    assert executor.ignore_error is True

