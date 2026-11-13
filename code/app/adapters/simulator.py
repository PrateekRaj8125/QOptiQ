import uuid, math
import numpy as np
from .base import QuantumBackend
from ..compiler.ir import Circuit
class SimulatorBackend(QuantumBackend):
    name="local-statevector"
    def __init__(self): self.jobs={}
    def _simulate(self,c,shots):
        if c.num_qubits>20: raise ValueError("Local statevector simulator is limited to 20 qubits")
        n=c.num_qubits; state=np.zeros(2**n,dtype=complex); state[0]=1
        def single(q,U):
            for i in range(2**n):
                if (i>>q)&1: continue
                j=i|(1<<q); a,b=state[i],state[j]
                state[i]=U[0,0]*a+U[0,1]*b; state[j]=U[1,0]*a+U[1,1]*b
        for g in c.gates:
            t=g.params[0] if g.params else 0
            matrices={"I":np.eye(2),"H":np.array([[1,1],[1,-1]])/math.sqrt(2),
                      "X":np.array([[0,1],[1,0]]),"Y":np.array([[0,-1j],[1j,0]]),
                      "Z":np.diag([1,-1]),"S":np.diag([1,1j]),"T":np.diag([1,np.exp(1j*math.pi/4)]),
                      "RX":np.array([[math.cos(t/2),-1j*math.sin(t/2)],[-1j*math.sin(t/2),math.cos(t/2)]]),
                      "RY":np.array([[math.cos(t/2),-math.sin(t/2)],[math.sin(t/2),math.cos(t/2)]]),
                      "RZ":np.diag([np.exp(-1j*t/2),np.exp(1j*t/2)])}
            if g.name in matrices: single(g.qubits[0],matrices[g.name])
            elif g.name=="CZ":
                for i in range(2**n):
                    if (i>>g.qubits[0]&1) and (i>>g.qubits[1]&1): state[i]*=-1
            elif g.name=="CX":
                a,b=g.qubits
                for i in range(2**n):
                    if (i>>a&1) and not (i>>b&1):
                        j=i|(1<<b); state[i],state[j]=state[j],state[i]
            elif g.name=="SWAP":
                a,b=g.qubits
                for i in range(2**n):
                    if ((i>>a)&1)!=((i>>b)&1):
                        j=i^(1<<a)^(1<<b)
                        if i<j: state[i],state[j]=state[j],state[i]
        probs=np.abs(state)**2
        samples=np.random.default_rng().choice(2**n,shots,p=probs/probs.sum())
        measured=c.measurements or list(range(n)); counts={}
        for v in samples:
            key="".join(str((int(v)>>q)&1) for q in reversed(measured))
            counts[key]=counts.get(key,0)+1
        return {"counts":counts,"shots":shots,"backend":self.name}
    def submit(self,circuit,shots=1024):
        c=Circuit.from_dict(circuit) if isinstance(circuit,dict) else circuit
        jid=str(uuid.uuid4())
        try: self.jobs[jid]={"status":"completed","result":self._simulate(c,shots)}
        except Exception as e: self.jobs[jid]={"status":"failed","error":str(e)}
        return jid
    def get_status(self,jid): return self.jobs.get(jid,{"status":"not_found"})["status"]
    def get_result(self,jid): return self.jobs.get(jid,{"status":"not_found"})
