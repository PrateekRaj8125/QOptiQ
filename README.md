# QOptiQ Backend

Provider-independent backend foundation for QOptiQ: quantum circuit IR, basic compiler passes, hardware topology routing, heuristic strategy selection, local statevector simulation, FastAPI, and SQLite-backed jobs.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs.

## Docker
```bash
docker compose up --build
```

## API
- GET `/health`
- POST `/circuits/validate`
- POST `/circuits/parse-qasm`
- GET `/hardware`
- POST `/optimize`
- POST `/transpile`
- POST `/execute`
- POST `/jobs`
- GET `/jobs/{id}`
- GET `/results/{id}`
- GET `/benchmarks`

Example `/optimize`:
```json
{
  "circuit": {
    "num_qubits": 3,
    "gates": [
      {"name": "H", "qubits": [0]},
      {"name": "CX", "qubits": [0, 2]}
    ],
    "measurements": [0, 1, 2]
  },
  "objective": "balanced"
}
```

Set `QOPTIQ_API_KEY` to require `X-API-Key`. This is only a simple development guard.

## Implemented / not implemented
Implemented: IR validation, limited QASM2 parser, adjacent inverse cancellation, same-axis rotation merging, shortest-path SWAP insertion, heuristic strategy selection, approximate metrics, small NumPy simulator, REST API, SQLite job persistence, Docker.

Not implemented: global qubit remapping, full QASM standard, unitary resynthesis, hardware noise simulation, real IBM/Braket job submission, PostgreSQL/Redis worker cluster, measured AI training dataset. IBM and Braket files are deliberate extension placeholders.

The simulator is capped at 20 qubits. Estimated error/fidelity are analytic estimates from configured error rates, not device-measured fidelity. The heuristic selector is not a trained scientific model. Use measured benchmark data before making research claims.

Run tests: `pytest -q`.
