import pytest
from math import gcd
from fractions import Fraction

# Basic test to verify GCD function behaves as expected
def test_gcd_nontrivial_factor():
    a = 13
    N = 15
    r = 4  # Known period for a=13 mod 15
    factors = [gcd(a**(r//2) - 1, N), gcd(a**(r//2) + 1, N)]
    assert any(f not in [1, N] and N % f == 0 for f in factors), "No non-trivial factor found"

# Test that converting a phase to a fraction returns an expected denominator
def test_phase_to_fraction():
    phase = 0.333
    frac = Fraction(phase).limit_denominator(15)
    assert frac.denominator in [3, 5, 15], f"Unexpected denominator: {frac.denominator}"

# Dummy QFT dagger test: just checks that the function runs and returns a circuit
def test_qft_dagger():
    from your_script_name import qft_dagger  # Update this import!
    circuit = qft_dagger(3)
    assert circuit is not None
    assert circuit.num_qubits == 3
