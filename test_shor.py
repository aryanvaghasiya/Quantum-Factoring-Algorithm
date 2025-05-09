def test_gcd_example():
    from math import gcd
    assert gcd(13**2 - 1, 15) in [3, 5]

def test_phase_to_fraction():
    from fractions import Fraction
    phase = 0.333
    frac = Fraction(phase).limit_denominator(15)
    assert frac.denominator in [3, 5, 15]
