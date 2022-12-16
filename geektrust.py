#!/usr/bin/python
import operator
import os
import sys
from Expense_Management import ExpenseManagement


# readFromFile - read contents from given file
# input        - filename:string
# output       - lines:array_of_string
# error        - if file not found
#                if file empty
def read_from_file(input_file):
    # exit if file doesnt exist
    if not os.path.isfile(input_file):
        print("%s file not found. Please provide valid file" % input_file)
        exit(2)
    # read from given file
    with open(input_file, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    # exit if no commands provided in file
    if len(lines) == 0:
        print("%s file is empty. Please provide valid inputs" % input_file)
        exit(2)
    return lines


def main():
    input_file = sys.argv[1]
    # parse the file and process the command
    contents = read_from_file(input_file)
    # Actual processing starts here
    ExpenseManagement(contents)


if __name__ == "__main__":
    main()  # pragma: no cover
