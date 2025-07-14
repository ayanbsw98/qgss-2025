# Test file for accumulated_errors function

from qiskit import QuantumCircuit
import json
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService

# Define the function to test (copied from user code, with minor adaptation for testability)
def accumulated_errors(backend, circuit):
    """Compute accumulated gate and readout errors for a given circuit on a specific backend."""
    acc_single_qubit_error = 0
    acc_two_qubit_error = 0
    single_qubit_gate_count = 0
    two_qubit_gate_count = 0
    acc_readout_error = 0

    properties = backend.properties()
    if properties is None:
        # No hardware properties available (e.g., basic AerSimulator)
        return [0, 0, 0, 0, 0, 0]
    
    n = circuit.num_qubits
    qubit_layout = list(range(n))  # For test, assume trivial layout

    for qubit in qubit_layout:
        acc_readout_error += properties.readout_error(qubit)

    for instruction in circuit.data:
        num_qubits = len(instruction.qubits)
        if instruction.operation.name == "measure":
            continue
        if num_qubits == 1:
            single_qubit_gate_count += 1
            logical_index = circuit.find_bit(instruction.qubits[0]).index
            if logical_index < len(qubit_layout):
                physical_qubit = qubit_layout[logical_index]
                try:
                    acc_single_qubit_error += properties.gate_error(instruction.operation.name, physical_qubit)
                except Exception:
                    pass
        elif num_qubits == 2:
            two_qubit_gate_count += 1
            logical_indices = [circuit.find_bit(q).index for q in instruction.qubits]
            if all(idx < len(qubit_layout) for idx in logical_indices):
                physical_qubits = [qubit_layout[idx] for idx in logical_indices]
                # ...existing code...
                # Directly search for the matching gate in properties.gates
                found = False
                for gate in properties.gates:
                    if gate.gate == instruction.operation.name and list(gate.qubits) == physical_qubits:
                        for param in gate.parameters:
                            if param.name == 'gate_error':
                                acc_two_qubit_error += param.value
                                found = True
                                break
                    if found:
                        break
    acc_total_error = acc_two_qubit_error + acc_single_qubit_error + acc_readout_error
    results = [
        acc_total_error,
        acc_two_qubit_error,
        acc_single_qubit_error,
        acc_readout_error,
        single_qubit_gate_count,
        two_qubit_gate_count,
    ]
    return results

# Test with a simple circuit and noisy fake backend

from qiskit.providers.fake_provider import GenericBackendV2

# Create a generic fake backend with 5 qubits
fake_backend = GenericBackendV2(num_qubits=5)

# Create noisy simulator from fake backend
backend = AerSimulator.from_backend(fake_backend, seed_simulator=42)
print(f"Using noisy simulator based on: {fake_backend.name}")

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()

print("Results:", accumulated_errors(backend, circuit))
