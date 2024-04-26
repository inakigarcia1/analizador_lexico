# 0: Entero
# 1: Real
# 2: Parentesis
# 3: Operadores
# ERROR_LEXICO: Otro

# Estados AFD
Q0 = 0  # Comienzo
Q1 = 1  # Cero inicial
Q2 = 2  # Parentesis
Q3 = 3  # Operador
Q4 = 4  # Entero
Q5 = 5  # Punto
Q6 = 6  # Real
Q7 = 7  # Sumidero

# Definir tabla de transicion
tabla_transicion = [[Q1, Q4, Q3, Q2, Q5, Q7],
                    [Q1, Q1, Q3, Q2, Q5, Q7],
                    [Q1, Q4, Q3, Q2, Q5, Q7],
                    [Q1, Q4, Q3, Q2, Q5, Q7],
                    [Q4, Q4, Q3, Q2, Q5, Q7],
                    [Q6, Q6, Q3, Q2, Q5, Q7],
                    [Q6, Q6, Q3, Q2, Q5, Q7],
                    [Q1, Q4, Q3, Q2, Q5, Q7]]

# Definir estados finales
estados_finales = [Q2, Q3, Q4, Q6]

# Definir simbolos especificos
operadores = ['+', '-', '/', '*']
parentesis = ['(', ')']

# Solicitar archivo de entrada
nombre_archivo = input("Nombre del archivo a leer (TXT): ")

# Agregar extension .txt si el usuario no lo hizo
if ".txt" not in nombre_archivo:
    nombre_archivo += ".txt"

# Abrir archivo en modo lectura
try:
    archivo = open(nombre_archivo, 'r')
except FileNotFoundError:
    print("Error, archivo no encontrado.")
    exit()

# Lineas del archivo
lineas_originales = archivo.readlines()

# Lineas finales
lineas = []

# Separar Tokens por espacios en blanco y saltos de linea
espacio = " "
indice = 0

for linea in lineas_originales:
    if espacio in linea:
        separado = linea.split()
        for token in separado:
            lineas.insert(indice, token)
            indice += 1

    else:
        lineas.append(linea)

    indice += 1

# Eliminar \n
for linea in lineas:
    if '\n' in linea:
        lineas[lineas.index(linea)] = linea.replace("\n", "")


# Funcion para comprobar si un estado es final
def es_final(estado):
    if estado in estados_finales:
        return True
    else:
        return False


# Funcion para determinar el token type de una entrada
def get_token_type(simbolo):
    if simbolo.isdigit():

        if simbolo == '0':
            return 0

        if 1 <= int(simbolo) <= 9:
            return 1

    if simbolo in operadores:
        return 2

    if simbolo in parentesis:
        return 3

    if simbolo == '.':
        return 4

    return 5


# Funcion para transformar un estado a String (salida)
def transformar(Q):
    if Q == 2:
        return 'Parentesis'

    if Q == 3:
        return 'Operador'

    if Q == 4:
        return 'Entero'

    if Q == 6:
        return 'Real'


# Programa principal
salidas = []
lineas_finales = []

ubicacion_actual = 0
Q = Q0  # Estado inicial Q0
Q1 = Q0  # Estado del simbolo siguiente
simbolos = ''  # String del lexema
falso_real = False  # Numero real que empieza por cero
for token in lineas:

    for simbolo in token:
        token_type = get_token_type(simbolo)  # Obtener token type del simbolo leido
        simbolos += simbolo  # Agregar simbolo al string del lexema
        Q = tabla_transicion[Q][token_type]  # Transicionar
        try:
            ubicacion_siguiente = ubicacion_actual + 1
            sig_simbolo = token[ubicacion_siguiente]
            token_type = get_token_type(sig_simbolo)
            Q1 = tabla_transicion[Q][token_type]
            if Q != Q1:
                if Q == 5 and (Q1 == 1 or Q1 == 4):
                    continue

                if Q == 4 and Q1 == 5:
                    continue

                if Q == 1 and Q1 == 5:
                    falso_real = True
                    break

                if Q == 3 and Q1 == 4:
                    continue

                if Q == 3 and Q1 == 1:
                    continue

                if es_final(Q):
                    token_type = transformar(Q)
                    salida = f"( {simbolos}, {token_type})"
                    salidas.append(salida)
                    simbolos = ''
                else:
                    salida = f"( {simbolos}, ERROR_LEXICO)"
                    # print(sig_simbolo)
                    salidas.append(salida)
                    simbolos = ''

        except IndexError:
            continue

        ubicacion_actual += 1

    if falso_real:
        salida = f"( {token}, ERROR_LEXICO)"
        salidas.append(salida)
        simbolos = ''
        falso_real = False

    elif es_final(Q):
        token_type = transformar(Q)
        salida = f"( {simbolos}, {token_type})"
        salidas.append(salida)
        simbolos = ''

    else:
        salida = f"( {simbolos}, ERROR_LEXICO)"
        salidas.append(salida)
        simbolos = ''

    lineas_finales.append(salidas)
    salidas = []
    Q = Q0
    ubicacion_actual = 0

archivo_salida = open("salida.txt", "w")

token_completo = ""
for linea in lineas_finales:
    for token in linea:
        token_completo += token + " "

    archivo_salida.write(token_completo)
    archivo_salida.write('\n')
    token_completo = ""

print("Proceso finalizado, resultado guardado en salida.txt")
