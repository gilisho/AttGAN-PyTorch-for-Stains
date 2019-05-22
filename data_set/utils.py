

# randint(a, b) returns a random integer in the range (a..b) (inclusive)
from colorsys import hsv_to_rgb
from numpy.random import randint

def get_text(source_text_cache, minlines, maxlines):
    # source_text_cache is a list containing lines of text read beforehand from a text file
    
    output_text = ''
    num_lines_in_source = len(source_text_cache)
    num_lines_in_output = randint(minlines, maxlines+1)
      
    for _ in range(num_lines_in_output):
        # take randomly a line and add it to output_text
        line_num = randint(0, num_lines_in_source)
        output_text += source_text_cache[line_num]
    return output_text


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))



# CREDIT: https://stackoverflow.com/questions/44818884/all-numbers-in-a-given-range-but-random-order

# def lcg_params(u, v):
#     # Generate parameters for an LCG that produces a maximal length sequence
#     # of numbers in the range (u..v)
#     diff = v - u
#     if diff < 4:
#         raise ValueError("Sorry, range must be at least 4.")
#     m = 2 ** diff.bit_length()  # Modulus
#     a = (randint(1, (m >> 2) - 1) * 4) + 1  # Random odd integer, (a-1) divisible by 4
#     c = randint(3, m) | 1  # Any odd integer will do
#     return (m, a, c, u, diff + 1)


# def generate_pseudorandom_sequence(rmin, rmax):
#     (m, a, c, offset, seqlength) = lcg_params(rmin, rmax)
#     x = 1  # Start with a seed value of 1
#     result = []  # Create empty list for output2 values
#     for i in range(seqlength):
#         # To generate numbers on the fly without storing them in an array,
#         # just run the following while loop to fetch a new number
#         while True:
#             x = (x * a + c) % m  # Iterate LCG until we get a value in the
#             if x < seqlength: break  # required range
#         result.append(x + offset)  # Add this value to the list
#     return result
