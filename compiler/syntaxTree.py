# https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from __future__ import annotations
from lexer import LexList, Type, Types, bcolors, lex

"""
Parses the LexedList into a tree consisting of Nodes
Eric Diskin
3/22/21 Created, things copied from older projects from 2019
"""

"""

Each Parse function takes in at least a lexedList and returns a Node

"""


# used for includes.
# every include is parsed into a tree, then at the end of the parsing of the LexList,
# add these in reversed order to the syntax tree.
## if it has already been included then fuck.
includedTrees = []

class Node:
    def __init__(self, name) -> None:
        # the name of node: string, body, if, func declaration, like statements
        self.nodeName = name
        # children of the node, for bodys, and arguments
        self.children: list[Node] = []
        # arguments, for parameters or arrays or if statements: Node, because arguments is its own list
        self.arguments: list[Node] = []
        # the name of the node
        self.name = ""

        # the type of the node (for functions and variable declarations and other things like that)
        self.type = ""

        # for builtin functions
        self.special = False

        # if the node (for variable declaration types) is initalized or not.
        # TODO HERE, varDeclaration now.
        self.initialized = False
        # only is set to true if the variable is a constant, not something else
        self.constant = False

        # the value of the node, for values like strings and numbers
        self.value = ""

    # print all children and itself

    def printAll(self, spaces=0):
        output = spaces * ' '
        output += getIfValue("NODETYPE: ", self.nodeName)
        output += getIfValue("NAME: ", self.name)
        output += getIfValue("TYPE: ", self.type)
        output += getIfValue("INITIALIZED: ", self.initialized)
        output += getIfValue("VALUE: ", self.value)
        output += getIfValue("SPECIAL: ", self.special)
        print(output)
        for i in range(len(self.children)):
            self.children[i].printAll(spaces + 6)
        for i in range(len(self.arguments)):
            if i < 1:
                print('\n\n')
            self.arguments[i].printAll(spaces + 4)


# for better printing of printAll, only include if the value != "" or None
def getIfValue(prefix: str, value) -> str:
    if value == "" or value == False and not type(value) == int:
        return ""
    else:
        return prefix + str(value) + " "

# parse a body


def parseBody(lexed: LexList, end="EOF") -> Node:
    # EXPECTS to have lexed on token before the first statement.
    # init a body node
    tree = Node("Body")
    # lexed.index starts at -1 so taking it to 0 for the first index
    lexed.stepUp()
    # end is either EOF or } or something similar.
    while lexed.canRetrieve() and lexed.getVal() != end:
        # always skip space

        lexed.skipSpace()
        # expect only ID's and STATEMENTS
        if lexed.getVal() == end:
            break
        lexed.expect(Types.ID, Types.STATEMENT)

        # inside body funcs expect only statements and word tokens like for assinging and calling functions
        if lexed.getType() == "STATEMENT":
            # each function call here lexed index is pointing on top of STATEMENT
            if lexed.getVal() == "var":
                # parse a variable declaration
                tree.children.append(parseVarDeclaration(lexed))
            if lexed.getVal() == "func":
                # parse a function declaration
                tree.children.append(parseFunctionDeclaration(lexed))
            if lexed.getVal() == "if":
                # parse an if statement
                tree.children.append(parseIf(lexed))
            if lexed.getVal() == "else":
                # parse an else statement
                tree.children.append(parseElse(lexed))
            if lexed.getVal() == "return":
                # parse a return statement
                tree.children.append(parseReturn(lexed))
            if lexed.getVal() == "for":
                # parse a for loop statement
                tree.children.append(parseForLoop(lexed))
            if lexed.getVal() == "while":
                # parse a while loop statement
                tree.children.append(parseWhileLoop(lexed))
            if lexed.getVal() == "include":
                # include another file into the file.
                pass

        elif lexed.getType() == "ID":
            # lexed index is pointing on top of ID
            tree.children.append(parseID(lexed))
            # expect a semicolon at the end of a statement
            lexed.expect(Types.SEMICOL)
            # step past the semicolon
            lexed.stepUp()
        else:
            # error
            pass


        # stepUp
        lexed.stepUp()
    return tree

