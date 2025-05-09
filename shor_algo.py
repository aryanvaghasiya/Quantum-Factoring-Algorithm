# Import necessary libraries
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from math import gcd
from fractions import Fraction

# ------------------------------
# QFT Helper Functions
# ------------------------------

# Create a controlled phase rotation gate for QFT
def create_phase_rotation_gate(n):
    theta = 2 * np.pi / (2 ** n)
    phase_gate = QuantumCircuit(1, name=f'R_{n}')
    phase_gate.rz(theta, 0)
    return phase_gate.to_gate().control(1)

# Create a controlled inverse phase rotation gate for inverse QFT
def create_inverse_phase_rotation_gate(n):
    theta = -2 * np.pi / (2 ** n)
    inverse_gate = QuantumCircuit(1, name=f'R_{n}†')
    inverse_gate.rz(theta, 0)
    return inverse_gate.to_gate().control(1)

# Construct the Quantum Fourier Transform circuit
def quantum_fourier_transform(num_qubits):
    qft_circuit = QuantumCircuit(num_qubits, name="QFT")
    for target_qubit in range(num_qubits):
        qft_circuit.h(target_qubit)
        for control_qubit in range(target_qubit + 1, num_qubits):
            qft_circuit.append(
                create_phase_rotation_gate(control_qubit - target_qubit),
                [control_qubit, target_qubit]
            )
        qft_circuit.barrier()

    # Swap qubits to reverse their order
    for i in range(num_qubits // 2):
        qft_circuit.swap(i, num_qubits - i - 1)
    return qft_circuit

# Construct the inverse Quantum Fourier Transform circuit
def quantum_fourier_transform_inverse(num_qubits):
    qft_inverse = QuantumCircuit(num_qubits, name="QFT†")

    # Swap first (reverse order)
    for i in range(num_qubits // 2):
        qft_inverse.swap(i, num_qubits - i - 1)
    qft_inverse.barrier()

    # Apply controlled phase rotations and Hadamard gates
    for target_qubit in reversed(range(num_qubits)):
        for control_qubit in reversed(range(target_qubit + 1, num_qubits)):
            qft_inverse.append(
                create_inverse_phase_rotation_gate(control_qubit - target_qubit),
                [control_qubit, target_qubit]
            )
        qft_inverse.h(target_qubit)
        qft_inverse.barrier()
    return qft_inverse

# Alternate inverse QFT (QFT†) implementation using controlled phase rotations
def qft_dagger(n):
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2 ** (j - m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc

# ------------------------------
# Modular Exponentiation Gate
# ------------------------------

# Create a controlled modular multiplication circuit for a^x mod 15
def c_amod15(a, power):
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("'a' must be one of: 2, 4, 7, 8, 11, or 13")
    U = QuantumCircuit(4)
    for _ in range(power):
        if a in [2, 13]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [7, 8]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [4, 11]:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)

    # Convert to a controlled gate
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    return U.control()

# ------------------------------
# Quantum Phase Estimation
# ------------------------------

# Quantum Phase Estimation using modular exponentiation
def qpe_amod15(a):
    n_count = 8  # Number of counting qubits
    qc = QuantumCircuit(4 + n_count, n_count)

    # Apply Hadamard to counting qubits
    for q in range(n_count):
        qc.h(q)

    # Set last qubit of auxiliary register to |1>
    qc.x(3 + n_count)

    # Apply controlled-U operations
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q), [q] + [i + n_count for i in range(4)])

    # Apply inverse QFT to counting register
    qc.append(qft_dagger(n_count), range(n_count))

    # Measure counting register
    qc.measure(range(n_count), range(n_count))

    # Simulate the circuit
    aer_sim = AerSimulator()
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, memory=True).result()
    readings = result.get_memory()

    # Decode binary result to a phase (float)
    phase = int(readings[0], 2) / (2 ** n_count)
    return phase

# ------------------------------
# Run Shor's Algorithm
# ------------------------------

# High-level routine to execute Shor's Algorithm to factor N
def run_shor(N=15, a=13):
    factor_found = False
    attempt = 0

    while not factor_found:
        attempt += 1
        print(f"\nAttempt {attempt}:")
        
        # Step 1: Run QPE to get phase
        phase = qpe_amod15(a)

        # Step 2: Convert phase to a rational fraction
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        print(f"Estimated r = {r}")

        # Step 3: Use guessed period to compute factors
        if phase != 0:
            guesses = [gcd(a**(r//2) - 1, N), gcd(a**(r//2) + 1, N)]
            print(f"Guessed factors: {guesses}")
            
            # Step 4: Check if factor is valid
            for guess in guesses:
                if guess not in [1, N] and N % guess == 0:
                    print(f"*** Non-trivial factor found: {guess} ***")
                    factor_found = True
                    break


if __name__ == "__main__":
    run_shor(N=15, a=13)
