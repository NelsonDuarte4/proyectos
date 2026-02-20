from collections import deque
import random

class Mapa:
    def __init__(self, filas, columnas, cantidad_obstaculos, cantidad_alternativos):
        self.filas = filas
        self.columnas = columnas
        
        # Se crea una matriz inicial llena de 0 (espacios libres)
        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
        
        # Se generan obstáculos y caminos alternativos
        self._generar_obstaculos(cantidad_obstaculos)
        self._generar_alternativos(cantidad_alternativos)

    def _generar_obstaculos(self, cantidad):
        creados = 0
        while creados < cantidad:
            x = random.randint(0, self.filas - 1)
            y = random.randint(0, self.columnas - 1)

            # Solo se coloca si la celda está vacía
            if self.matriz[x][y] == 0:
                self.matriz[x][y] = 1
                creados += 1

    def _generar_alternativos(self, cantidad):
        creados = 0
        while creados < cantidad:
            x = random.randint(0, self.filas - 1)
            y = random.randint(0, self.columnas - 1)

            if self.matriz[x][y] == 0:
                self.matriz[x][y] = 2
                creados += 1

    def coordenada_valida(self, x, y):
        return 0 <= x < self.filas and 0 <= y < self.columnas

    def es_accesible(self, x, y):
        return self.coordenada_valida(x, y) and self.matriz[x][y] not in (1, 3)

    def agregar_bloque_temporal(self, x, y):
        if self.coordenada_valida(x, y) and self.matriz[x][y] == 0:
            self.matriz[x][y] = 3
            return True
        return False

    def mostrar(self, ruta=None, inicio=None, destino=None):
        for i in range(self.filas):
            for j in range(self.columnas):
                posicion = (i, j)

                if posicion == inicio:
                    print("E", end=" ")
                elif posicion == destino:
                    print("S", end=" ")
                elif ruta and posicion in ruta:
                    print("*", end=" ")
                elif self.matriz[i][j] == 0:
                    print(".", end=" ")
                elif self.matriz[i][j] == 2:
                    print("~", end=" ")
                elif self.matriz[i][j] == 3:
                    print("T", end=" ")
                else:
                    print("X", end=" ")
            print()
        print()

class AlgoritmoBusqueda:
    def buscar(self, mapa, inicio, destino):
        raise NotImplementedError("Debe implementar el método buscar.")

class BFS(AlgoritmoBusqueda):
    def buscar(self, mapa, inicio, destino):
        cola = deque()
        
        # Se guarda la posición actual y el camino recorrido
        cola.append((inicio, [inicio]))

        visitado = set()
        visitado.add(inicio)

        while cola:
            posicion_actual, camino = cola.popleft()

            # Si llegamos al destino, retornamos el camino
            if posicion_actual == destino:
                return camino

            x, y = posicion_actual

            # Movimientos posibles (abajo, arriba, derecha, izquierda)
            movimientos = [(1,0), (-1,0), (0,1), (0,-1)]

            for dx, dy in movimientos:
                nx = x + dx
                ny = y + dy
                nueva = (nx, ny)

                # Verificamos si es accesible y no fue visitada
                if mapa.es_accesible(nx, ny) and nueva not in visitado:
                    visitado.add(nueva)
                    cola.append((nueva, camino + [nueva]))

        # Si no se encuentra camino
        return None

class CalculadoraDeRutas:
    def __init__(self, mapa, algoritmo):
        
        # Recibe el mapa y el algoritmo de búsqueda a utilizar.
        self.mapa = mapa
        self.algoritmo = algoritmo

    def calcular(self, inicio, destino):
        
        # Ejecuta el algoritmo de búsqueda.
        return self.algoritmo.buscar(self.mapa, inicio, destino)

def pedir_coordenada(mensaje, mapa):
    while True:
        x = int(input(f"Fila {mensaje}: "))
        y = int(input(f"Columna {mensaje}: "))

        if not mapa.coordenada_valida(x, y):
            print(" Fuera del mapa.")
        elif mapa.matriz[x][y] == 1:
            print(" Hay un obstáculo.")
        elif mapa.matriz[x][y] == 3:
            print(" Zona bloqueada temporalmente.")
        else:
            return (x, y)

def main():
    filas = int(input("Filas del mapa: "))
    columnas = int(input("Columnas del mapa: "))
    cantidad_obstaculos = int(input("Cantidad de obstáculos: "))
    cantidad_alternativos = int(input("Cantidad de caminos alternativos: "))

    mapa = Mapa(filas, columnas, cantidad_obstaculos, cantidad_alternativos)

    print("\nMapa generado:")
    mapa.mostrar()

    inicio = pedir_coordenada("de entrada (E)", mapa)
    destino = pedir_coordenada("de salida (S)", mapa)

    algoritmo = BFS()
    calculadora = CalculadoraDeRutas(mapa, algoritmo)

    while True:
        ruta = calculadora.calcular(inicio, destino)

        if ruta:
            print("\nRuta más corta encontrada:")
            mapa.mostrar(ruta, inicio, destino)
        else:
            print("❌ No se encontró una ruta posible.")

        opcion = input("¿Recalcular ruta? (s/n): ").lower()
        if opcion != "s":
            print("Programa finalizado.")
            break

        agregar = input("¿Desea agregar bloques temporales? (s/n): ").lower()
        if agregar == "s":
            cantidad = int(input("Cantidad de bloques temporales a agregar: "))
            agregados = 0

            while agregados < cantidad:
                print(f"\nBloque temporal {agregados + 1} de {cantidad}")
                x = int(input("Fila del bloque temporal: "))
                y = int(input("Columna del bloque temporal: "))

                if mapa.agregar_bloque_temporal(x, y):
                    print(" Bloque temporal agregado.")
                    agregados += 1
                else:
                    print(" No se pudo agregar el bloque.")

            print("\nMapa actualizado:")
            mapa.mostrar()

            continue

        cambiar = input("¿Desea cambiar la salida? (s/n): ").lower()
        if cambiar == "s":
            destino = pedir_coordenada("de salida (S)", mapa)


# Punto de entrada del programa
if __name__ == "__main__":
    main()
