"""Models package for TES, WES, and WRROC.

This package contains Pydantic models that conform to the GA4GH schemas for Task Execution Services (TES),
Workflow Execution Services (WES), and WRROC. These models are used for data validation and type safety
throughout the CrateGen project.
"""

from .tes_models import (
    TESData,
    TESExecutor,
    TESExecutorLog,
    TESFileType,
    TESInput,
    TESOutput,
    TESOutputFileLog,
    TESResources,
    TESState,
    TESTaskLog,
)

__all__ = [
    "TESData",
    "TESInput",
    "TESOutput",
    "TESExecutor",
    "TESTaskLog",
    "TESResources",
    "TESExecutorLog",
    "TESOutputFileLog",
    "TESFileType",
    "TESState",
]
