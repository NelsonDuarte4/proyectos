import heapq
import random

# ==============================================================================
# CLASE MAPA
# ==============================================================================

class Mapa:

    def __init__(self, dim):
        self.dim = dim
        self.filas = dim
        self.cols = dim
        self.tablero = [[0 for _ in range(dim)] for _ in range(dim)]
        self.inicio = None
        self.meta = None

    def generar_obstaculos_aleatorios(self, cantidad):
        creados = 0
        while creados < cantidad:
            rf = random.randint(0, self.dim - 1)
            rc = random.randint(0, self.dim - 1)

            if self.tablero[rf][rc] == 0:
                self.tablero[rf][rc] = random.choice([1, 2])
                creados += 1

    def set_inicio(self, f, c):
        self.inicio = (f, c)
        self.tablero[f][c] = 9

    def set_meta(self, f, c):
        self.meta = (f, c)
        self.tablero[f][c] = 8

    def dibujar(self, camino=[]):
        iconos = {
            0: "⬜",
            1: "🟥",
            2: "🟦",
            3: "🟥",
            8: "🟨",
            9: "🟧"
        }

        camino_set = set(camino)

        print("\n   ", end="")
        for c in range(self.cols):
            print(c, end=" ")
        print()

        for f in range(self.filas):
            print(f, end="  ")
            for c in range(self.cols):
                if (f, c) in camino_set:
                    print("🟩", end=" ")
                else:
                    val = self.tablero[f][c]
                    print(iconos.get(val, "?"), end=" ")
            print()


# ==============================================================================
# CLASE CALCULADORA DE RUTAS
# ==============================================================================

class CalculadoraDeRutas:

    def _movimientos(self, f, c, mapa):
        movs = []
        direcciones = [(-1,0), (1,0), (0,-1), (0,1)]

        for df, dc in direcciones:
            nf = f + df
            nc = c + dc

            if 0 <= nf < mapa.filas and 0 <= nc < mapa.cols:
                movs.append((nf, nc))

        return movs

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
                    heapq.heappush(
                        cola,
                        (costo + peso, nf, nc, camino + [(nf, nc)])
                    )

        return [], 0


# ==============================================================================
# FUNCIÓN MAIN
# ==============================================================================

def main():

    dim = int(input("Ingrese tamaño del tablero: "))
    mi_mapa = Mapa(dim)

    cant = int(input("Ingrese cantidad de obstáculos: "))
    mi_mapa.generar_obstaculos_aleatorios(cant)

    mi_mapa.dibujar()

    f_ini, c_ini = map(int, input("Ingrese inicio (fila columna): ").split())
    mi_mapa.set_inicio(f_ini, c_ini)

    f_meta, c_meta = map(int, input("Ingrese meta (fila columna): ").split())
    mi_mapa.set_meta(f_meta, c_meta)

    calc = CalculadoraDeRutas()
    ruta, costo = calc.encontrar_camino(mi_mapa)

    print("\nCosto total de la ruta:", costo)
    mi_mapa.dibujar(ruta)
    print("Ruta encontrada:", ruta)


if __name__ == "__main__":
    main()