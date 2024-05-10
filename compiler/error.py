from lexer import bcolors

def errorTrace(node):
    print(bcolors.UNDERLINE + bcolors.BOLD + bcolors.FAIL + "An Error occured in file: " + node.file + " on line " + str(node.line) + bcolors.ENDC + bcolors.HEADER + '\n')

    