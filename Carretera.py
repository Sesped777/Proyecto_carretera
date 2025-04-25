# importamos las librererias necesarias y configuramos manim, libreria necesaria para animaciones
import numpy as np
import pandas as pd
import random
from manim import *
import networkx as nx
import matplotlib.pyplot as plt

config.media_width = "100%"

# Declaramos las contantes, las cantidades de piezas de cada tipo
RECTAS = 12
CURVAS = 16
DISECCION_1 = 2
DISECCION_2 = 2

#Inicializamos estado inicial, una matriz identidad de 32 x 32
estado_inicial = np.eye(32)


def verificar_suma_columnas(matriz):
    # Verificar las primeras 28 columnas (índices 0 a 27)
    for j in range(28):
        suma_columna = np.sum(matriz, axis=0) - np.diag(matriz)
        if suma_columna > 2:
            print(f"Columna {j+1}: suma = {suma_columna} (debe ser ≤ 2)")
            return False
    
    # Verificar las columnas 29 a 32 (índices 28 a 31)
    for j in range(28, 32):
        suma_columna = sum(matriz[Ai][j] for i in range(32))
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
    sumas_columnas, sumas_filas = sumas_ejes(matriz)
    print(f"suma de las filas\n{sumas_filas} \n sumas de las columnas\n{sumas_columnas} \n ================================")
    # Buscar columnas válidas
    for i in rango_1:
        if sumas_columnas[i] == 0:
            for j in rango_2:
                if sumas_filas[j] == 0:
                    if i != j and (matriz[i][j] < 1 and matriz[j][i] < 1):
                        return i,j
    
    return None


def matriz_adyacencia_a_grafo_sin_diagonal(matriz, dirigido=False):
    """Convierte matriz de adyacencia (NumPy o lista) a grafo de NetworkX, ignorando la diagonal"""
    # Verificar si es un array de NumPy y convertirlo si es necesario
    if isinstance(matriz, np.ndarray):
        matriz = matriz
    else:
        try:
            matriz = np.array(matriz)
        except:
            return nx.DiGraph() if dirigido else nx.Graph()
    
    # Verificar si la matriz está vacía (manera correcta para NumPy)
    if matriz.size == 0:
        return nx.DiGraph() if dirigido else nx.Graph()
    
    # Crear el grafo
    G = nx.DiGraph() if dirigido else nx.Graph()
    num_nodos = matriz.shape[0]
    G.add_nodes_from(range(num_nodos))
    
    # Encontrar índices donde hay conexiones (ignorando diagonal)
    rows, cols = np.where((matriz != 0) & (~np.eye(num_nodos, dtype=bool)))
    
    # Añadir aristas
    for i, j in zip(rows, cols):
        if not dirigido and i < j:  # Para grafos no dirigidos, evitar duplicados
            G.add_edge(i, j, weight=float(matriz[i, j]))
        elif dirigido:
            G.add_edge(i, j, weight=float(matriz[i, j]))
    
    return G
    

def dibujar_grafo(grafo):
    """Función de dibujo"""
    if not isinstance(grafo, (nx.Graph, nx.DiGraph)):
        raise TypeError("El objeto debe ser un grafo de NetworkX")
    
    if len(grafo.nodes()) == 0:
        print("El grafo está vacío")
        return
    
    plt.figure(figsize=(12, 10))
    
    # Usar un layout diferente para grafos grandes
    if len(grafo.nodes()) > 20:
        pos = nx.kamada_kawai_layout(grafo)
    else:
        pos = nx.spring_layout(grafo, k=0.15, iterations=50)
    
    nx.draw(grafo, pos, with_labels=True, 
            node_color='lightblue', 
            node_size=500, 
            edge_color='gray',
            width=1.5,
            font_size=8)
    
    try:
        nx.draw_networkx_edges(grafo, pos, font_size=7)
    except:
        pass
    
    plt.tight_layout()
    plt.show()


def Funcion_transicion(estado, accion):
    """Función de transición modificada para evitar modificar el estado original"""
    estado = estado.copy()  # Crear una copia para no modificar el original
    coordenada = Casilla_valida(estado, accion[0], accion[1])
    if coordenada is not None:
        estado[coordenada[0], coordenada[1]] = 1
    return estado

# Funcion para hacer una accion
def Accion():
    return random.randint(1,4), random.randint(1,4)



estado_inicial = np.eye(32)
estado_sig = estado_inicial
for i in range(100):
    accion = Accion()
    print(f"Accion: {accion}")
    estado_actual = estado_sig
    estado_sig = Funcion_transicion(estado_actual, accion)