# parse a thing like var name@type;
# isArgument tells this if the thing being parsed is an argument or a variable declaration
def parseVarDeclaration(lexed: LexList, isArgument=False) -> Node:

    # return value:
    varDeclarationNode = Node("varDeclaration")
    
    # what type of variable.
    varDeclarationNode.type = "parameter" if isArgument  else "variable"

    # starts pointintg lexed on top of the STATEMENT, or a COMMA. maybe: parenthesis for opening function declarations
    lexed.expect(Types.STATEMENT, Types.COMMA, Types.PARENTH)

    # skip to the name of the variable
    lexed.stepUp()
    lexed.skipSpace()
    # expect ID, the name
    lexed.expect(Types.ID)
    varDeclarationNode.name = lexed.getVal()

    # skip to the @ symbol, for the type
    lexed.stepUp()
    lexed.skipSpace()
    lexed.expect(Types.TYPEOPER)

    # skip to the type, an ID:
    lexed.stepUp()
    lexed.skipSpace()
    lexed.expect(Types.ID)
    varDeclarationNode.type = lexed.getVal()

    # expect either a ; or an = or a , or a )
    lexed.stepUp()
    lexed.skipSpace()
    lexed.expect(Types.SEMICOL, Types.COMPOPERATOR, Types.COMMA, Types.PARENTH)

    ## TODO: make sure that the operator type expected here is a = sign.

    # end here if it is a semicolon or a comma(argument) or a ) (argument)
    if lexed.getType() == "SEMICOL" or ((lexed.getType() == "COMMA" or lexed.getVal() == ")") and isArgument):
        return varDeclarationNode

    # else, parse it as an expression
    varDeclarationNode.initialized = True
    varDeclarationNode.children = [
        parseExpression(lexed, ")," if isArgument else ";")]

    # expect the line to end with a semicolon, then return back.
    if not isArgument:
        lexed.expect(Types.SEMICOL)

    return varDeclarationNode


# parse an ID into a function call or an assignment
def parseID(lexed: LexList) -> Node:

    # expect an ID on top
    lexed.expect(Types.ID)

    # step and skip
    lexed.stepUp()
    lexed.skipSpace()

    # expect ID followed by (), =, or []
    # dont do this because it might not be true in every case.
    #lexed.expect(Types.PARENTH, Types.EQUALS, Types.BRACKET)

    # parse a function call
    if lexed.getVal() == "(":
        # parseCall is expecting the name of the ID
        lexed.stepDown()
        # return the call Node.
        ### TODO: Check where lexed leaves this off,
        return parseCall(lexed)

    # parse an assignment
    elif lexed.getVal() == "=":
        return parseAssignment(lexed)

    # parse a bracket
    # followed by assignment or call: array[index]();
    elif lexed.getVal() == "[":
        pass

    else:
        # just is a reference to another variable
        lexed.stepDown()
        # skip downwards
        lexed.skipSpace(True)
        referenceNode = Node("reference")
        referenceNode.name = lexed.getVal()
        ### TODO: check where lexed leave sthis off, relative to above.
        return referenceNode

    # TODO: return a Node
    return Node("DOESNT EXIST, LOOK AT END OF PARSED ID")


def parseCall(lexed: LexList) -> Node:
    tree = Node("call")

    # expect an ID, for function name
    lexed.expect(Types.ID)

    # get the name of the function
    tree.name = lexed.getVal()

    # step and skip
    lexed.stepUp()
    lexed.skipSpace()

    # now pointing to (
    tree.children.append(parseList(lexed, Types.PARENTH))
    # now pointing to )
    lexed.stepUp()
    lexed.skipSpace()
    # now pointing to next ID or statement i think

    return tree


def parseAssignment(lexed: LexList) -> Node:

    # the node to return
    assignmentTree = Node("assignment")

    # expect a = sign
    lexed.expect(Types.COMPOPERATOR)

    ## TODO: make this check for equals sign here

    # down and stepDown the space to get the name
    lexed.stepDown()
    # skip space downwards
    lexed.skipSpace(True)

    # expect an ID, the name of the variable to change
    lexed.expect(Types.ID)
    # get name of variable to assign to
    assignmentTree.name = lexed.getVal()

    # skip to the equals sign, then get expression
    lexed.stepUp()
    lexed.skipSpace()

    # get value of variable
    assignmentTree.children = [parseExpression(lexed, ";")]

    # return the variable
    return assignmentTree


