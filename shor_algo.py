!pip install qiskit
!pip install qiskit_aer

# Import essential libraries
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator
from math import gcd
from fractions import Fraction
from numpy.random import randint
import pandas as pd

print("Imports Successful")

def create_phase_rotation_gate(n):
    """
    Create a controlled phase rotation gate for Quantum Fourier Transform.

    Parameters:
        n (int): Level of rotation (controls the phase angle 2π / 2^n)

    Returns:
        Gate: Controlled phase rotation gate.
    """
    theta = 2 * np.pi / (2 ** n)
    phase_gate = QuantumCircuit(1, name=f'R_{n}')
    phase_gate.rz(theta, 0)
    return phase_gate.to_gate().control(1)


def quantum_fourier_transform(num_qubits):
    """
    Constructs a QFT circuit for a given number of qubits.

    Parameters:
        num_qubits (int): Number of qubits to apply QFT on.

    Returns:
        QuantumCircuit: QFT circuit.
    """
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

# Example QFT circuit
print(quantum_fourier_transform(5).draw())


def create_inverse_phase_rotation_gate(n):
    """
    Creates a controlled inverse phase rotation gate for inverse QFT.

    Parameters:
        n (int): Rotation level.

    Returns:
        Gate: Controlled inverse phase rotation gate.
    """
    theta = -2 * np.pi / (2 ** n)
    inverse_gate = QuantumCircuit(1, name=f'R_{n}†')
    inverse_gate.rz(theta, 0)
    return inverse_gate.to_gate().control(1)

def quantum_fourier_transform_inverse(num_qubits):
    """
    Constructs inverse QFT (QFT†) circuit.

    Parameters:
        num_qubits (int): Number of qubits.

    Returns:
        QuantumCircuit: QFT† circuit.
    """
    qft_inverse = QuantumCircuit(num_qubits, name="QFT†")

    # Reverse swap first
    for i in range(num_qubits // 2):
        qft_inverse.swap(i, num_qubits - i - 1)

    qft_inverse.barrier()

    for target_qubit in reversed(range(num_qubits)):
        for control_qubit in reversed(range(target_qubit + 1, num_qubits)):
            qft_inverse.append(
                create_inverse_phase_rotation_gate(control_qubit - target_qubit),
                [control_qubit, target_qubit]
            )
        qft_inverse.h(target_qubit)
        qft_inverse.barrier()

    return qft_inverse

# Example inverse QFT
print(quantum_fourier_transform_inverse(4).draw())



def qft_dagger(n):
    """
    Simpler implementation of QFT† for n qubits.

    Parameters:
        n (int): Number of qubits.

    Returns:
        QuantumCircuit: Inverse QFT circuit.
    """
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2 ** (j - m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc



def c_amod15(a, power):
    """
    Controlled modular multiplication gate for a^x mod 15.

    Parameters:
        a (int): Base of modular exponentiation.
        power (int): Number of times U is applied.

    Returns:
        Instruction: Controlled-U gate.
    """
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
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    return U.control()



def qpe_amod15(a):
    """
    Quantum Phase Estimation for finding the order 'r' in a^r mod N.

    Parameters:
        a (int): Base value for modular exponentiation.

    Returns:
        float: Estimated phase s/r
    """
    n_count = 8
    qc = QuantumCircuit(4 + n_count, n_count)

    # Apply Hadamards to counting qubits
    for q in range(n_count):
        qc.h(q)

    # Set auxiliary register to |1>
    qc.x(3 + n_count)

    # Apply controlled modular exponentiation
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q), [q] + [i + n_count for i in range(4)])

    # Apply inverse QFT
    qc.append(qft_dagger(n_count), range(n_count))
    qc.measure(range(n_count), range(n_count))

    # Simulate circuit
    aer_sim = AerSimulator()
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, memory=True).result()
    readings = result.get_memory()

    print("Register Reading: " + readings[0])
    phase = int(readings[0], 2) / (2 ** n_count)
    print(f"Corresponding Phase: {phase:.6f}")
    return phase


from math import gcd

# Number to factor
N = 15
# Choose valid a < N and gcd(a, N) == 1
a = 13

factor_found = False
attempt = 0

# Repeat until we find a non-trivial factor
while not factor_found:
    attempt += 1
    print(f"\nAttempt {attempt}:")
    phase = qpe_amod15(a)
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    print(f"Result: r = {r}")

    if phase != 0:
        guesses = [gcd(a**(r//2) - 1, N), gcd(a**(r//2) + 1, N)]
        print(f"Guessed Factors: {guesses[0]} and {guesses[1]}")
        for guess in guesses:
            if guess not in [1, N] and N % guess == 0:
                print(f"*** Non-trivial factor found: {guess} ***")
                factor_found = True




