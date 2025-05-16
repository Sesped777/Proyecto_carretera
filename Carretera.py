# importamos las librererias necesarias y configuramos manim, libreria necesaria para animaciones
import numpy as np
import pandas as pd
import random
from Grafos import matriz_adyacencia_a_grafo,dibujar_grafo

# Declaramos las contantes, las cantidades de piezas de cada tipo
RECTAS = 5
CURVAS = 0
DISECCION_1 = 0
DISECCION_2 = 0
TAM_MATRIZ = RECTAS + CURVAS + DISECCION_1 + DISECCION_2

def verificar_suma_columnas(matriz):
    # Verificar las primeras 28 columnas (índices 0 a 27)
    for j in range(RECTAS + CURVAS):
        suma_columna = np.sum(matriz, axis=0) - np.diag(matriz)
        if suma_columna > 2:
            print(f"Columna {j+1}: suma = {suma_columna} (debe ser ≤ 2)")
            return False
    
    # Verificar las columnas 29 a 32 (0índices 28 a 31)
    for j in range(RECTAS + CURVAS, TAM_MATRIZ):
        suma_columna = sum(matriz[i][j] for i in range(32))
        if suma_columna > 3:
            print(f"Columna {j+1}: suma = {suma_columna} (debe ser ≤ 3)")
            return False
    return True

def sumas_ejes(matriz):
        return np.sum(matriz, axis=0) - np.diag(matriz), np.sum(matriz, axis=1) - np.diag(matriz) 

def rangos(tipo):
    if tipo == 1:
        return range(RECTAS)
    elif tipo == 2:
        return range(RECTAS, RECTAS + CURVAS)
    elif tipo == 3:
        return range(RECTAS + CURVAS, RECTAS + CURVAS + DISECCION_1)
    elif tipo == 4:
        return range(RECTAS + CURVAS + DISECCION_1,RECTAS + CURVAS + DISECCION_1 + DISECCION_1)
    else:
        return None
    
def Casilla_valida(matriz, tipo_1, tipo_2):
    # Definir el rango de búsqueda
    rango_1 = rangos(tipo_1)
    rango_2 = rangos(tipo_2)
    # Calcular sumas (excluyendo diagonal)
    sumas_columnas ,sumas_filas= sumas_ejes(matriz)
    print(f"suma de las filas\n{sumas_filas} \n sumas de las columnas\n{sumas_columnas} \n")
    # Buscar columnas válidas
    for i in rango_1:
        if sumas_columnas[i] == 0:
            print(f"suma de la columna: {sumas_columnas[i]} en la columna {i}")
            for j in rango_2:
                if sumas_filas[j] == 0:
                    print(f"suma de la fila: {sumas_filas[j]} en la fila {j}")
                    if i != j and (matriz[i][j] == 0  and matriz[j][i] == 0):
                        print(f" i : {i}, j : {j}")
                        return j,i
    
    return None

def Funcion_transicion(estado, accion):
    """Función de transición modificada para evitar modificar el estado original"""
    estado = estado.copy()  # Crear una copia para no modificar el original
    coordenada = Casilla_valida(estado, accion[0], accion[1])
    if coordenada is not None:
        estado[coordenada[0], coordenada[1]] = 1
    return estado

# Funcion para hacer una accion
def Accion(a = 1, b = 4):
    return random.randint(a,b), random.randint(a,b)



if __name__ == '__main__':
    estado_inicial = np.eye(TAM_MATRIZ)
    estado_actual = estado_inicial
    print (estado_actual)
    for i in range(10):
        accion = Accion(1,1)
        print(f"====================================== \nAccion: {accion}")
        estado_sig = Funcion_transicion(estado_actual, accion)
        estado_actual = estado_sig
        print(estado_sig)
    grafo = matriz_adyacencia_a_grafo(estado_sig,True)
    dibujar_grafo(grafo)