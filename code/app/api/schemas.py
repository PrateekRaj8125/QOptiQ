from pydantic import BaseModel,Field
from typing import Any,Literal
class GateIn(BaseModel):
    name:str; qubits:list[int]; params:list[float]=Field(default_factory=list)
class CircuitIn(BaseModel):
    num_qubits:int=Field(ge=1,le=128)
    gates:list[GateIn]
    measurements:list[int]=Field(default_factory=list)
    name:str="circuit"
    metadata:dict[str,Any]=Field(default_factory=dict)
class OptimizeRequest(BaseModel):
    circuit:CircuitIn
    hardware:dict[str,Any]|None=None
    objective:Literal["balanced","minimum_gates","minimum_depth","minimum_error"]="balanced"
    weights:dict[str,float]|None=None
class ExecuteRequest(BaseModel):
    circuit:CircuitIn
    shots:int=Field(default=1024,ge=1,le=1000000)
    backend:str="simulator"
