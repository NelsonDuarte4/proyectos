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

    # TODO: Crear método generar_obstaculos_aleatorios que reciba 'cantidad'
    # TODO: Crear variable creados = 0
    # TODO: Hacer bucle while creados < cantidad
    # TODO: Generar rf aleatorio entre 0 y self.dim - 1
    # TODO: Generar rc aleatorio entre 0 y self.dim - 1
    # TODO: Si self.tablero[rf][rc] == 0
    # TODO: Asignar a self.tablero[rf][rc] random.choice([1, 2])
    # TODO: Incrementar creados

    # TODO: Crear método set_inicio que reciba f, c
    # TODO: Guardar tupla (f, c) en self.inicio
    # TODO: Marcar self.tablero[f][c] = 9

    # TODO: Crear método set_meta que reciba f, c
    # TODO: Guardar tupla (f, c) en self.meta
    # TODO: Marcar self.tablero[f][c] = 8

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

# ==============================================================================
# FUNCIÓN MAIN
# ==============================================================================
def main():

    # TODO: Pedir al usuario el tamaño del tablero y guardarlo en una variable 'dim' (usar int e input)

    # TODO: Instanciar la clase Mapa pasando 'dim' como argumento. Guardarlo en la variable 'mi_mapa'

    # TODO: Pedir la cantidad de obstáculos y guardarlo en 'cant'
   
    # TODO: Llamar al método generar_obstaculos_aleatorios de 'mi_mapa' pasando 'cant'

    # TODO: Llamar al método dibujar de 'mi_mapa' para mostrar el escenario inicial
   
    # TODO: Pedir coordenadas de inicio (Fila Columna) y guardarlas.
    
    # TODO: Pedir coordenadas de meta (Fila Columna) y guardarlas en f_meta, c_meta
    
    # --- Lógica de la Calculadora ---
    
    # TODO: Instanciar la clase CalculadoraDeRutas y guardarla en la variable 'calc'
    
    # TODO: Llamar al método encontrar_camino de 'calc' pasándole 'mi_mapa' como argumento
    # TODO: Guardar los resultados en: ruta, costo
    
    # --- Resultados ---
    
    # TODO: Imprimir el costo total de la ruta
    # TODO: Llamar al método mi_mapa.dibujar(ruta) pasando la ruta encontrada
    # TODO: Imprimir la lista de coordenadas de la ruta

if __name__ == "__main__":
    main()