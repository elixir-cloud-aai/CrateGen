"""TES UNIT TESTS"""

import pytest

from crategen.models.tes_models import (
    TESData,
    TESExecutor,
    TESExecutorLog,
    TESInput,
    TESOutput,
    TESOutputFileLog,
    TESTaskLog,
)

valid_datetime_strings = [
    "2020-10-02T16:00:00.000Z",
    "2024-10-15T18:14:34+00:00",
    "2024-10-15T18:14:34.948996+00:00",
    "2024-10-15T19:01:06.872464+00:00",
]

invalid_datetime_strings = [
    "2020-10-02 16:00:00",  # Missing 'T' separator
    "2020-10-02T16:00:00",  # Missing timezone or fractional seconds
    "20201002T160000Z",  # Missing separators
    "2020-10-02T16:00:00.000+0200",  # Invalid timezone format
    "2020-10-02T16:00:00.000 GMT",  # Invalid timezone format
    "02-10-2020T16:00:00.000Z",  # Incorrect date order
]

valid_paths = [
    "/",
    "/random_path",
    r"C:\Users\user\Document.pdf",
    r"D:\Projects\my_website\index.html",
    r"\\server\share",
    # "s3://my-bucket/data/file.txt",
]

invalid_paths = [
    "str",
    "./random_path",
    "..some_path",
]

test_url = "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/README.md"


class TestTESExecutorLog:
    """Test suite for the TESExecutor model validators."""

    @pytest.mark.parametrize(
        "valid_datetime",
        valid_datetime_strings,
    )
    def test_validate_datetime_valid(self, valid_datetime):
        """Test that datetime validator accepts correct datetime strings."""
        log_entry = TESExecutorLog(
            start_time=valid_datetime, end_time=valid_datetime, exit_code=0
        )
        assert bool(log_entry.start_time)
        assert bool(log_entry.end_time)

    @pytest.mark.parametrize(
        "invalid_datetime",
        invalid_datetime_strings,
    )
    def test_validate_datetime_invalid(self, invalid_datetime):
        """Test that datetime validator rejects correct datetime strings."""

        with pytest.raises(ValueError) as exc_info:
            TESExecutorLog(
                start_time=invalid_datetime,
                end_time="2020-10-02T16:00:00.000Z",
                exit_code=0,
            )

        assert "The 'start_time' property must be in the rfc3339 format" in str(
            exc_info.value
        )

        with pytest.raises(ValueError) as exc_info:
            TESExecutorLog(
                start_time="2020-10-02T16:00:00.000Z",
                end_time=invalid_datetime,
                exit_code=0,
            )

        # check the error message
        assert "The 'end_time' property must be in the rfc3339 format" in str(
            exc_info.value
        )


class TestTESExecutor:
    """Test suite for the TESExecutorLog model validators."""

    @pytest.mark.parametrize(
        "path",
        valid_paths,
    )
    def test_validate_stdin_stdout_valid(self, path):
        """Test that validator accepts valid paths"""
        executor = TESExecutor(
            image="image", command=["commands"], stdin=path, stdout=path
        )

        assert bool(executor)

    @pytest.mark.parametrize(
        "path",
        invalid_paths,
    )
    def test_validate_stdin_stdout_invalid(self, path):
        """Test that validator rejects invalid paths"""
        with pytest.raises(ValueError) as exc_info:
            TESExecutor(image="image", command=["commands"], stdin=path, stdout="/")

        assert "The 'stdin' property must be an absolute path" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            TESExecutor(image="image", command=["commands"], stdin="/", stdout=path)

        assert "The 'stdout' property must be an absolute path" in str(exc_info.value)


class TestTESTInput:
    """Test suite for the TESData model validators."""

    @pytest.mark.parametrize(
        "valid_path",
        valid_paths,
    )
    def test_validate_path_valid(self, valid_path):
        """Test path accepts absolute paths."""
        input_data = TESInput(
            url=test_url,
            path=valid_path,
        )

        assert bool(input_data.path)

    @pytest.mark.parametrize("invalid_path", invalid_paths)
    def test_validate_path_invalid(self, invalid_path):
        """Test path rejects non-absolute paths."""
        with pytest.raises(ValueError) as exc_info:
            TESInput(
                url=test_url,
                path=invalid_path,
            )

        assert "The 'path' property must be an absolute path" in str(exc_info.value)

    def test_validate_no_content_or_url(self):
        """An error should be thrown if both content and url are not set"""
        with pytest.raises(ValueError) as exc_info:
            TESInput(path="/")

        assert "Either the 'url' or 'content' properties must be set" in str(
            exc_info.value
        )

    def test_validate_content_or_url(self):
        """No error if either content or url are set"""
        tes_input = TESInput(path="/", url=test_url)

        assert bool(tes_input.url)
        assert not bool(tes_input.content)

        tes_input = TESInput(path="/", content="content")

        assert not bool(tes_input.url)
        assert bool(tes_input.content)

    def test_validate_not_content_and_url(self):
        """If both content and url are set, url should be automatically unset"""
        tes_input = TESInput(path="/", url=test_url, content="content")

        assert not bool(tes_input.url)
        assert bool(tes_input.content)


class TestTESOutput:
    """Test suite for TESOutput model validators."""

    @pytest.mark.parametrize("valid_path", valid_paths)
    def test_path_valid(self, valid_path):
        """Test that validator accepts valid paths"""
        tes_output = TESOutput(url=test_url, path=valid_path)

        assert bool(tes_output)

    @pytest.mark.parametrize("invalid_path", invalid_paths)
    def test_path_invalid(self, invalid_path):
        """Test that validator rejects invalid paths"""
        with pytest.raises(ValueError) as exc_info:
            TESOutput(url=test_url, path=invalid_path)

        assert "The 'path' property must be an absolute path" in str(exc_info.value)

    @pytest.mark.parametrize(
        "path,path_prefix",
        [
            ("/path/to/file.txt", None),
            ("/path/to/directory", None),
            ("/path/to/files*.txt", "/path/to"),
            ("/path/to/data???.csv", "/path/to"),
        ],
    )
    def test_validate_is_path_prefix_necessary_valid(self, path, path_prefix):
        """Test that validator accepts valid paths and path prefixes."""
        tes_output = TESOutput(
            url="https://example.com", path=path, path_prefix=path_prefix
        )
        assert bool(tes_output)

    @pytest.mark.parametrize(
        "path,path_prefix",
        [
            ("/path/to/files*.txt", None),
            ("/path/to/data???.csv", ""),
        ],
    )
    def test_validate_is_path_prefix_necessary_invalid(self, path, path_prefix):
        """Test that validator rejects invalid paths and path prefixes."""
        with pytest.raises(ValueError) as exc_info:
            TESOutput(url="https://example.com", path=path, path_prefix=path_prefix)

        assert (
            "The 'path_prefix' property is required when the 'path' property contains a wildcard"
            in str(exc_info.value)
        )


class TestTESTaskLog:
    """Test suite for TESTaskLog model validators."""

    tes_output_file_log = TESOutputFileLog(url=test_url, path="/", size_bytes="10gb")
    tes_executor_log = TESExecutorLog(exit_code=0)

    @pytest.mark.parametrize("time", valid_datetime_strings)
    def test_validate_datetime_valid(self, time):
        """Test that the validator accepts valid paths"""
        tes_task_log = TESTaskLog(
            outputs=[self.tes_output_file_log],
            logs=[self.tes_executor_log],
            start_time=time,
            end_time=time,
        )

        assert bool(tes_task_log.start_time)

    @pytest.mark.parametrize("time", invalid_datetime_strings)
    def test_validate_datetime_invalid(self, time):
        """Test that the validator rejects valid paths"""
        with pytest.raises(ValueError) as exc_info:
            TESTaskLog(
                outputs=[self.tes_output_file_log],
                logs=[self.tes_executor_log],
                start_time="2020-10-02T16:00:00.000Z",
                end_time=time,
            )

        assert "The 'end_time' property must be in the rfc3339 format" in str(
            exc_info.value
        )

        with pytest.raises(ValueError) as exc_info:
            TESTaskLog(
                outputs=[self.tes_output_file_log],
                logs=[self.tes_executor_log],
                start_time=time,
                end_time="2020-10-02T16:00:00.000Z",
            )

        assert "The 'start_time' property must be in the rfc3339 format" in str(
            exc_info.value
        )


class TestTESData:
    """Test suite for the TESData model."""

    executor = TESExecutor(image="image", command=["commands"], stdin="/", stdout="/")

    @pytest.mark.parametrize("valid_datetime", valid_datetime_strings)
    def test_validate_datetime_valid(self, valid_datetime):
        """Test that datetime validator accepts correct datetime strings."""
        data = TESData(id="id", creation_time=valid_datetime, executors=[self.executor])
        assert bool(data.creation_time)

    @pytest.mark.parametrize("invalid_datetime", invalid_datetime_strings)
    def test_validate_datetime_invalid(self, invalid_datetime):
        """Test that datetime validator rejects incorrect datetime strings."""
        with pytest.raises(ValueError) as exc_info:
            TESData(id="id", creation_time=invalid_datetime, executors=[self.executor])

        assert "The 'creation_time' property must be in the rfc3339 format" in str(
            exc_info.value
        )
