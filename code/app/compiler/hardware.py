from dataclasses import dataclass, field

@dataclass
class HardwareProfile:
    name: str
    num_qubits: int
    coupling_map: list[tuple[int,int]]
    basis_gates: list[str] = field(default_factory=lambda:["I","H","X","Y","Z","S","T","RX","RY","RZ","CX","CZ","SWAP"])
    gate_error: dict[str,float] = field(default_factory=lambda:{"1q":0.001,"2q":0.01})
    readout_error: float = 0.015
    provider: str = "simulator"
    def validate(self):
        if self.num_qubits < 1: raise ValueError("Hardware needs at least one qubit")
        for a,b in self.coupling_map:
            if a==b or min(a,b)<0 or max(a,b)>=self.num_qubits: raise ValueError("Invalid coupling edge")
        return self
    def to_dict(self):
        return {"name":self.name,"num_qubits":self.num_qubits,"coupling_map":[list(e) for e in self.coupling_map],
                "basis_gates":self.basis_gates,"gate_error":self.gate_error,"readout_error":self.readout_error,"provider":self.provider}
    @classmethod
    def from_dict(cls,d):
        return cls(d["name"],int(d["num_qubits"]),[tuple(x) for x in d.get("coupling_map",[])],
                   d.get("basis_gates",["I","H","X","Y","Z","S","T","RX","RY","RZ","CX","CZ","SWAP"]),
                   d.get("gate_error",{"1q":.001,"2q":.01}),float(d.get("readout_error",.015)),d.get("provider","custom")).validate()

def sample_profiles():
    return [HardwareProfile("line-5",5,[(0,1),(1,2),(2,3),(3,4)]),
            HardwareProfile("fully-connected-5",5,[(i,j) for i in range(5) for j in range(i+1,5)],
                            gate_error={"1q":.001,"2q":.006},readout_error=.01)]
