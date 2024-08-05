from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Dict

class Executor(BaseModel):
    image: str
    command: List[str]

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
    executors: List[Executor]
    inputs: List[TESInputs]
    outputs: List[TESOutputs]
    creation_time: str
    logs: List[TESLogs]

    class Config:
        extra = "forbid"

class WESRunLog(BaseModel):
    name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    cmd: Optional[List[str]] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None

class WESOutputs(BaseModel):
    location: str
    name: str

class WESRequest(BaseModel):
    workflow_params: Dict[str, str]
    workflow_type: str
    workflow_type_version: str
    tags: Optional[Dict[str, str]] = None

class WESData(BaseModel):
    run_id: str
    request: WESRequest
    state: str
    run_log: WESRunLog
    task_logs: Optional[List[WESRunLog]] = None
    outputs: List[WESOutputs]

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
    object: List[WRROCInputs]
    result: List[WRROCOutputs]
    startTime: Optional[str] = None
    endTime: Optional[str] = None

    class Config:
        extra = "forbid"

class WRROCDataWES(BaseModel):
    id: str
    name: str
    status: str
    result: List[WRROCOutputs]
    startTime: Optional[str] = None
    endTime: Optional[str] = None

    class Config:
        extra = "forbid"