# parse a list, like for passing arguments, or arrays.
# bracketType:
def parseList(lexed: LexList, bracketType: Type) -> list[Node]:
    parsedList: Node = Node("list")
    # expect a [ or ( or somethign else similar
    lexed.expect(bracketType)
    # expecting a comma, like after an id or actual value is passed in
    expectingComma = False

    # skip the bracketType token, to the start of the expression
    # lexed.stepUp()
    # lexed.skipSpace()

    skipFirst = False

    while lexed.canRetrieve() and not lexed.eof() and bracketType.values[1] != lexed.getVal():

        # check if type then value is correct
        if lexed.getType() == bracketType.name and bracketType.values[1] == lexed.getVal():
            # the end of the list has been found
            break

        if expectingComma:
            # where lexed.index is pointing should be a comma.
            lexed.expect(Types.COMMA)

        # assume that the type's values have the following format: '()', '[]', '{}'.
        # add comma because the expression could break at bracketType or at an actual comma.
        # parseExpression wants to be positioned at the start of the expression
        parsedList.children.append(parseExpression(
            lexed, bracketType.values[1] + ',', skip=skipFirst))

        # now that the first loop ran, all the others must skip the commas at the start
        skipFirst = True
        # after one expression expect a comma, or the ending
        expectingComma = True

        # check if type then value is correct before stepping up
        if lexed.getType() == bracketType.name and bracketType.values[1] == lexed.getVal():
            # the end of the list has been found
            break

        # step and skip to the next expression, because it did not end here yet
        # lexed.stepUp()
        # lexed.skipSpace()

    # returns with lexed pointing to bracketType ending.
    return parsedList


# for parsing the arguments
def parseArguments(lexed: LexList) -> Node:
    # expect (
    lexed.expect(Types.PARENTH)


