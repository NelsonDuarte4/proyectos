import heapq
import random

# ==============================================================================
# CLASE MAPA
# ==============================================================================
    # TODO: Crear método constructor que reciba 'dim'
    # TODO: Guardar dim en atributo self.dim
    # TODO: Guardar dim en atributo self.filas
    # TODO: Guardar dim en atributo self.cols
    # TODO: Crear matriz tablero llena de ceros usando comprensión de listas
    # TODO: Inicializar self.inicio en None
    # TODO: Inicializar self.meta en None
class Mapa:
    def __init__(self, dim):
        self.dim = dim
        self.filas = dim
        self.cols = dim
        self.tablero = [[0 for _ in range(dim)]for _ in range(dim)]
        self.inicio = None
        self.meta = None

    # TODO: Crear método generar_obstaculos_aleatorios que reciba 'cantidad'
    # TODO: Crear variable creados = 0
    # TODO: Hacer bucle while creados < cantidad
    # TODO: Generar rf aleatorio entre 0 y self.dim - 1
    # TODO: Generar rc aleatorio entre 0 y self.dim - 1
    # TODO: Si self.tablero[rf][rc] == 0
    # TODO: Asignar a self.tablero[rf][rc] random.choice([1, 2])
    # TODO: Incrementar creados
    def generar_obstaculos_aleatorios(self, cantidad):
        creados = 0
        while creados < cantidad:
            rf = random.randint(0, self.dim - 1)
            rc = random.randint(0, self.dim - 1)
            
            if self.tablero[rf][rc] == 0:
                self.tablero[rf][rc] = random.choice([1, 2])
                creados += 1

    # TODO: Crear método set_inicio que reciba f, c
    # TODO: Guardar tupla (f, c) en self.inicio
    # TODO: Marcar self.tablero[f][c] = 9
    def set_inicio(self,f, c):
        self.inicio = (f, c)
        self.tablero[f][c] = 9

    # TODO: Crear método set_meta que reciba f, c
    # TODO: Guardar tupla (f, c) en self.meta
    # TODO: Marcar self.tablero[f][c] = 8
    def set_meta(self,f, c):
        self.meta = (f, c)
        self.tablero[f][c] = 9

    # TODO: Crear método dibujar que reciba camino=[]
    # TODO: Crear diccionario iconos con los valores: 0:"⬜", 1:"🟥", 2:"🟦", 3:"🟥", 8:"🟨", 9:"🟧"
    # TODO: Convertir camino a set y guardar en camino_set
    # TODO: Imprimir encabezado de columnas
    # TODO: Hacer bucle for f in range(self.filas)
    # TODO: Imprimir número de fila
    # TODO: Hacer bucle for c in range(self.cols)
    # TODO: Si (f, c) está en camino_set, imprimir "🟩" con end=" "
    # TODO: Sino, obtener val de self.tablero[f][c] e imprimir iconos.get(val, "?")
    # TODO: Hacer salto de línea después de cada fila
    def dibujar(self,camino=[]):
        iconos = {0:"⬜", 1:"🟥", 2:"🟦", 3:"🟥", 8:"🟨", 9:"🟧"}
        camino_set = set(camino)

        print("   ", end = " ")
        for c in range(self.cols):
            print(c, end = " ")
        print()

        for f in range(self.filas):
            print(f, end = " ")
            for c in range(self.cols):
                if (f, c) in camino_set:
                    print("🟩", end = " ")
                else:
                    val = self.tablero[f][c]
                    print(iconos.get(val, "?"), end = " ")
            print()

# ==============================================================================
# CLASE CALCULADORA DE RUTAS
# ==============================================================================

    # TODO: Crear método _movimientos que reciba f, c, mapa
    # TODO: Crear lista vacía movs
    # TODO: Crear lista direcciones con [(-1,0), (1,0), (0,-1), (0,1)]
    # TODO: Hacer bucle for df, dc in direcciones
    # TODO: Calcular nf = f + df
    # TODO: Calcular nc = c + dc
    # TODO: Si 0 <= nf < mapa.filas y 0 <= nc < mapa.cols
    # TODO: Agregar tupla (nf, nc) a movs
    # TODO: Retornar movs
