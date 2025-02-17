import re
file = "P0/codigo_entrada.txt"

def read_file(filename):
    with open(filename, "r") as file:
        return file.read().strip()



def tokenize(code):
    token_patterns = [
        (r"\|[a-zA-Z0-9_ ]+\|", "VARIABLES"),
        (r"proc [a-z][a-zA-Z0-9_]*:?(\s+[a-z][a-zA-Z0-9_]*(:\s+[a-z][a-zA-Z0-9_]*)*)?", "PROCEDURE_DEF"),
        (r"[a-z][a-zA-Z0-9_]*:?(\s+[a-z][a-zA-Z0-9_]*)*.", "PROCEDURE_CALL"),
        (r"[a-z][a-zA-Z0-9_]*\s*:=\s*[0-9]+.", "ASSIGNMENT"),
        (r"if:\s+[a-zA-Z0-9_]+\s+then:\s+\[.*?\]\s+else:\s+\[.*?\]", "IF_STATEMENT"),
        (r"while:\s+[a-zA-Z0-9_]+\s+do:\s+\[.*?\]", "WHILE_LOOP"),
        (r"repeatTimes:\s+for:\s+[0-9]+\s+repeat:\s+\[.*?\]", "REPEAT_LOOP"),
        (r"move:\s+[0-9]+\s+inDir:\s+#(north|south|west|east).", "MOVE"),
        (r"put:\s+[0-9]+\s+ofType:\s+#(balloons|chips).", "PUT"),
        (r"pick:\s+[0-9]+\s+ofType:\s+#(balloons|chips).", "PICK"),
        (r"\[", "BLOCK_START"),
        (r"\]", "BLOCK_END"),
        (r"\.", "DOT")
    ]
    
    tokens = []
    for pattern, token_type in token_patterns:
        matches = re.findall(pattern, code)
        for match in matches:
            tokens.append((match, token_type))
    
    return tokens

def parse(tokens):
    defined_procedures = set()
    defined_variables = set()
    
    for token, token_type in tokens:
        if token_type == "VARIABLES":
            variables = token.strip("|").split()
            defined_variables.update(variables)

        elif token_type == "PROCEDURE_DEF":
            proc_name = token.split()[1].rstrip(":")
            defined_procedures.add(proc_name)

        elif token_type == "PROCEDURE_CALL":
            proc_name = token.split()[0].rstrip(":")
            if proc_name not in defined_procedures:
                return "NO"

        elif token_type == "ASSIGNMENT":
            var_name = token.split(":=")[0].strip()
            if var_name not in defined_variables:
                return "NO"

    return "YES"

def check_syntax(filename):
    code = read_file(filename)
    tokens = tokenize(code)
    result = parse(tokens)
    print(result)


check_syntax(file)