# ending is when to expect the ending of the expression, ie. ) or , or ;
# expectingOperator is if expecting an operator after an ID or const
### what is skip? I am not sure it is not clear.
def parseExpression(lexed: LexList, ending: str, skip=False) -> Node:

    expressionTree = Node("expression")

    expectingOperator = False

    # maybe check for all of these conditions after stepping up?
    while lexed.canRetrieve() and not lexed.eof() and (not lexed.getVal() in ending or skip):

        # stepUp for the next token
        lexed.stepUp()
        lexed.skipSpace()

        # make skip false since it should not skip again
        skip = False

        # check if it should be ended, because it is at the end of the expression
        if lexed.getVal() in ending:
            # the end of the expression
            break

        if expectingOperator:
            # this is a bs fix but idk what else to do here.
            ### i should come back to this later idk wtf im doing
            if lexed.getVal() == ")":
                # only should get here if in a function call.
                # all this is so it works correctly.
                lexed.stepUp()
                lexed.skipSpace()
                lexed.expect(Types.SEMICOL)
                break
            
            
            # expect an operator, or a parenthesis
            lexed.expect(Types.OPERATOR, Types.COMPOPERATOR)
            # create a node for the operator
            operatorNode = Node("operator")
            operatorNode.value = lexed.getVal()

            # push the node into expression
            expressionTree.children.append(operatorNode)

            # no longer expecting operator
            expectingOperator = False

            continue

        # expect a variable name, string, or number, or opening parenthesis
        lexed.expect(Types.ID, Types.STRSEP, Types.NUM, Types.PARENTH)

        # open another expression
        if lexed.getType() == "PARENTH" and lexed.getVal() == "(":
            # here, add an opening parenthesis, the expression inside, then close and add a closing parenthesis to the expression.
            # add opening parenthesis node
            openParenNode = Node("openingParenthesis")
            openParenNode.value = "("
            expressionTree.children.append(openParenNode)

            # add expression body as another expression
            expressionTree.children += parseExpression(lexed, ")").children

            # add closing parenthesis node
            closingParenNode = Node("closingParenthesis")
            closingParenNode.value = ")"
            expressionTree.children.append(closingParenNode)

            # in an expression following a symbol you need an operator
            expectingOperator = True

            # make sure that the while loop doesnt break, so skip the current token
            lexed.stepUp()
            lexed.skipSpace()

            # check if the current token is an operator. If it is then step down again.
            if lexed.getType() == "OPERATOR":
                lexed.stepDown()
            # all should be good after here

        elif lexed.getType() == "ID":
            expressionTree.children.append(parseID(lexed))

            # check if ID was a call, if so then stepback so operator can get called
            if expressionTree.children[-1].nodeName == "call":
                lexed.stepDown()

            # in an expression following a symbol you need an operator
            expectingOperator = True
            
            # what does this leave lexed pointing to?

        elif lexed.getType() == "STRSEP":
            # parse a string
            expressionTree.children.append(parseString(lexed))
            # in an expression following a symbol you need an operator
            expectingOperator = True
            # leaves lexed on top of last STRSEP token

        elif lexed.getType() == "NUM":
            # parse a number
            expressionTree.children.append(parseNumber(lexed))
            # in an expression following a symbol you need an operator
            expectingOperator = True
            # leaves lexed on top of NUM token

    # ends pointing to ending param

    # shunting yard algorithm
    # taken from wikipedia
    # slightly edited to make it work here, changed a LITTLE bit of the logic i think
    output: list[Node] = []
    operatorStack: list[Node] = []
    queue: list[Node] = expressionTree.children

    operatorsPrecedence = {
        "+": 2,
        "-": 2,
        "/": 3,
        "*": 3,
        # not sure if these would work
        "<=": 0,
        ">=": 0,
        "<": 0,
        ">": 0,
        "==": 0
    }

    for token in queue:
        if token.nodeName == "int" or token.nodeName == "string" or token.nodeName == "reference" or token.nodeName == "call":
            output.append(token)
        elif token.nodeName == "call":
            operatorStack.append(token)
        elif token.nodeName == "operator":
            while len(operatorStack) > 0 and (operatorStack[-1].nodeName == "operator") and (operatorsPrecedence[operatorStack[-1].value] >= operatorsPrecedence[token.value]) and queue[-1].nodeName != "openingParenthesis":
                output.append(operatorStack[-1])
                operatorStack.pop()
            operatorStack.append(token)
        elif token.nodeName == "openingParenthesis":
            operatorStack.append(token)
        elif token.nodeName == "closingParenthesis":
            while operatorStack[-1].nodeName != "openingParenthesis":
                output.append(operatorStack[-1])
                operatorStack.pop()
            if operatorStack[-1].nodeName == "openingParenthesis":
                operatorStack.pop()

    while operatorStack != []:
        output.append(operatorStack[-1])
        operatorStack.pop()

    expressionTree.children = output
    return expressionTree


def parseIf(lexed: LexList) -> Node:
    # starts LexList pointing to if STATEMENT token.
    lexed.expect(Types.STATEMENT)

    # the if node for the tree
    ifNode = Node("if")

    # parse the if expression all the way to {, then get the body of the if and put it as children.
    # arguments is the expression and children is the body.
    ifNode.arguments.append(parseExpression(lexed, "{"))

    ifNode.children = parseBody(lexed, "}").children

    return ifNode

def parseElse(lexed: LexList) -> Node:
    # starts LexList pointing to else STATEMENT token.
    lexed.expect(Types.STATEMENT)

    # the else node for the tree
    elseNode = Node("else")

    # after the else, skip whitespace and expect a {
    lexed.stepUp()
    lexed.skipSpace()

    # statement is for if the else is followed by an if statement
    lexed.expect(Types.CURLY_PAREN, Types.STATEMENT)
    if lexed.getType() == "CURLY_PAREN":
        # put the body of the else as children
        elseNode.children = parseBody(lexed, "}").children
    else:
        # put the body of the else as children
        elseNode.children = parseBody(lexed, "}").children
    return elseNode

def parseNumber(lexed: LexList) -> Node:
    # floats are not yet supported. I should support them eventually i will probably
    # give them their own special stack or something
    number = ""

    # expect a number since we are getting a number
    lexed.expect(Types.NUM)

    node = Node("int")
    node.value = int(lexed.getVal())

    # stops with lexed pointing to int
    return node


