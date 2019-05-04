import random


def read_txt_file(filename):
    file = open(filename, "r")
    output_text = ''

    while len(output_text) == 0:  # make sure that output_text will not be empty
        lines = file.readlines()
        num_of_lines_in_files = len(lines)

        num_of_lines_in_output_text = random.randint(1, 4)  # number of lines of text is between 1 to 3

        # take randomly a line and add it to output_text
        for i in range(num_of_lines_in_output_text):
            line_num = random.randint(0, num_of_lines_in_files + 1)  # line num to read from text
            output_text += lines[line_num]

    file.close()
    return output_text
