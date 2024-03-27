""""
Creates a data section for a assembly script

Eric Diskin
Created on: 3/11/21
"""

# takes data from a data.txt file in this directory with the following format:

"""
[N|S] [number or string]
  for example for the number 42:
N 42
  or for the string, "Hello World!"
S Hello World!
  strings can be escaped using \\'s. for example:
S hello my name is eric. \n i like eating food.
F 123.122
F 12.542123
"""



"""
Format:

Number of constants: unsigned integer

For each constant: 2 bits to specify if it is an int, float, or string
If int:
4 Bytes long
If string:
Unsigned int with length n of string in bytes
a set of bytes n long with values of the string
If float:
1 bit sign
"""



def bytesFromNumber(number: int): 
    hexString = hex(number)[2:]
    lengthToPad = len(hexString)
    zeros = (8 - lengthToPad) * '0'
    hexString = zeros + hexString
    
    n = 2

    return "0x" + '\n0x'.join([hexString[i:i+n] for i in range(0, len(hexString), n)])
  

def formatNumber(line):
  out = ""

  # number of bytes per Data block (4)
  out += "0x04 ; Four Bytes per Data block\n"

  # if this is a number, only one Data value is needed
  out += bytesFromNumber(1) + ' ; This constant [INDEX: ' + str(numberLines - 1) + ']\n'
  # the actual number
  out += bytesFromNumber(int(line.split()[1])) + " ; Number: " + line.split()[1] + '\n'
  return out

# 1 byte from number
def byteFromNumber(number: int):
  if number > 127:
    print("ERROR!!!!?????")
  return hex(number)

def formatString(line):
  # get rid of "S "
  # TODO: Does \\n get replaced?
  line = line[2:].replace('\\t', '\t').replace('\\n', '\n')
  
  # use 1 byte spacers
  out = "0x01 ; One Byte per Data block\n"
  
  # length of the string is how many bytes this is going to take up
  out += bytesFromNumber(len(line)) + ' ; This constant [INDEX: ' + str(numberLines - 1) + '] takes up (' +  str(len(line)) + ') bytes\n'
  for i in line:
    out += byteFromNumber(ord(i)) + ' ; Char: \'' + i.replace('\t', '\\t').replace('\n', '\\n') + '\'\n'
  
  return out

numberLines = 0

def createData(text) -> str:
  global numberLines
  output = ""
  for i in text.splitlines():
      i = i.replace('\\n', '\n').replace('\\t', '\t')
      if i[0] == ";":
        continue
      if i[0] == "S":
          numberLines += 1
          output += formatString(i)
      else:
          numberLines += 1
          output += formatNumber(i)


  output = str(bytesFromNumber(numberLines)) + ' ; ' + str(numberLines) + ' Constants:\n' + output
  return output
