from lexer import bcolors
from __future__ import annotations
def errorTrace(node):
    print(bcolors.UNDERLINE + bcolors.BOLD + bcolors.FAIL + "An Error occured in file: " + node.file + " on line " + str(node.line) + bcolors.ENDC + bcolors.HEADER + '\n')

    