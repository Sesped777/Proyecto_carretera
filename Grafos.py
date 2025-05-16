import networkx as nx
import matplotlib.pyplot as plt
import numpy as np 
def matriz_adyacencia_a_grafo(matriz, dirigido=False):
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
