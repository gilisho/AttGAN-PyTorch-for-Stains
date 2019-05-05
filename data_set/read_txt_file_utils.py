import random


def read_txt_file(filename, minlines, maxlines):
    file = open(filename, "r")
    output_text = ''

    while len(output_text) == 0:  # make sure that output_text will not be empty
        lines = file.readlines()
        num_of_lines_in_file = len(lines)

        num_of_lines_in_output_text = random.randint(minlines, maxlines)

        # take randomly a line and add it to output_text
        for _ in range(num_of_lines_in_output_text):
            line_num = random.randint(0, num_of_lines_in_file + 1)  # line num to read from text
            if line_num >= num_of_lines_in_file:       # file has ended 
                break
            output_text += lines[line_num]

    file.close()
    return output_text
