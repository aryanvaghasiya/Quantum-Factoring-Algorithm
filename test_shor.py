import pytest
from math import gcd
from fractions import Fraction

def test_gcd_nontrivial_factor():
    a = 13
    N = 15
    r = 4  # Known period
    factors = [gcd(a**(r//2) - 1, N), gcd(a**(r//2) + 1, N)]
    assert any(f not in [1, N] and N % f == 0 for f in factors), "No non-trivial factor found"

def test_phase_to_fraction():
    phase = 0.333
    frac = Fraction(phase).limit_denominator(15)
    assert 1 <= frac.denominator <= 15, f"Unexpected denominator: {frac.denominator}"

def test_qft_dagger():
    from shor_algo import qft_dagger  
    circuit = qft_dagger(3)
    assert circuit is not None
    assert circuit.num_qubits == 3

def test_c_amod15_structure():
    from shor import c_amod15
    gate = c_amod15(7, 1)
    assert gate.num_ctrl_qubits == 1
    assert gate.num_qubits == 5
