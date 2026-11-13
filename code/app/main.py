import os,uuid
from fastapi import FastAPI,HTTPException,BackgroundTasks,Header,Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.schemas import CircuitIn,OptimizeRequest,ExecuteRequest
from .compiler.ir import Circuit,parse_qasm2
from .compiler.hardware import HardwareProfile,sample_profiles
from .compiler.optimizer import compile_circuit
from .compiler.metrics import calculate
from .ai.strategy import StrategySelector
from .adapters.simulator import SimulatorBackend
from .jobs.store import JobStore

app=FastAPI(title="QOptiQ Backend",version="0.1.0",description="AI-guided hardware-aware quantum circuit compilation backend")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()],allow_methods=["*"],allow_headers=["*"])
selector=StrategySelector(os.getenv("QOPTIQ_MODEL_PATH","models/strategy_model.joblib"))
simulator=SimulatorBackend(); jobs=JobStore()
def auth(x_api_key:str|None=Header(default=None)):
    key=os.getenv("QOPTIQ_API_KEY")
    if key and x_api_key!=key: raise HTTPException(401,"Invalid or missing X-API-Key")
def circuit(x):
    d=x.model_dump() if hasattr(x,"model_dump") else x.dict()
    return Circuit.from_dict(d)
def profile(d):
    return HardwareProfile.from_dict(d) if d else sample_profiles()[0]
@app.get("/")
def home(): return {"service":"QOptiQ Backend","docs":"/docs","health":"/health"}
@app.get("/health")
def health(): return {"status":"ok","service":"qoptiq-api","version":"0.2.0"}
@app.post("/circuits/validate",dependencies=[Depends(auth)])
def validate(c:CircuitIn):
    q=circuit(c); return {"valid":True,"circuit":q.to_dict(),"metrics":calculate(q)}
@app.post("/circuits/parse-qasm",dependencies=[Depends(auth)])
def qasm(body:dict):
    try:
        q=parse_qasm2(body.get("qasm","")); return {"valid":True,"circuit":q.to_dict(),"metrics":calculate(q)}
    except Exception as e: raise HTTPException(422,str(e))
@app.get("/hardware",dependencies=[Depends(auth)])
def hardware(): return {"items":[p.to_dict() for p in sample_profiles()]}
def run_optimization(req):
    c=circuit(req.circuit); h=profile(req.hardware)
    decision=selector.select(c,h,req.objective)
    result=compile_circuit(c,h,req.weights); result["ai_decision"]=decision; result["hardware"]=h.to_dict()
    return result
@app.post("/optimize",dependencies=[Depends(auth)])
def optimize(req:OptimizeRequest):
    try:return run_optimization(req)
    except ValueError as e:raise HTTPException(422,str(e))
@app.post("/transpile",dependencies=[Depends(auth)])
def transpile(req:OptimizeRequest): return optimize(req)
@app.post("/execute",dependencies=[Depends(auth)])
def execute(req:ExecuteRequest):
    if req.backend!="simulator": raise HTTPException(501,"Only local simulator is enabled in this release")
    jid=simulator.submit(circuit(req.circuit),req.shots); result=simulator.get_result(jid)
    if result["status"]=="failed": raise HTTPException(422,result["error"])
    return {"job_id":jid,**result}
def job_task(jid,payload):
    jobs.update(jid,"running")
    try:
        c=Circuit.from_dict(payload["circuit"]); h=profile(payload.get("hardware"))
        decision=selector.select(c,h,payload["objective"])
        result=compile_circuit(c,h,payload.get("weights")); result["ai_decision"]=decision; result["hardware"]=h.to_dict()
        jobs.update(jid,"completed",result)
    except Exception as e: jobs.update(jid,"failed",error=str(e))
@app.post("/jobs",status_code=202,dependencies=[Depends(auth)])
def submit(req:OptimizeRequest,bg:BackgroundTasks):
    jid=str(uuid.uuid4()); payload={"circuit":circuit(req.circuit).to_dict(),"hardware":req.hardware,"objective":req.objective,"weights":req.weights}
    jobs.create(jid,payload); bg.add_task(job_task,jid,payload)
    return {"job_id":jid,"status":"queued","status_url":f"/jobs/{jid}"}
@app.get("/jobs/{jid}",dependencies=[Depends(auth)])
def job(jid):
    result=jobs.get(jid)
    if not result:raise HTTPException(404,"Job not found")
    return result
@app.get("/results/{jid}",dependencies=[Depends(auth)])
def result(jid):
    item=jobs.get(jid)
    if not item:raise HTTPException(404,"Job not found")
    if item["status"]!="completed":raise HTTPException(202,{"status":item["status"],"error":item["error"]})
    return item["result"]
@app.get("/benchmarks",dependencies=[Depends(auth)])
def benchmarks():
    return {"baselines":["original","qoptiq-classical","qoptiq-ai"],"metrics":["gate_count","two_qubit_gates","depth","swap_count","estimated_error","estimated_fidelity","compile_time_ms"],
            "note":"Comparative Qiskit/PennyLane benchmark runners are future work."}
