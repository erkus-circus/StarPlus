"""
Takes a Node tree, from actionTree.py
Then converts it into a string containing the bytecode and data to be transpiled into actual bytecode
Eric Diskin
Created: 4-19-21, in TLP class
"""

from syntaxTree import Node
from createData import bytesFromNumber, createData
from actionTree import Function, functionData, specialFunctionData, constants, functions
from debugging import DebugFlags

spacer = " " * 16

class CodeBlock:
    def __init__(self, *args):
        self.body = []
    def append(self, toAppend):
        if type(toAppend) == str:
            self.body.append(toAppend)
        else:
            for i in toAppend.body:
                self.body.append(i)
    def __len__(self):
        return len(self.body)

    # def __add__(self, b):
    #     self.body.append(b)
    #     return self

    def __str__(self):
        longestLine = 0
        for i in self.body:
            if len(i) > longestLine:
                longestLine = len(i)

        output = "\n" + bytesFromNumber(len(self.body)) + " ; Number of instructions\n"
        for i in range(len(self.body)):
            if self.body[i] != "":
                output += self.body[i] + ((longestLine + 8 - len(self.body[i])) * " ") + "; PC: " + str(i) + "\n" 
        return output

constantsData = ""
output = ""

# this is how many spaces are in between line and its comment.
commentWidth = 4 * " "

# wraps a bunch of code into a function
#


def wrapInFunction(code: CodeBlock, functionIndex: int) -> str:
    # TODO: bytes from number gives it a 4 long hex, when it should be 2 long hex number.
    argumentsLen = '\n'.join(bytesFromNumber(
        len(functionData[functionIndex].paramTypes)).split()[2:])
    # return "\nFUN_HEAD" + " ; Index: " + str(functionIndex) + "\n" + argumentsLen + " ; " + str(len(functionData[functionIndex].paramTypes)) + " parameters.\n" + code + "\nINSTR_END\n"
    return "\n\n; FUNCTION HEADER, Index: " + str(functionIndex) + " \n" + argumentsLen + " ; " + str(len(functionData[functionIndex].paramTypes)) + " parameters." + str(code)


def createExpression(expression: list[Node]) -> CodeBlock:
    # the dictionary for comparing operators to their bytecode values.
    operatorDict = {
        '+': "ADD ; Add",
        '-': "SUB ; Subtract",
        '*': "MUL ; Multiply",
        '/': "DIV ; Divide",
        '%': "MOD ; Modulo",

        # these are reversed because i am lazy
        "<=": "GTE ; Greater Than or Equal To",
        ">=": "LTE ; Less Than Or Equal To",
        "<": "GT ; Greater Than",
        ">": "LT ; Less Than",
        "==": "EQ ; Equal To"
    }

    expressionBlock = CodeBlock()
    # loop through the expression and create an currentOutput
    for i in expression:
        if i.nodeName == "call":
            # do something special here.
            expressionBlock.append(createCall(i))
        elif i.nodeName == "variableReference":
            expressionBlock.append(getString(i.name, "LOAD_", postComment=" ; Variable Index: " + str(i.name)))
        elif i.nodeName == "constantReference":
            expressionBlock.append(getString(i.value, "CONST_", postComment=" ; " + str(constants[i.value]) + ", Index: " + str(i.value)))
        elif i.nodeName == "operator":
            expressionBlock.append(operatorDict[i.value])
    return expressionBlock

def createWhileLoop(node: Node) -> CodeBlock:
    whileBlock = CodeBlock()
    # first is the expression to check if is true, then after is the number of lines to skip if the expression evaluates to FALSE.
    whileBlock.append(createExpression(node.arguments[0].children))
    whileBody = createBody(node)

    # first add number of instructions to move up
    # also include number of instructions the MVU takes up
    # + 5 is the number the CONST_BYTE will take up for the 
    numInstructions = len(whileBody) + len(whileBlock) + 6

    # find if the numInstructions is in the allConstants list
    if numInstructions in constants:
        # if it is, then we can just use the constant
        whileBody.append(getString(constants.index(numInstructions), "CONST_", forceByte=True, postComment=" ; " + str(numInstructions)))
    else:
        # if it is not, then we need to add it to the constants list
        constants.append(numInstructions)
        # and then we need to add it to the whileBlock
        whileBody.append(getString(constants.index(numInstructions), "CONST_", forceByte=True, postComment=" ; " + str(numInstructions)))
    whileBody.append("MVU")

    # number of lines the compare should skip over
    numLinesSkip = len(whileBody)

    if numLinesSkip in constants:
        whileBlock.append(getString(constants.index(numLinesSkip), "CONST_", forceByte=True, postComment=" ; " + str(numLinesSkip)))
    else:
        # if it is not, then we need to add it to the constants list
        constants.append(numLinesSkip)
        # and then we need to add it to the whileBlock
        whileBlock.append(getString(constants.index(numLinesSkip), "CONST_", forceByte=True, postComment=" ; " + str(numLinesSkip)))
    
    whileBlock.append("COMPARE")
    whileBlock.append(whileBody)
    # get the expression
    return whileBlock


def createCall(node: Node) -> CodeBlock:
    callBlock = CodeBlock()

    # parse its arguments
    for i in node.children[0].children:
        callBlock.append(createExpression(i.children))

    # this is a builtin function.
    if node.special:
        for i in specialFunctionData[node.name].assembly.split():
            callBlock.append(i)
    else:
        # get call index
        callBlock.append(getString(constants.index(node.name), "CONST_", postComment=" ; " + str(
            functions[node.name]) + ", Function Index: " + str(node.name)))
        # call the function
        callBlock.append("CALL")
    return callBlock


