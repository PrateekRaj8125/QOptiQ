from pathlib import Path
class StrategySelector:
    def __init__(self,path="models/strategy_model.joblib"):
        self.model=None
        p=Path(path)
        if p.exists():
            try:
                import joblib
                self.model=joblib.load(p)
            except Exception: pass
    def select(self,c,h,objective="balanced"):
        if objective not in {"balanced","minimum_gates","minimum_depth","minimum_error"}:
            raise ValueError("Unsupported optimization objective")
        if self.model:
            two=sum(g.name in {"CX","CZ"} for g in c.gates)
            x=[c.num_qubits,len(c.gates),two/max(1,len(c.gates)),
               len(h.coupling_map)/max(1,h.num_qubits),h.gate_error.get("2q",.01),h.readout_error]
            return {"strategy":str(self.model.predict([x])[0]),"method":"trained-model","confidence":None}
        if objective=="minimum_gates": s="aggressive"
        elif objective=="minimum_depth": s="depth"
        elif objective=="minimum_error": s="noise_aware"
        else:
            s="noise_aware" if h.gate_error.get("2q",.01)>.008 else "balanced"
        return {"strategy":s,"method":"heuristic-fallback","confidence":None,
                "reason":"Selected from requested objective and configured hardware error profile."}
