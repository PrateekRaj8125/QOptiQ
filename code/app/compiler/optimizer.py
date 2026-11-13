from collections import deque
from math import pi
import time
from .ir import Circuit,Gate
from .metrics import calculate

SELF_INVERSE={"H","X","Y","Z","CX","CZ","SWAP"}
def optimize(c):
    out=[]
    for g in c.gates:
        if out and out[-1].name==g.name and out[-1].qubits==g.qubits and g.name in SELF_INVERSE:
            out.pop()
        elif out and g.name in {"RX","RY","RZ"} and out[-1].name==g.name and out[-1].qubits==g.qubits:
            angle=(out.pop().params[0]+g.params[0])%(2*pi)
            if abs(angle)>1e-10 and abs(angle-2*pi)>1e-10: out.append(Gate(g.name,list(g.qubits),[angle]))
        else: out.append(g)
    return Circuit(c.num_qubits,out,list(c.measurements),c.name,{**c.metadata,"optimizer":"qoptiq-classical"})

def route(c,h):
    if c.num_qubits>h.num_qubits: raise ValueError("Circuit requires more qubits than target hardware")
    adj={i:set() for i in range(h.num_qubits)}
    for a,b in h.coupling_map: adj[a].add(b); adj[b].add(a)
    out=[]
    for g in c.gates:
        if g.name in {"CX","CZ"}:
            a,b=g.qubits
            if b not in adj[a]:
                q=deque([(a,[a])]); seen={a}; path=None
                while q:
                    u,p=q.popleft()
                    if u==b: path=p; break
                    for v in adj[u]:
                        if v not in seen: seen.add(v); q.append((v,p+[v]))
                if not path: raise ValueError(f"No coupling path from {a} to {b}")
                for i in range(len(path)-2): out.append(Gate("SWAP",[path[i],path[i+1]]))
                out.append(Gate(g.name,[path[-2],path[-1]],list(g.params)))
            else: out.append(g)
        else: out.append(g)
    return Circuit(c.num_qubits,out,list(c.measurements),c.name,{**c.metadata,"routing":"shortest-path-baseline"})

def compile_circuit(c,h,weights=None):
    start=time.perf_counter()
    before=calculate(c,h)
    optimized=route(optimize(c),h)
    after=calculate(optimized,h,(time.perf_counter()-start)*1000)
    gains={}
    for k in ["gate_count","depth","two_qubit_gates","swap_count","estimated_error"]:
        gains[k+"_reduction_pct"]=round((before[k]-after[k])*100/before[k],2) if before[k] else 0
    w=weights or {"gate":.25,"depth":.25,"swap":.25,"error":.25}
    cost=w.get("gate",0)*after["gate_count"]+w.get("depth",0)*after["depth"]+w.get("swap",0)*after["swap_count"]+w.get("error",0)*100*after["estimated_error"]
    return {"original_circuit":c.to_dict(),"optimized_circuit":optimized.to_dict(),"before":before,"after":after,
            "improvements":gains,"weights":w,"cost":round(cost,6),
            "explanation":["Cancelled adjacent inverse gates and merged adjacent same-axis rotations where valid.",
                           "Inserted SWAP operations for non-adjacent two-qubit interactions using shortest paths."]}
