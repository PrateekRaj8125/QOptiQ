from app.compiler.ir import Circuit,Gate
from app.compiler.hardware import sample_profiles
from app.compiler.optimizer import compile_circuit
from app.compiler.metrics import calculate

def test_metrics():
    c=Circuit(2,[Gate("H",[0]),Gate("CX",[0,1])])
    m=calculate(c)
    assert m["gate_count"]==2 and m["two_qubit_gates"]==1

def test_optimization_and_routing():
    c=Circuit(3,[Gate("H",[0]),Gate("H",[0]),Gate("CX",[0,2])])
    result=compile_circuit(c,sample_profiles()[0])
    assert result["after"]["swap_count"]>=1
    assert result["after"]["gate_count"]>=1
