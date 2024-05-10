"""
Eric Diskin
Turns assembly into binary code.
Created on January 25, 2022
"""

import struct
import debugging

binKeys = [
    "FUN_HEAD",
    "ZERO",
    "CONST_0",
    "CONST_1",
    "CONST_2",
    "CONST_3",
    "CONST_4",
    "CONST_5",
    "CONST_BYTE",
    "CONST_SHORT",
    "LOAD_0",
    "LOAD_1",
    "LOAD_2",
    "LOAD_3",
    "LOAD_4",
    "LOAD_5",
    "LOAD_BYTE",
    "LOAD_SHORT",
    "STORE_0",
    "STORE_1",
    "STORE_2",
    "STORE_3",
    "STORE_4",
    "STORE_5",
    "STORE_BYTE",
    "STORE_SHORT",
    "IADD",
    "ISUB",
    "IMUL",
    "IDIV",
    "IMOD",
    "EXP",
    "AND",
    "OR",
    "XOR",
    "NOT",
    "LSHIFT",
    "RSHIFT",
    "COMPARE",
    "IEQ",
    "IGT",
    "ILT",
    "IGTE",
    "ILTE",
    "INEQ",
    "NEG",
    "BREAKPOINT",
    "MVU",
    "OUT",
    "IN",
    "SLEEP",
    "EXIT",
    "CALL",
    "RET",
    "DUP",
    "DATACOPY",
    "DATAFREE",
    "DATAGET",
    "DATASET",
    "DATASIZE",
    "DATARESIZE",
    "INTTOSTR",
    "RANDINT",
    "FADD",
    "FSUB",
    "FDIV",
    "FMUL",
    "FMOD",
    "FTI",
    "ITF",
    "FOUT",
    "FEQ",
    "FGT",
    "FLT",
    "FGTE",
    "FLTE",
    "FNEQ",
]

def buildBin(fileName):
    
    fileData = open(fileName, "r").read()

    if debugging.DebugFlags.saveBytecode:
        outPutFileCode = open('./' + fileName + "_bytecode", 'w')
        outPutFileCode.write(fileData)
        outPutFileCode.close()
        
    # loop through the lines of the file and erase any that start with a ; or are empty
    fileData = "\n".join([line.split()[0] for line in fileData.split(
        "\n") if not line.startswith(";") and not line == ""])

    res = []

    for i in fileData.split():
        if i in binKeys:
            res.append(binKeys.index(i))
        else:
            # turn the 0x into a number or float.

            res.append(int(i, 16))

    outPutFile = open('./' + fileName, 'wb')
    outPutFile.write(bytes(res))
    outPutFile.close()
