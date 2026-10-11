# c3_composite_check.py
import sympy

p3 = 115792089237316196275616121189559184590969122206767713959943689392442706417673

print("p3 bit length:", p3.bit_length())
print("p3 is prime?", sympy.isprime(p3))

if not sympy.isprime(p3):
    print("p3 FACTORIZATION:", sympy.factorint(p3))
    # Если p3 = q1*q2*..., решаем ECDLP mod qi и собираем CRT