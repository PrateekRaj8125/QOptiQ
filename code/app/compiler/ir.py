from dataclasses import dataclass, field
from typing import Any
import re

SINGLE = {"I","H","X","Y","Z","S","T","RX","RY","RZ"}
DOUBLE = {"CX","CNOT","CZ","SWAP"}
SUPPORTED = SINGLE | DOUBLE

@dataclass
class Gate:
    name: str
    qubits: list[int]
    params: list[float] = field(default_factory=list)
    def __post_init__(self):
        self.name = self.name.upper()
        if self.name == "CNOT": self.name = "CX"

@dataclass
class Circuit:
    num_qubits: int
    gates: list[Gate]
    measurements: list[int] = field(default_factory=list)
    name: str = "circuit"
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self):
        if not 1 <= self.num_qubits <= 128:
            raise ValueError("num_qubits must be between 1 and 128")
        for i, g in enumerate(self.gates):
            if g.name not in SUPPORTED: raise ValueError(f"Unsupported gate: {g.name}")
            expected = 2 if g.name in DOUBLE else 1
            if len(g.qubits) != expected: raise ValueError(f"{g.name} expects {expected} qubits")
            if len(set(g.qubits)) != len(g.qubits): raise ValueError("A gate cannot target a qubit twice")
            if any(q < 0 or q >= self.num_qubits for q in g.qubits): raise ValueError("Invalid qubit index")
            if g.name in {"RX","RY","RZ"} and len(g.params) != 1: raise ValueError(f"{g.name} needs one angle")
        if any(q < 0 or q >= self.num_qubits for q in self.measurements):
            raise ValueError("Invalid measurement qubit")
        return self

    def to_dict(self):
        return {"num_qubits":self.num_qubits,"gates":[{"name":g.name,"qubits":g.qubits,"params":g.params} for g in self.gates],
                "measurements":self.measurements,"name":self.name,"metadata":self.metadata}

    @classmethod
    def from_dict(cls, d):
        return cls(int(d["num_qubits"]),[Gate(x["name"],list(x["qubits"]),list(x.get("params",[]))) for x in d.get("gates",[])],
                   list(d.get("measurements",[])),d.get("name","circuit"),d.get("metadata",{})).validate()

def parse_qasm2(text):
    text = re.sub(r"//.*?$","",text,flags=re.M)
    m = re.search(r"qreg\\s+\\w+\\[(\\d+)\\]\\s*;",text)
    if not m: raise ValueError("Expected one qreg declaration")
    n=int(m.group(1)); gates=[]; measurements=[]
    for stmt in text.split(";"):
        s=stmt.strip()
        if not s or s.startswith(("OPENQASM","include","qreg","creg","barrier")): continue
        if s.startswith("measure"):
            q=re.search(r"\\[(\\d+)\\]",s)
            if q: measurements.append(int(q.group(1)))
            continue
        m=re.fullmatch(r"([A-Za-z]+)(?:\\(([^)]*)\\))?\\s+(.+)",s)
        if not m: raise ValueError(f"Unsupported QASM statement: {s}")
        name,params,operands=m.groups()
        qs=[int(x) for x in re.findall(r"\\[(\\d+)\\]",operands)]
        ps=[float(x.strip()) for x in params.split(",")] if params else []
        gates.append(Gate(name,qs,ps))
    return Circuit(n,gates,sorted(set(measurements)),"qasm-import").validate()
