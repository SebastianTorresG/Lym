import re

"""
Sebastian Torres - 202223811
Sofia Rodriguez - 202222588
"""


"""Por favor, indicar el nombre del archivo de entrada en la variable """
file = "P0/codigo_entrada.txt"

SPC = r"\s"
POINT = r"\."
END = rf"{SPC}{POINT}"
NUM = r"[0-9]"  
ALFMIN = r"[a-z]" 
ALFMAY = r"[A-Z]"
ID = rf"{ALFMIN}({ALFMIN}|{ALFMAY}|{NUM})*"
DECVAR = rf"({ID}{SPC})*{ID}"
ASSVAR = rf"{ID}{SPC}:=({SPC}({NUM}|{ID}))"
DIR90 = r"#left|#right|#around"
DIR = r"#front|#back|#left|#right"
COMPAS = r"#north|#south|#west|#east"
CONSTANT = r"#balloons|#chips" 

GOTO = rf"goto:{SPC}{ID}{SPC}with:{SPC}{ID}"
M_J = rf"(move|jump):{SPC}({NUM}|{ID})"
TURN = rf"turn{SPC}:{SPC}{DIR90}"
FACE = rf"face{SPC}:{SPC}{COMPAS}"
OFTYPE = rf"{SPC}ofType:{SPC}*{CONSTANT}"
NOP = r"nop"
M_JTOTHE = rf"{M_J}{SPC}toThe:{SPC}{DIR}"
M_JINDIR = rf"{M_J}{SPC}inDir:{SPC}{COMPAS}"
P_POFTYPE = rf"(put|pick):{SPC}({NUM}|{ID}){OFTYPE}"

INSTR = rf"({GOTO}|{M_J}|{TURN}|{FACE}|{NOP}|{M_JTOTHE}|{M_JINDIR}|{P_POFTYPE}){END}"

FACING = rf"facing:{SPC}{COMPAS}"
CANP_P = rf"can(Put|Pick):{SPC}{OFTYPE}"
CAN_MJ_INDIR = rf"can(Move|Jump):{SPC}inDir:{SPC}{COMPAS}"
CAN_MJ_TOTHE = rf"can(Move|Jump):{SPC}toThe:{SPC}{DIR}"
INCONDICION = rf"({FACING}|{CANP_P}|{CAN_MJ_INDIR}|{CAN_MJ_TOTHE}){END}"
NOT = rf"not:{SPC}{INCONDICION}{END}"
FULLCOND = rf"({INCONDICION}|{NOT})"

BLOCK = rf"\[({INSTR}{SPC})*\]"
IF_ELSE = rf"if{SPC}:{SPC}{FULLCOND}{SPC}then{SPC}:{SPC}{BLOCK}{SPC}else{SPC}:{SPC}{BLOCK}"
WHILE = rf"while{SPC}:{SPC}{FULLCOND}{SPC}do{SPC}:{SPC}{BLOCK}"
REPEAT = rf"for{SPC}:{SPC}({NUM}+|{ID}){SPC}repeat{SPC}:{SPC}{BLOCK}"

# Instrucciones incluyendo condicionales y bucles
INSTR = rf"({GOTO}|{M_J}|{TURN}|{FACE}|{NOP}|{M_JTOTHE}|{M_JINDIR}|{P_POFTYPE}|{IF_ELSE}|{WHILE}|{REPEAT}){END}"



def read_file(filename):
    with open(filename, "r") as file:
        return file.read().strip()



def tokenize(code):
    token_patterns = [
        (IF_ELSE, "IF_ELSE"),
        (WHILE, "WHILE"),
        (REPEAT, "REPEAT"),
        (INSTR, "INSTRUCTION"),
        (DECVAR, "DECLARATION"),
        (ASSVAR, "ASSIGNMENT"),
        (BLOCK, "BLOCK")
    ]
    
    tokens = []
    for pattern, token_type in token_patterns:
        matches = re.findall(pattern, code)
        for match in matches:
            tokens.append((match, token_type))
    
    return tokens


def parse(tokens):
    defined_variables = set()
    defined_procedures = set() 

    for token, token_type in tokens:
        # Almacenar las variables declaradas
        if token_type == "DECLARATION":
            variables = token[0].strip("|").split()
            defined_variables.update(variables)

        # Almacenar los procedimientos declarados
        elif token_type == "PROC_DECLARATION":
            proc_name = token[0].split()[1].rstrip(":")  
            defined_procedures.add(proc_name)

        # Verificar asignaciones de variables
        elif token_type == "ASSIGNMENT":
            var_name = token[0].split(":=")[0].strip()
            if var_name not in defined_variables:
                return "NO"

        # Verificar llamadas a procedimientos
        elif token_type == "PROC_CALL":
            proc_name = token[0].split()[0].rstrip(":") 
            if proc_name not in defined_procedures:
                return "NO"  
    return "YES"



def check_syntax(filename):
    code = read_file(filename)
    tokens = tokenize(code)
    result = parse(tokens)
    return result



