

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
