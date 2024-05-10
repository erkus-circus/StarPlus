import lexer
import codeGeneration
from actionTree import parseCalls, parseConstants, parseExpressions, parseFunctions, functions, constants, totalVariablesList
from syntaxTree import parseBody
import actionTree
from debugging import DebugFlags


def build(inputProgram: str, filePath="") -> str:
    lexed = lexer.lex(inputProgram, filePath=filePath)
    if DebugFlags.showLexedTokens:
        print ("================= LEXED TOKENS =================")
        lexed.printOut()

    # create the abstract syntax tree
    ast = parseBody(lexed)
    if DebugFlags.showPreAST:
        print("================= PRE PROCESSED AST ======================")
        ast.printAll()




    # create the action tree
    parseFunctions(ast)
    parseCalls(ast)
    parseConstants(ast)
    parseExpressions(ast)
    
    # parseVariables(ast)

    if DebugFlags.showPostAST:
        print("================= POST PROCESSED AST ======================")
        # print the Action Tree
        ast.printAll()

    # add index for constants, variables, and functions.
    # for i in range(max(max(len(variables), len(constants)), len(functions))):
    for i in range(max(max(max(totalVariablesList), len(constants)), len(functions))):
        if not i in constants:
            constants.append(i)
    if DebugFlags.showConstantsLists:
        # make the variable index and constant index constants:
        print ("================= FUNCTIONS, CONSTANTS (pre-code generation) =================")
        print("Functions: ", functions)
        print("Constants: ", constants)


    # crete code generation.
    return (codeGeneration.createCode(ast, actionTree.functions, actionTree.functionData, actionTree.constants))

# build("""

# func createName: string (nameParam: string, lastNameParam: string) {
#     var output: string;
#     output = nameParam + lastNameParam;
# }

# func main: int (returnStatus: int) {
#     var myName: string = "Eric";
#     var lastName: string = "Diskin";
#     var fullName: string = myName + lastName;

#     myName = createName(lastName, "Ilana");
#     print(fullName);
# }
# """, 0)

# build("""
# func main: int (param: string) {
#     print("Hello");
# }
# """, 0)


## an example if statement could be:
