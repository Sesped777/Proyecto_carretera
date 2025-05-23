import numpy as np
import matplotlib.pyplot as plt

class Pieza:
    def __init__(self,i, columna):
        self.tipo = self.definir_tipo(i)
        self.angulos = self.definir_angulos()
        self.salidas = self.definir_salidas(columna)
    
    def definir_salidas(self, columna):
        salidas = []
        for i in range(32):
            if columna[i] == 1:
                salidas.append(i)
        #print(f"estas son las salidas: {salidas}")
        return salidas

    def definir_angulos(self):
        if self.tipo in (1, 4):
            return 0, None
        elif self.tipo == 2:
            return 45, None
        elif self.tipo == 3:
            return 0, 45 

    def definir_tipo(self, i):
        if i < 12:
            return 1
        elif 12 <= i < 28:
            return 2
        elif 28 <= i < 30:
            return 3
        elif 30 <= i < 32:
            return 4


    def get_salidas(self):
        return self.salidas

def diferencias(theta):
    return int(np.round(np.cos(np.deg2rad(theta)))), int(np.round(np.sin(np.deg2rad(theta))))

def posicion_nueva(x, y, theta, pieza):
    dx, dy = diferencias(theta)
    nuevo_theta = theta
    
    if pieza.tipo == 2:
        nuevo_theta = (theta + 45) % 360
    elif pieza.tipo == 3:
        nuevo_theta = (theta + 90) % 360
    
    nuevo_x = x + dx
    nuevo_y = y + dy
    
    return nuevo_x, nuevo_y, nuevo_theta

    

def Construir_pista(matriz):
    pista = []
    x, y, theta = 0, 0, 0  # posición y ángulo inicial
    i = 0  # pieza inicial
    
    pieza_actual = Pieza(i, matriz[i])
    nuevo_x, nuevo_y, nuevo_theta = posicion_nueva(x, y, theta, pieza_actual)
    pista.append((i, pieza_actual.tipo, (x, y), (nuevo_x, nuevo_y)))
    salidas = pieza_actual.get_salidas()

    if len(salidas) == 1:
        # pista lineal normal
        while salidas:
            i = salidas[0]
            x, y, theta = nuevo_x, nuevo_y, nuevo_theta
            pieza_actual = Pieza(i, matriz[i])
            nuevo_x, nuevo_y, nuevo_theta = posicion_nueva(x, y, theta, pieza_actual)
            pista.append((i, pieza_actual.tipo, (x, y), (nuevo_x, nuevo_y)))
            salidas = pieza_actual.get_salidas()
            print("...")
    elif len(salidas) == 2:
        # pista con bifurcación
        i1, i2 = salidas
        x1, y1, theta1 = nuevo_x, nuevo_y, nuevo_theta
        x2, y2, theta2 = nuevo_x, nuevo_y, nuevo_theta
        salidas_1 = [i1]
        salidas_2 = [i2]

        while (x1, y1) != (x2, y2):
            if salidas_1:
                i1 = salidas_1.pop(0)
                pieza_1 = Pieza(i1, matriz[i1])
                nuevo_x1, nuevo_y1, nuevo_theta1 = posicion_nueva(x1, y1, theta1, pieza_1)
                pista.append((i1, pieza_1.tipo, (x1, y1), (nuevo_x1, nuevo_y1)))
                x1, y1, theta1 = nuevo_x1, nuevo_y1, nuevo_theta1
                salidas_1.extend(pieza_1.get_salidas())
            
            if salidas_2:
                i2 = salidas_2.pop(0)
                pieza_2 = Pieza(i2, matriz[i2])
                nuevo_x2, nuevo_y2, nuevo_theta2 = posicion_nueva(x2, y2, theta2, pieza_2)
                pista.append((i2, pieza_2.tipo, (x2, y2), (nuevo_x2, nuevo_y2)))
                x2, y2, theta2 = nuevo_x2, nuevo_y2, nuevo_theta2
                salidas_2.extend(pieza_2.get_salidas())
            print("...")
            # Romper el bucle si alguna pista se quedó sin piezas o se cruzaron
            if not salidas_1 or not salidas_2:
                break

    return pista

        
def graficar_pista(pista):
    for (id_pieza, tipo, inicio, fin) in pista:
        x_vals = [inicio[0], fin[0]]
        y_vals = [inicio[1], fin[1]]
        
        if tipo in (1, 4):
            plt.plot(x_vals, y_vals, 'b-', marker='o')
        elif tipo == 2:
            plt.plot(x_vals, y_vals, 'g--', marker='o')
        elif tipo == 3:
            plt.plot(x_vals, y_vals, 'r-.', marker='o')
        
        plt.text(inicio[0], inicio[1], f"{id_pieza}-{tipo}", fontsize=8, ha='center', va='center')

    plt.grid(True)
    plt.axis('equal')
    plt.title("Pista construida")
    plt.show()

