# Shor's Algorithm - Quantum Factoring with Qiskit

This repository contains a simple yet complete implementation of **Shor's Algorithm**, a quantum algorithm for integer factorization that runs exponentially faster than the best known classical algorithms. This project simulates the algorithm using IBM's **Qiskit** framework and targets factoring of the number 15, a standard demonstration example.

## 🔍 What is Shor's Algorithm?

Shor's Algorithm was proposed by mathematician Peter Shor in 1994 and is one of the most well-known quantum algorithms due to its theoretical ability to break widely used cryptographic schemes (like RSA) by factoring large integers in polynomial time.

The algorithm relies on **Quantum Phase Estimation** (QPE) and **modular exponentiation** to find the periodicity (order) of a function, which helps in factorizing a number.

## 📘 Project Highlights

- Simulates **Shor's Algorithm** for factoring \( N = 15 \)
- Uses **Quantum Fourier Transform (QFT)** and its inverse
- Implements **Quantum Phase Estimation (QPE)** for order finding
- Includes logic to compute classical post-processing and verify the factors
- Built using **Qiskit**, a powerful open-source SDK for quantum computing

## 🧠 Key Concepts & Technologies Used

| Concept | Description |
|--------|-------------|
| **Quantum Fourier Transform** | Key component for Phase Estimation |
| **Quantum Phase Estimation (QPE)** | Central subroutine to extract the period of a function |
| **Modular Exponentiation** | Circuit-level implementation to simulate \( a^x \mod N \) |
| **Qiskit** | IBM's quantum computing SDK used for simulation |
| **Classical Post-Processing** | GCD and periodicity logic to compute factors |

## 🛠 Installation

Make sure you have Python installed, then install the required dependencies:

```bash
pip install qiskit qiskit-aer matplotlib numpy pandas

## 🚀 How to Run

You can run this project via Jupyter Notebook or directly in a Python environment. The key function that performs the order-finding is:

```python
phase = qpe_amod15(a)
```

Followed by computing the factors from the derived phase.

To explore how the algorithm behaves with different inputs:

```python
a = 13  # Can be 2, 4, 7, 8, 11, or 13
```

and rerun the simulation loop until a non-trivial factor is found.

## 📊 Sample Output

```
Attempt 1:
Register Reading: 01100000
Corresponding Phase: 0.375000
Result: r = 8
Guessed Factors: 5 and 3
*** Non-trivial factor found: 5 ***
```

## 📂 Project Structure

```
├── Shor_algo.ipynb       # Jupyter notebook with all code
├── README.md             # This file
└── requirements.txt      # Optional: list of dependencies
```

## 🔍 References

* [Shor's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Shor%27s_algorithm)
* [Qiskit Documentation](https://qiskit.org/documentation/)
* Nielsen & Chuang, *Quantum Computation and Quantum Information*
