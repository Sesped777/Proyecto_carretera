# importamos las librererias necesarias y configuramos manim, libreria necesaria para animaciones
import numpy as np
import random
from Grafos import matriz_adyacencia_a_grafo,dibujar_grafo,es_conexo

# Declaramos las contantes, las cantidades de piezas de cada tipo
RECTAS = 12
CURVAS = 16
DISECCION_1 = 2
DISECCION_2 = 2
TAM_MATRIZ = RECTAS + CURVAS + DISECCION_1 + DISECCION_2

def sumas (matriz):
    return np.sum(np.sum(matriz, axis=0) - np.diag(matriz))

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
    rango_1 = rangos(tipo_1)
    rango_2 = rangos(tipo_2)
    sumas_columnas, sumas_filas = sumas_ejes(matriz)

    for i in rango_1:
        # Definir límite de conexiones para el tipo de nodo
        limite_i = 2 if tipo_1 == 3 else 1  # o algún otro valor si querés limitar otros
        if sumas_columnas[i] < limite_i:
            for j in rango_2:
                limite_j = 2 if tipo_2 == 4 else 1
                if sumas_filas[j] < limite_j:
                    if i != j and matriz[i][j] == 0 and matriz[j][i] == 0:
                        return j, i
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
    conexividad = False 
    gen = 0
    suma = 0 
    MAX_GEN = 5000  # seguridad para evitar loop infinito

    while not conexividad: #while not conexividad or suma != 42 :
        estado_inicial = np.eye(TAM_MATRIZ)
        estado_actual = estado_inicial.copy()

        for _ in range(1000):
            accion = Accion()
            estado_sig = Funcion_transicion(estado_actual, accion)
            estado_actual = estado_sig

        grafo = matriz_adyacencia_a_grafo(estado_sig, True)
        conexividad = es_conexo(grafo)
        suma = sumas(estado_sig)
        gen += 1

        print(f"Generación: {gen} \n Suma conexiones: {suma} \n Es conexo? {conexividad}")
    dibujar_grafo(grafo)
   