def parseString(lexed: LexList) -> Node:
    # expects lexed to point on top of first "
    lexed.expect(Types.STRSEP)
    # get whether the string is ' or "
    quote = lexed.getVal()
    # to check if the current string is terminated or not. ie \n \t
    terminated = False
    output = ""
    while not lexed.eof() and lexed.canRetrieve():
        # move up
        lexed.stepUp()

        # chars could be a whole token so loop through everything
        chars = lexed.getVal()

        if lexed.getType() == "NEWLINE" and not terminated:
            # this could have more space
            if '\n' in chars:
                # error
                pass

        if terminated:
            if chars == "n":
                # new line:
                output += "\\n"
            elif chars == "t":
                # tab
                output += "\\t"
            else:
                # everything else
                output += chars

        elif lexed.getVal() == "\\":
            # an escape sequence
            terminated = True
            continue

        elif lexed.getType() == "STRSEP" and quote == lexed.getVal():
            # the string has ended
            break
        else:
            output += chars
        terminated = False
    # wrap up output in node and return
    node = Node("string")
    # stops with lexer on top of STRSEP
    node.value = output
    return node

# TODO: maybe add anonymous functions to language. Not for now because that is a lot of work.


def parseFunctionDeclaration(lexed: LexList) -> Node:
    functionNode = Node("function")
    # starts with func keyword on top, then parses arguments (parseVarDeclaration on while loop??), then gets children as parseBody, then returns.
    lexed.expect(Types.STATEMENT)
    lexed.stepUp()
    lexed.skipSpace()

    # expect the name of the function here.
    lexed.expect(Types.ID)
    functionNode.name = lexed.getVal()

    # expect the @ type symbol
    lexed.stepUp()
    lexed.skipSpace()
    lexed.expect(Types.TYPEOPER)

    # expect ID, return type of function.
    lexed.stepUp()
    lexed.skipSpace()
    lexed.expect(Types.ID)
    functionNode.type = lexed.getVal()

    # expect ( for arguments
    lexed.stepUp()
    lexed.skipSpace()
    lexed.expect(Types.PARENTH)

    if lexed.getVal() != "(":
        # throw an error here
        pass

    # check if there are any arguments in function. 
    # If so do while loop, else skip over
    lexed.stepUp()

    if lexed.getVal() != ")":
        lexed.stepDown()
        # this while loop gets all the arguments.
        while lexed.getVal() != ')' and lexed.canRetrieve():
            functionNode.arguments.append(parseVarDeclaration(lexed, True))
        

    # expect the ending parenthesis
    lexed.expect(Types.PARENTH)

    # now expect the { symbol
    lexed.stepUp()
    lexed.skipSpace()
    lexed.expect(Types.CURLY_PAREN)

    if lexed.getVal() != "{":
        # throw an error here
        pass
    functionNode.children = [parseBody(lexed, "}")]

    return functionNode


def parseReturn(lexed: LexList) -> Node:
    returnNode = Node("return")

    # return an expression
    returnNode.children = [parseExpression(lexed, ';')]

    return returnNode

# parse an include, then add it to the syntax tree.
def parseInclude(lexed: LexList) -> Node:
    pass

# parse a while loop, then add it to the syntax tree.
def parseWhileLoop(lexed: LexList) -> Node:

    loopNode = Node("whileLoop")

    # expect to be pointing lexed on top of statement
    lexed.expect(Types.STATEMENT)

    # parse the expression all the way to {, then get the body of the loop and put it as children.
    # arguments is the expression and children is the body.
    loopNode.arguments.append(parseExpression(lexed, "{"))

    loopNode.children = parseBody(lexed, "}").children

    #return the loopNode
    return loopNode



# parse a for loop, then add it to the syntax tree.
def parseForLoop(lexed: LexList):
    pass


if __name__ == "__main__":
    toLex = """ 
    func sayHi@null (name@string) {
        var output@int = (12 + 14) - output;
        print(output);
    }
    sayHi(("Eric Diskin" * 5) + " Is said 5 times." - (22));
    """

    otherToLex = """
    func main@int (param@int) {
        var zero@int = 0;
        var one@int = 1;
        var two@int = 2;
        var three@int = 3;
        var four@int = 4;
    }

    """
    lexed = lex(otherToLex)
    parsed = parseBody(lexed)
    parsed.printAll()
