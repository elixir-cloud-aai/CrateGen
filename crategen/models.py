from pydantic import BaseModel
from typing import Optional

class Executor(BaseModel):
    image: str
    command: list[str]

class TESInputs(BaseModel):
    url: str
    path: str

class TESOutputs(BaseModel):
    url: str
    path: str

class TESLogs(BaseModel):
    end_time: Optional[str] = None

class TESData(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    executors: list[Executor]
    inputs: list[TESInputs]
    outputs: list[TESOutputs]
    creation_time: str
    logs: list[TESLogs]

    class Config:
        extra = "forbid"

class WESRunLog(BaseModel):
    name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    cmd: Optional[list[str]] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None

class WESOutputs(BaseModel):
    location: str
    name: str

class WESRequest(BaseModel):
    workflow_params: dict[str, str]
    workflow_type: str
    workflow_type_version: str
    tags: Optional[dict[str, str]] = None

class WESData(BaseModel):
    run_id: str
    request: WESRequest
    state: str
    run_log: WESRunLog
    task_logs: Optional[list[WESRunLog]] = None
    outputs: list[WESOutputs]

    class Config:
        extra = "forbid"

class WRROCInputs(BaseModel):
    id: str
    name: str

class WRROCOutputs(BaseModel):
    id: str
    name: str

class WRROCData(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    instrument: Optional[str] = None
    object: list[WRROCInputs]
    result: list[WRROCOutputs]
    startTime: Optional[str] = None
    endTime: Optional[str] = None

    class Config:
        extra = "forbid"

class WRROCDataTES(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    instrument: Optional[str] = None
    object: list[WRROCInputs]
    result: list[WRROCOutputs]
    startTime: Optional[str] = None
    endTime: Optional[str] = None

    class Config:
        extra = "forbid"

class WRROCDataWES(BaseModel):
    id: str
    name: str
    status: str
    result: list[WRROCOutputs]
    startTime: Optional[str] = None
    endTime: Optional[str] = None

    class Config:
        extra = "forbid"