class CalculadorasDeRutas():
    def _movimientos(self, f, c, mapa):
        movs = []
        direcciones = [(-1,0), (1,0), (0,-1), (0,1)]
       
        for df, dc in direcciones:
            nf = f + df
            nc = c + dc

            if 0 <= nf < mapa.filas and 0 <= nc < mapa.cols:
                movs.append((nf, nc))
        return movs

    # TODO: Crear método encontrar_camino que reciba mapa
    # TODO: Obtener start de mapa.inicio
    # TODO: Obtener end de mapa.meta
    # TODO: Crear cola con [(0, start[0], start[1], [start])]
    # TODO: Crear set visitados vacío
    # TODO: Hacer bucle while len(cola) > 0
    # TODO: Hacer heapq.heappop(cola) y desempaquetar en costo, f, c, camino
    # TODO: Si (f, c) == end, retornar camino, costo
    # TODO: Si (f, c) está en visitados, hacer continue
    # TODO: Agregar (f, c) a visitados usando add()
    # TODO: Hacer bucle for nf, nc in self._movimientos(f, c, mapa)
    # TODO: Obtener terreno de mapa.tablero[nf][nc]
    # TODO: Inicializar peso = 0 y se_puede = False
    # TODO: Si terreno == 0 o terreno == 8 o terreno == 9: peso = 1 y se_puede = True
    # TODO: Si terreno == 2: peso = 5 y se_puede = True
    # TODO: Si se_puede y (nf, nc) no está en visitados
    # TODO: Hacer heapq.heappush(cola, (costo + peso, nf, nc, camino + [(nf, nc)]))
    # TODO: Al final del método, retornar [], 0
    def encontrar_camino(self, mapa):
        start = mapa.inicio
        end = mapa.meta

        cola = [(0, start[0], start[1], [start])]
        visitados = set()

        while len(cola) > 0:
            costo, f, c, camino = heapq.heappop(cola)

            if (f, c) == end:
                return camino, costo
            
            if (f, c) in visitados:
                continue

            visitados.add((f, c))

            for nf, nc in self._movimientos(f, c, mapa):
                terreno = mapa.tablero[nf][nc]
                peso = 0
                se_puede = False

                if terreno == 0 or terreno == 8 or terreno == 9:
                    peso = 1
                    se_puede = True
                
                if terreno == 2:
                    peso = 5
                    se_puede = True
                
                if se_puede and (nf, nc) not in visitados:
                    heapq.heappush(cola, (costo + peso, nf, nc, camino + [(nf, nc)]))
        return [], 0


# ==============================================================================
# FUNCIÓN MAIN
# ==============================================================================
def main():

    # TODO: Pedir al usuario el tamaño del tablero y guardarlo en una variable 'dim' (usar int e input)
    dim = int(input("ingrese el tamaño del tablero: "))
    # TODO: Instanciar la clase Mapa pasando 'dim' como argumento. Guardarlo en la variable 'mi_mapa'
    mi_mapa = Mapa(dim)

    # TODO: Pedir la cantidad de obstáculos y guardarlo en 'cant'
    cant = int(input("ingrese la cantidad de obstaculos: "))
   
    # TODO: Llamar al método generar_obstaculos_aleatorios de 'mi_mapa' pasando 'cant'
    mi_mapa.generar_obstaculos_aleatorios(cant)

    # TODO: Llamar al método dibujar de 'mi_mapa' para mostrar el escenario inicial
    mi_mapa.dibujar()
    # TODO: Pedir coordenadas de inicio (Fila Columna) y guardarlas.
    # TODO: Llamar a mi_mapa.set_inicio(f_ini, c_ini)
    f_ini, c_ini = map(int, input("ingresa la fila y la columna con un espacio (fila columna): ").split())
    mi_mapa.set_inicio(f_ini, c_ini)

    # TODO: Pedir coordenadas de meta (Fila Columna) y guardarlas en f_meta, c_meta
    # TODO: Llamar a mi_mapa.set_meta(f_meta, c_meta)
    f_meta, c_meta = map(int, input("ingresa la fila y la columna con un espacio (fila columna): ").split())
    mi_mapa.set_meta(f_meta, c_meta)

    # --- Lógica de la Calculadora ---
    
    # TODO: Instanciar la clase CalculadoraDeRutas y guardarla en la variable 'calc'
    calc = CalculadorasDeRutas()
    # TODO: Llamar al método encontrar_camino de 'calc' pasándole 'mi_mapa' como argumento
    calc.encontrar_camino(mi_mapa)
    # TODO: Guardar los resultados en: ruta, costo
    ruta, costo = calc.encontrar_camino(mi_mapa)
    # --- Resultados ---
    
    # TODO: Imprimir el costo total de la ruta
    print("\n costo total ", costo)
    mi_mapa.dibujar(ruta) 
    print("ruta encontrada", ruta)
    # TODO: Llamar al método mi_mapa.dibujar(ruta) pasando la ruta encontrada
    # TODO: Imprimir la lista de coordenadas de la ruta

if __name__ == "__main__":
    main()