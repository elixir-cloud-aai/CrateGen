from pydantic import BaseModel, Field, validator,root_validator
from typing import List, Optional, Dict, Any

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

class WESRunLog(BaseModel):
    name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class WESOutputs(BaseModel):
    location: str
    name: str

class WESData(BaseModel):
    run_id: str
    run_log: WESRunLog
    state: str
    outputs: List[WESOutputs]

    @root_validator(pre=True)
    def check_unexpected_fields(cls, values):
        allowed_fields = {"run_id", "run_log", "state", "outputs"}
        unexpected = set(values.keys()) - allowed_fields
        if unexpected:
            raise ValueError(f"Unexpected fields: {unexpected}")
        return values

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

    @validator('id')
    def id_must_be_string(cls, value):
        if not isinstance(value, str):
            raise ValueError('Invalid id type')
        return value

    @validator('name')
    def name_must_be_string(cls, value):
        if not isinstance(value, str):
            raise ValueError('Invalid name type')
        return value

class WRROCDataWES(BaseModel):
    id: str
    name: str
    status: str
    result: List[WRROCOutputs]
    startTime: Optional[str] = None
    endTime: Optional[str] = None

    @root_validator(pre=True)
    def check_unexpected_fields(cls, values):
        allowed_fields = {"id", "name", "startTime", "endTime", "status", "result"}
        unexpected = set(values.keys()) - allowed_fields
        if unexpected:
            raise ValueError(f"Unexpected fields: {unexpected}")
        return values
