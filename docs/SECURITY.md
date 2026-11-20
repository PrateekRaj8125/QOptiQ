# Security Policy

## Supported Versions

The following versions are currently supported with security updates:

| Version | Supported |
| --- | --- |
| Latest (`main`) | ✅ |
| Older versions | ❌ |

---

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

### 📧 Contact:

<prateek.raj.indt@gmail.com>

Please do **not** open a public GitHub issue for security problems.

---

## Reporting Guidelines

When reporting a vulnerability, include:

* Description of the issue
* Affected component (API, compiler, job store, adapters, frontend, Docker setup)
* Steps to reproduce (a sample request or circuit is ideal)
* Potential impact
* Suggested fix (if available)

---

## Response Process

* Acknowledgement within 48 hours
* Investigation and validation
* Fix development and testing
* Responsible disclosure after resolution

---

## Scope of Security

This project is a **research / educational MVP**, so:

* Authentication is a simple development guard: setting `QOPTIQ_API_KEY` requires an `X-API-Key` header, but there are no user accounts, roles or rate limits
* Job data is stored in a local SQLite file without encryption
* Real IBM Quantum and Amazon Braket submission is **not enabled**; the adapter files are placeholders
* Fidelity and error values are analytic estimates, not device-measured results
* The local simulator is capped at 20 qubits

Despite this, we take security concerns seriously.

### Areas of Particular Interest

Reports are especially welcome for:

* Bypass of the `X-API-Key` check
* Malformed circuit or QASM input that crashes the service or causes excessive CPU or memory use
* Injection or path issues in the job store
* Insecure CORS behavior
* Secrets (tokens, keys) leaking through logs, responses or the repository
* Vulnerable dependencies in `requirements.txt` or the frontend `package-lock.json`

---

## Best Practices for Users

* Run QOptiQ locally or in a controlled environment
* Do not expose the API publicly without authentication, TLS and rate limiting in front of it
* Set a strong `QOPTIQ_API_KEY` and never commit it
* Replace the default `CORS_ORIGINS=*` with your actual frontend origin
* Keep `.env` out of version control, especially if you add `IBM_QUANTUM_TOKEN`
* Only load strategy models (`.joblib`) from sources you trust, since joblib files can execute code when loaded
* Keep Python and npm dependencies updated
* Do not submit proprietary or sensitive circuits to a shared deployment

---

## Responsible Disclosure

Please do not publicly disclose vulnerabilities until they are resolved.

---

Thank you for helping keep this project secure 🔒
