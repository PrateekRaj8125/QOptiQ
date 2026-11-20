# Contributing Guidelines

Thank you for your interest in contributing to **QOptiQ**! 🚀

---

## How to Contribute

You can contribute in several ways:

* Reporting bugs
* Suggesting new features or improvements
* Adding or improving compiler optimization passes
* Improving the AI strategy selector and benchmark data
* Adding quantum hardware profiles
* Enhancing the React dashboard
* Writing tests
* Improving documentation

---

## Getting Started

### 1. Fork the Repository

Click the **Fork** button on GitHub to create your own copy of the repository.

### 2. Clone Your Fork

```bash
cd ..
cd ..
git clone https://github.com/PrateekRaj8125/QOptiQ.git
```

### 3. Navigate to the Project Directory

```bash
cd QOptiQ/code
```

### 4. Set Up the Backend

```bash
python -m venv .venv

# Windows:       .venv\Scripts\activate
# Linux / macOS: source .venv/bin/activate

./QOptiQ.bat
```

Open the interactive docs at:

```text
http://127.0.0.1:8000/docs
```

### 5. Set Up the Frontend (Optional)

```bash
cd QOptiQ/code/frontend

npm install

npm run dev
```

Open:

```text
http://localhost:5173
```

### 6. Run the Tests

```bash
cd ..

pytest -q
```

> [!NOTE]
> Windows users can run `QOptiQ.bat` from the `code` folder to set up and start the backend automatically.

---

## Development Guidelines

When contributing code:

* Follow clean and readable coding practices.
* Keep compiler passes small, modular and independently testable.
* Keep the compiler core provider-independent: talk to the internal IR, never to a vendor SDK directly.
* Use meaningful variable and function names.
* Add comments where the logic is not obvious.
* Validate all external input at the API boundary.
* Avoid breaking existing functionality.
* Ensure all changes are tested before submission.

---

## Project Structure

```text
QOptiQ/
├── code/
│   ├── app/
│   │   ├── main.py          # FastAPI routes
│   │   ├── api/             # Request / response schemas
│   │   ├── compiler/        # IR, optimizer, hardware, metrics
│   │   ├── ai/              # Strategy selector
│   │   ├── adapters/        # Simulator, IBM, Braket backends
│   │   └── jobs/            # SQLite job store
│   ├── frontend/            # React + TypeScript + Vite dashboard
│   ├── tests/
│   └── requirements.txt
├── docs/
│   ├── PROJECT_REPORT.md
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   └── SECURITY.md
└── README.md
```

---

## Areas for Contribution

### Compiler & Optimization

Possible enhancements:

* Global qubit remapping
* Better routing heuristics than shortest-path SWAP insertion
* Gate commutation and cancellation passes
* Unitary resynthesis
* Fuller OpenQASM 2 / 3 support

---

### AI Strategy Selection

Possible enhancements:

* Measured benchmark dataset generation
* Trained strategy model with documented features and evaluation
* Confidence estimates for predictions
* Comparison against fixed transpilation strategies

---

### Hardware & Execution

Possible enhancements:

* Additional hardware profiles and coupling maps
* Noise-aware simulation
* IBM Quantum integration (IR-to-Qiskit conversion and job handling)
* Amazon Braket integration
* Qiskit / PennyLane comparison benchmarks

---

### Platform & Infrastructure

Possible enhancements:

* PostgreSQL and Redis worker architecture
* Authentication and rate limiting
* Structured logging and monitoring
* CI pipeline and dependency scanning

---

### Dashboard

Possible enhancements:

* Visual circuit editor
* Circuit diagram rendering
* Hardware topology visualization
* Richer analytics and benchmark charts
* Export of results

---

## Commit Guidelines

Use clear and descriptive commit messages.

Examples:

```text
feat: add gate commutation pass

fix: correct SWAP count for disconnected coupling maps

docs: update Docker setup steps

test: add routing test for line topology

refactor: split metrics into per-pass helpers

ui: improve optimization result charts
```

---

## Pull Request Process

### 1. Create a New Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Implement your feature, bug fix, or improvement.

### 3. Test Your Changes

Verify that:

* `pytest -q` passes.
* The API starts and `/health` responds.
* The frontend builds (`npm run build`) if you changed it.
* New functionality behaves as expected and has a test where practical.

### 4. Commit and Push

```bash
git add .

git commit -m "feat: your feature description"

git push origin feature/your-feature-name
```

### 5. Open a Pull Request

Include:

* A clear description of the changes
* Motivation for the changes
* Before/after metrics for compiler or strategy changes
* Screenshots (for UI changes)
* Related issue references (if applicable)

---

## Code Style

### Python

* Follow PEP 8 guidelines.
* Keep functions concise and modular.
* Use descriptive names and type hints where helpful.
* Prefer readability over clever code.

### TypeScript / React

* Use consistent formatting.
* Keep components small and focused.
* Keep UI changes aligned with the existing design.

### Research & Machine Learning

* Document model assumptions and feature choices.
* Keep experiments reproducible.
* Do not present estimated or heuristic results as measured hardware results.

---

## Security & Secrets

* Never commit API keys, tokens or `.env` files (for example `IBM_QUANTUM_TOKEN`).
* Do not commit generated databases, virtual environments or `node_modules`.
* Report vulnerabilities privately. See [SECURITY.md](SECURITY.md).

---

## Reporting Issues

When reporting issues, please include:

* Description of the problem
* Steps to reproduce
* Expected behavior
* Actual behavior
* The circuit and hardware profile used (if applicable)
* Screenshots (if applicable)
* Environment information

Example:

```text
Operating System:
Python Version:
Node Version:
Run Method (local / Docker):
Error Message:
```

---

## Future Contribution Opportunities

The following areas are planned for future development:

* Real quantum provider execution
* Trained, benchmarked strategy model
* Global qubit remapping
* Noise-aware simulation
* Worker queue architecture
* Authentication system
* Cloud deployment

---

## Questions?

If you have questions, suggestions, or ideas, feel free to:

* Open an Issue
* Start a Discussion
* Submit a Pull Request

---

## Thank You

Your contributions help make quantum circuit compilation more accessible, transparent and effective.

Happy Coding! 🎯
