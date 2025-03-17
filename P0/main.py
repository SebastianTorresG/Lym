
"""
Sebastian Torres - 202223811
Sofia Rodriguez - 202222588
"""


import parser as p

def main():
    a = "codigo_entrada.txt"
    #input("Escriba el nombre del archivo de entrada incluyendo el .txt \n(el archivo debe estar en la misma carpeta que este archivo): ")
    X = p.check_syntax("P0/"+ a)
    if X == "NO":
        return False
    else:
        return True
print("El programa retorno: "+ str(main()))
    