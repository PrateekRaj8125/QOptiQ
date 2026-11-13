"""IBM Quantum integration placeholder. No QPU submission is enabled in this release."""
import os
class IBMBackend:
    name="ibm-quantum"
    def __init__(self):
        if not os.getenv("IBM_QUANTUM_TOKEN"):
            raise RuntimeError("Set IBM_QUANTUM_TOKEN before enabling IBM Quantum.")
        raise NotImplementedError("Complete QOptiQ IR-to-Qiskit conversion and Runtime job handling before enabling QPU execution.")
