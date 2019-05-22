# CREDIT: https://stackoverflow.com/questions/44818884/all-numbers-in-a-given-range-but-random-order

# randint(a, b) returns a random integer in the range (a..b) (inclusive)
from random import randint


def lcg_params(u, v):
    # Generate parameters for an LCG that produces a maximal length sequence
    # of numbers in the range (u..v)
    diff = v - u
    if diff < 4:
        raise ValueError("Sorry, range must be at least 4.")
    m = 2 ** diff.bit_length()  # Modulus
    a = (randint(1, (m >> 2) - 1) * 4) + 1  # Random odd integer, (a-1) divisible by 4
    c = randint(3, m) | 1  # Any odd integer will do
    return (m, a, c, u, diff + 1)


def generate_pseudorandom_sequence(rmin, rmax):
    (m, a, c, offset, seqlength) = lcg_params(rmin, rmax)
    x = 1  # Start with a seed value of 1
    result = []  # Create empty list for output2 values
    for i in range(seqlength):
        # To generate numbers on the fly without storing them in an array,
        # just run the following while loop to fetch a new number
        while True:
            x = (x * a + c) % m  # Iterate LCG until we get a value in the
            if x < seqlength: break  # required range
        result.append(x + offset)  # Add this value to the list
    return result
