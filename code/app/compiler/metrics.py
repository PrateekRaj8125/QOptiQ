from .ir import Circuit
TWO={"CX","CZ","SWAP"}
def depth(c):
    levels=[0]*c.num_qubits
    for g in c.gates:
        level=1+max(levels[q] for q in g.qubits)
        for q in g.qubits: levels[q]=level
    return max(levels,default=0)
def calculate(c,h=None,compile_time_ms=0):
    one=sum(len(g.qubits)==1 for g in c.gates)
    two=sum(g.name in TWO for g in c.gates)
    swaps=sum(g.name=="SWAP" for g in c.gates)
    e1=h.gate_error.get("1q",.001) if h else .001
    e2=h.gate_error.get("2q",.01) if h else .01
    er=h.readout_error if h else .015
    survival=(1-e1)**one*(1-e2)**two*(1-er)**len(c.measurements or range(c.num_qubits))
    return {"gate_count":len(c.gates),"one_qubit_gates":one,"two_qubit_gates":two,"depth":depth(c),
            "swap_count":swaps,"estimated_error":round(1-survival,6),"estimated_fidelity":round(survival,6),
            "compile_time_ms":round(compile_time_ms,3)}