"""
# turn like get 5 to C_5 or C_3 or if it is greater than 5, C_B 0x06 or something.
# number is the index of the string, prefix is the prefix like C_ or P_ or S_ or L_
"""
def getString(number: int, prefix: str, forceByte=False, postComment="") -> CodeBlock:
    if number <= 5 and not forceByte:
        res = CodeBlock()
        res.append(prefix + str(number) + postComment)
        return res
    else:
        if number < 0xFF:
            # not sure if hex is the correct function, should work for now tho.
            hexedNum = hex(number)
            if len(hexedNum) < 4:
                # fixes something
                hexedNum = "0x0" + hexedNum[2]
            res = CodeBlock()
            res.append(prefix + "BYTE")
            res.append(hexedNum + postComment)
            return res
        else:
            hexedNum = bytesFromNumber(number)[9:]
            res = CodeBlock()
            res.append(prefix + "SHORT")
            res.append(hexedNum + postComment)
            return res


def createVariableAssignment(node: Node) -> CodeBlock:
    # the output for the expression
    assignmentBlock = CodeBlock()
    # get expression as children.
    # node.children is the expression array
    # should this work?
    if len(node.children) > 0:
        # child length is greater than zero.
        assignmentBlock.append(createExpression(node.children[0].children))
    else:
        assignmentBlock.append("ZERO")
    assignmentBlock.append(getString(node.name, "STORE_"))
    return assignmentBlock


# create a higher level constants string, then output it
def createConstants(constants: list) -> str:
    global constantsData

    for i in constants:
        if type(i) == int:
            # int
            constantsData += "\nN " + str(i)
        else:
            # string uses less bits to hold values
            constantsData += "\nS " + i
    # comment this out later:
    if DebugFlags.showHumanConstants:
        print("=============== Constants in human readable format ===============")
        print(constantsData)
    # above line
    return createData(constantsData.strip())

# number of functions
functionCount = 0

def createBody(node: Node, functions=[]) -> CodeBlock:
    global functionCount
    # the current output, this will go into wrapFunction to turn it into a function before going into the output.

    bodyBlock = CodeBlock()
    # TODO: thinking maybe here count how many lines currentOutput is
    # so then i am able to count how many statements execute
    # which then is used for skipping the correct amout of if statements if it does not work.
    ## TODO: almost 2022 take: do a wrapInIf and wrapInIfElse

    for i in node.children:

        # parse a variable declaration
        if i.nodeName == "varDeclaration" or i.nodeName == "assignment":
            bodyBlock.append(createVariableAssignment(i))
        elif i.nodeName == "function":
            # assumes i has at least one child, because if not then it is broken.
            bodyBlock.append(wrapInFunction(createBody(i.children[0]), functionIndex=int(i.name)))
            # increment the number of functiions parsed.
            functionCount += 1
        elif i.nodeName == "call":
            bodyBlock.append(createCall(i))
        elif i.nodeName == "return":
            bodyBlock.append(createExpression(i.children[0].children))
            bodyBlock.append("RET")
        elif i.nodeName == "if":
            bodyBlock.append(createIf(i))
        elif i.nodeName == "whileLoop":
            bodyBlock.append(createWhileLoop(i))
    return bodyBlock

# create an if statement


def createIf(node: Node) -> CodeBlock:
    ifBlock = CodeBlock()
    # first is the expression to check if is true, then after is the number of lines to skip if the expression evaluates to FALSE.
    ifBlock.append(createExpression(node.arguments[0].children))
    ifBody = createBody(node)

    numInstructions = len(ifBody)
    # i am going to need to make constants global for this to work

    # find if the numInstructions is in the allConstants list
    if numInstructions in constants:
        # if it is, then we can just use the constant
        ifBlock.append(getString(constants.index(numInstructions), "CONST_"))
    else:
        # if it is not, then we need to add it to the constants list
        constants.append(numInstructions)
        # and then we need to add it to the ifBlock
        ifBlock.append(getString(constants.index(numInstructions), "CONST_"))
    ifBlock.append("COMPARE")
    ifBlock.append(ifBody)
    return ifBlock

allConstants = []
def createCode(node: Node, functions: list[str], functionData: list[str], constants: list):
    allConstants = constants

    functionsOut = createBody(node, functions)
    
    # is below because more constants can be added (from if statements)
    constants = createConstants(allConstants)
    # - 1 i think for function count?
    codeOut = "\n".join(functionsOut.body)
    # index = 0
    # skipNext = False
    # for i in str(functionsOut).split('\n'):
    #     i = i.strip()
    #     if skipNext:
    #         skipNext = False
    #         codeOut += i + '\n'
    #         continue
    #     if len(i) > 0:
    #         if i.startswith("FUN_HEAD"):
    #             index = 0
    #             codeOut += "FUN_HEAD\n"
    #             skipNext = True
    #             continue

    #         codeOut += i + "\n" #+ ((longestLine + 8 - len(i)) * " ") + "; PC: " + str(index) + "\n"
    #         index += 1
    #     else:
    #         codeOut += '\n'

    output = constants + \
        bytesFromNumber(functionCount) + " ; Number of functions." + codeOut
    return output