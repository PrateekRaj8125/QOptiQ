import { useEffect, useMemo, useState } from 'react'
import { Activity, ArrowRight, Cpu, GitBranch, Play, RefreshCw, ShieldCheck, Zap } from 'lucide-react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_KEY = import.meta.env.VITE_API_KEY || ''
const sample = {
  num_qubits: 3,
  gates: [
    { name: 'H', qubits: [0], params: [] },
    { name: 'CX', qubits: [0, 2], params: [] },
    { name: 'RZ', qubits: [2], params: [1.570796] },
    { name: 'RZ', qubits: [2], params: [1.570796] },
    { name: 'CX', qubits: [0, 2], params: [] }
  ],
  measurements: [0, 1, 2],
  name: 'QOptiQ demo circuit'
}
type Hardware = {name:string; num_qubits:number; coupling_map:number[][]; provider:string; gate_error:Record<string,number>}
type Metrics = {gate_count:number; depth:number; two_qubit_gates:number; swap_count:number; estimated_error:number; estimated_fidelity:number; compile_time_ms:number}
type Result = {before:Metrics; after:Metrics; improvements:Record<string,number>; ai_decision:{strategy:string;method:string;reason?:string}; optimized_circuit:typeof sample; explanation:string[]; cost:number}
async function api(path:string, init?:RequestInit) {
  const response = await fetch(`${API}${path}`, { ...init, headers: {'Content-Type':'application/json', ...(API_KEY ? {'X-API-Key':API_KEY} : {}), ...(init?.headers || {})} })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || `API error ${response.status}`)
  return data
}
function Metric({label,value,unit=''}:{label:string;value:string|number;unit?:string}) {
  return <div className="metric"><span>{label}</span><strong>{value}{unit}</strong></div>
}
export default function App() {
  const [circuitText,setCircuitText] = useState(JSON.stringify(sample,null,2))
  const [hardware,setHardware] = useState<Hardware[]>([])
  const [selected,setSelected] = useState('')
  const [objective,setObjective] = useState('balanced')
  const [result,setResult] = useState<Result|null>(null)
  const [health,setHealth] = useState('Checking')
  const [busy,setBusy] = useState(false)
  const [error,setError] = useState('')
  const [tab,setTab] = useState('editor')
  const circuit = useMemo(() => { try { return JSON.parse(circuitText) } catch { return null } },[circuitText])
  useEffect(() => {
    api('/health').then(() => setHealth('Online')).catch(() => setHealth('Offline'))
    api('/hardware').then(d => {setHardware(d.items); if(d.items.length) setSelected(d.items[0].name)}).catch(e => setError(e.message))
  },[])
  async function optimize() {
    setBusy(true); setError(''); setResult(null)
    try {
      if(!circuit) throw new Error('Circuit JSON is not valid.')
      const h = hardware.find(x=>x.name===selected)
      if(!h) throw new Error('Select a target hardware profile.')
      const data = await api('/optimize',{method:'POST',body:JSON.stringify({circuit,hardware:h,objective})})
      setResult(data); setTab('results')
    } catch(e) {setError(e instanceof Error?e.message:'Unknown error')}
    finally {setBusy(false)}
  }
  async function execute() {
    setBusy(true); setError('')
    try {
      const data = await api('/execute',{method:'POST',body:JSON.stringify({circuit,backend:'simulator',shots:1024})})
      window.alert(`Simulation completed\\nShots: ${data.result?.shots}\\nCounts: ${JSON.stringify(data.result?.counts,null,2)}`)
    } catch(e) {setError(e instanceof Error?e.message:'Execution failed')}
    finally {setBusy(false)}
  }
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><GitBranch size={21}/></div><div><b>QOptiQ</b><small>QUANTUM COMPILER</small></div></div>
      <div className="side-label">WORKSPACE</div>
      {['editor','results'].map(t=><button key={t} className={`nav ${tab===t?'active':''}`} onClick={()=>setTab(t)}>{t==='editor'?<Cpu size={17}/>:<Activity size={17}/>} {t==='editor'?'Circuit Studio':'Optimization Results'}</button>)}
      <div className="side-bottom"><span className={`dot ${health==='Online'?'good':''}`}></span><span>API {health}</span><small>{API}</small></div>
    </aside>
    <main className="main">
      <header className="topbar"><div><span className="eyebrow">RESEARCH WORKSPACE / COMPILER</span><h1>Quantum Circuit Optimization</h1></div><div className="status"><span className={`dot ${health==='Online'?'good':''}`}></span>{health}</div></header>
      <section className="hero">
        <div><div className="eyebrow accent">AI-GUIDED · HARDWARE-AWARE · PROVIDER-INDEPENDENT</div><h2>Compile smarter.<br/><em>Explore the quantum frontier.</em></h2><p>Analyze circuit structure, select a hardware topology and compare the compiler's optimization output.</p></div>
        <div className="hero-art"><div className="orbit o1"></div><div className="orbit o2"></div><div className="core"><Zap size={30}/></div><span className="node n1"></span><span className="node n2"></span><span className="node n3"></span></div>
      </section>
      <div className="tabs"><button className={tab==='editor'?'selected':''} onClick={()=>setTab('editor')}>01 / Circuit input</button><button className={tab==='results'?'selected':''} onClick={()=>setTab('results')}>02 / Analysis output</button></div>
      {tab==='editor' ? <section className="workspace">
        <div className="panel editor-panel"><div className="panel-head"><div><span className="eyebrow">INPUT</span><h3>Circuit definition</h3></div><button className="subtle" onClick={()=>setCircuitText(JSON.stringify(sample,null,2))}><RefreshCw size={14}/> Load sample</button></div>
          <p className="hint">Edit the provider-neutral JSON circuit representation. Supported gates include H, X, Y, Z, RX, RY, RZ, CX, CZ and SWAP.</p>
          <textarea spellCheck={false} value={circuitText} onChange={e=>setCircuitText(e.target.value)} />
          <div className="editor-foot"><span className={circuit?'valid':'invalid'}>{circuit?'● Valid JSON':'● Invalid JSON'}</span><span>{circuit?.gates?.length ?? 0} gates · {circuit?.num_qubits ?? '—'} qubits</span></div>
        </div>
        <div className="panel config-panel"><div className="panel-head"><div><span className="eyebrow">CONFIGURATION</span><h3>Compile target</h3></div></div>
          <label>Hardware profile</label><select value={selected} onChange={e=>setSelected(e.target.value)}>{hardware.map(h=><option key={h.name} value={h.name}>{h.name} · {h.num_qubits} qubits</option>)}</select>
          {hardware.find(h=>h.name===selected)&&<div className="hardware-card"><div className="hardware-icon"><Cpu/></div><div><b>{selected}</b><small>{hardware.find(h=>h.name===selected)?.coupling_map.length} coupling edges · simulator profile</small></div></div>}
          <label>Optimization objective</label><select value={objective} onChange={e=>setObjective(e.target.value)}><option value="balanced">Balanced objective</option><option value="minimum_gates">Minimum gate count</option><option value="minimum_depth">Minimum circuit depth</option><option value="minimum_error">Minimum estimated error</option></select>
          <div className="objective-note"><ShieldCheck size={17}/><span>AI strategy selection currently uses a transparent heuristic fallback unless a trained model is supplied.</span></div>
          <button className="primary" disabled={busy||!circuit} onClick={optimize}>{busy?'Compiling…':'Optimize circuit'} <ArrowRight size={17}/></button>
          <button className="secondary" disabled={busy||!circuit} onClick={execute}><Play size={15}/> Run local simulation</button>
        </div>
      </section> : <section className="results">
        {!result ? <div className="empty panel"><Activity size={34}/><h3>No optimization run yet</h3><p>Submit a circuit from Circuit Studio to see before-and-after metrics.</p><button className="primary" onClick={()=>setTab('editor')}>Open Circuit Studio <ArrowRight size={16}/></button></div> :
        <>
          <div className="result-heading"><div><span className="eyebrow">COMPILATION COMPLETE</span><h2>Optimization summary</h2></div><div className="strategy"><span>SELECTED STRATEGY</span><b>{result.ai_decision.strategy}</b><small>{result.ai_decision.method}</small></div></div>
          <div className="metric-grid">{[['Gate count',result.before.gate_count,result.after.gate_count],['Circuit depth',result.before.depth,result.after.depth],['Two-qubit gates',result.before.two_qubit_gates,result.after.two_qubit_gates],['Inserted SWAPs',result.after.swap_count,'—'],['Estimated fidelity',result.after.estimated_fidelity,'—'],['Compile time',result.after.compile_time_ms+' ms','—']].map(([label,b,a],i)=><div className="panel metric-pair" key={i}><span>{label}</span><div><b>{b}</b><ArrowRight size={14}/><strong>{a}</strong></div></div>)}</div>
          <div className="panel"><div className="panel-head"><div><span className="eyebrow">EXPLAINABILITY</span><h3>Compiler decisions</h3></div></div><p>{result.ai_decision.reason || 'Strategy selected from configured objective and hardware profile.'}</p><ul>{result.explanation.map((x,i)=><li key={i}>{x}</li>)}</ul></div>
          <div className="panel"><div className="panel-head"><div><span className="eyebrow">OUTPUT</span><h3>Optimized circuit JSON</h3></div><button className="subtle" onClick={()=>navigator.clipboard.writeText(JSON.stringify(result.optimized_circuit,null,2))}>Copy JSON</button></div><pre>{JSON.stringify(result.optimized_circuit,null,2)}</pre></div>
        </>}
      </section>}
      {error&&<div className="error">{error}</div>}
      <footer>QOptiQ · Research prototype · Estimated metrics are analytical, not QPU measurements.</footer>
    </main>
  </div>
}
