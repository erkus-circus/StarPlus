#include <vector>


class Function {
    private:
    int num_args;
    // the number of instructions in the 
    int num_instructions;
    // the variables vector
    std::vector<int> variables;

    int pc;
    Function(int nargs, int ninstructions, std::vector<int> vars) {

    }
};

std::vector<Function> functions;

// function for setting the functions array
void set_functions(unsigned char* file, unsigned int index, unsigned int fileSize);