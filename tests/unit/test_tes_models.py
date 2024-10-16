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
    "s3://my-bucket/data/file.txt",
]

invalid_paths = [
    "str",
    "./random_path",
    "..some_path",
]

test_url = "https://raw.githubusercontent.com/elixir-cloud-aai/CrateGen/refs/heads/main/README.md"


class TestTESExecutorLog:
    """Test suite for the TESExecutor model validators."""

    def test_validate_datetime_valid(self):
        """Test that datetime validator accepts correct datetime strings."""
        for valid_datetime in valid_datetime_strings:
            # Create a TESExecutorLog object (we're just interested in the validator)
            log_entry = TESExecutorLog(
                start_time=valid_datetime, end_time=valid_datetime, exit_code=0
            )
            assert bool(log_entry.start_time)
            assert bool(log_entry.end_time)

    def test_validate_datetime_invalid(self):
        """Test that datetime validator rejects correct datetime strings."""
        for invalid_datetime in invalid_datetime_strings:
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

    def test_validate_stdin_stdout_valid(self):
        """Test that validator accepts valid paths"""
        for path in valid_paths:
            executor = TESExecutor(
                image="image", command=["commands"], stdin=path, stdout=path
            )

            assert bool(executor)

    def test_validate_stdin_stdout_invalid(self):
        """Test that validator rejects invalid paths"""
        for path in invalid_paths:
            with pytest.raises(ValueError) as exc_info:
                TESExecutor(image="image", command=["commands"], stdin=path, stdout="/")

            assert "The 'stdin' property must be an absolute path" in str(
                exc_info.value
            )

            with pytest.raises(ValueError) as exc_info:
                TESExecutor(image="image", command=["commands"], stdin="/", stdout=path)

            assert "The 'stdout' property must be an absolute path" in str(
                exc_info.value
            )


class TestTESTInput:
    """Test suite for the TESData model validators."""

    def test_validate_path_valid(self):
        """Test path accepts absolute paths."""
        for valid_path in valid_paths:
            input_data = TESInput(
                url=test_url,
                path=valid_path,
            )

            assert bool(input_data.path)

    def test_validate_path_invalid(self):
        """Test path rejects non-absolute paths."""
        for invalid_path in invalid_paths:
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

    def test_path_valid(self):
        """Test that validator accepts valid paths"""
        for valid_path in valid_paths:
            tes_output = TESOutput(url=test_url, path=valid_path)

            assert bool(tes_output)

    def test_path_invalid(self):
        """Test that validator rejects invalid paths"""
        for invalid_path in invalid_paths:
            with pytest.raises(ValueError) as exc_info:
                TESOutput(url=test_url, path=invalid_path)

            assert "The 'path' property must be an absolute path" in str(exc_info.value)


class TestTESTaskLog:
    """Test suite for TESTaskLog model validators."""

    tes_output_file_log = TESOutputFileLog(url=test_url, path="/", size_bytes="10gb")
    tes_executor_log = TESExecutorLog(exit_code=0)

    def test_validate_datetime_valid(self):
        """Test that the validator accepts valid paths"""
        for time in valid_datetime_strings:
            tes_task_log = TESTaskLog(
                outputs=[self.tes_output_file_log],
                logs=[self.tes_executor_log],
                start_time=time,
                end_time=time,
            )

            assert bool(tes_task_log.start_time)

    def test_validate_datetime_invalid(self):
        """Test that the validator rejects valid paths"""
        for time in invalid_datetime_strings:
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

    def test_validate_datetime_valid(self):
        """Test that datetime validator accepts correct datetime strings."""
        for valid_datetime in valid_datetime_strings:
            data = TESData(
                id="id", creation_time=valid_datetime, executors=[self.executor]
            )
            assert bool(data.creation_time)

    def test_validate_datettime_invalid(self):
        """Test that datetime validator rejects incorrect datetime strings."""
        for invalid_datetime in invalid_datetime_strings:
            with pytest.raises(ValueError) as exc_info:
                TESData(
                    id="id", creation_time=invalid_datetime, executors=[self.executor]
                )

            assert "The 'creation_time' property must be in the rfc3339 format" in str(
                exc_info.value
            )
