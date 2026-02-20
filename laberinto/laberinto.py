import os
import time

columnas = 8
filas = 8
max_turnos = 30
tiempo = 0.5
profundidad = 3

movimientos = [(-1,0),(1,0),(0,-1),(0,1)]

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def distancia(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def validar(posicion):
    lugares = []
    for dx, dy in movimientos:
        nueva = (posicion[0]+dx, posicion[1]+dy)
        if 0 <= nueva[0] < filas and 0 <= nueva[1] < columnas:
            lugares.append(nueva)
    return lugares

def mostrar(gato, raton, turno):
    limpiar()
    print("Turno:", turno, "/", max_turnos)
    for f in range(filas):
        fila = ""
        for c in range(columnas):
            if (f,c) == gato:
                fila += "G "
            elif (f,c) == raton:
                fila += "R "
            else:
                fila += ". "
        print(fila)
    time.sleep(tiempo)

def puntos(gato, raton):
    if gato == raton:
        return 100
    return 50 - distancia(gato, raton)

def Minimax(gato, raton, profundidad, turno_gato):
    if profundidad == 0 or gato == raton:
        return puntos(gato, raton)
# se calcula el mejor y peor moviemiento que puede tener el gato 
    if turno_gato:
        mejor = -999
        for A in validar(gato):
            valor = Minimax(A, raton, profundidad - 1, False)
            mejor = max(mejor, valor)
        return mejor
    else:
        peor = 999
        for A in validar(raton):
            valor = Minimax(gato, A, profundidad - 1, True)
            peor = min(peor, valor)
        return peor

# mover gato usando minimax
def mover_gato(gato, raton, gato_antes):
    mejor = gato
    mejor_puntos = -999

    for A in validar(gato):
        penal = -10 if A == gato_antes else 0  # evita que mi gato baile
        valor = Minimax(A, raton, profundidad, False) + penal

        if valor > mejor_puntos:
            mejor_puntos = valor
            mejor = A

    return mejor

# mover ratón escapando 
def mover_raton(raton, gato, raton_antes):
    opciones = validar(raton)
    opciones = [m for m in opciones if m != raton_antes] or opciones

    mejor = opciones[0]
    mejor_distancia = distancia(mejor, gato)

    for pos in opciones:
        dist = distancia(pos, gato)
        if dist > mejor_distancia:
            mejor = pos
            mejor_distancia = dist

    return mejor

# juego principal
def jugar():
    gato = (0,0)
    raton = (filas-1, columnas-1)   

    gato_antes = None
    raton_antes = None

    for turno in range(1, max_turnos+1):
        mostrar(gato, raton, turno)

        gato_nuevo = mover_gato(gato, raton, gato_antes)
        gato_antes = gato
        gato = gato_nuevo

        if gato == raton:
            mostrar(gato, raton, turno)
            print("\nEL GATO ATRAPÓ AL RATÓN 😼")
            return

        raton_nuevo = mover_raton(raton, gato, raton_antes)
        raton_antes = raton
        raton = raton_nuevo

        if gato == raton:
            mostrar(gato, raton, turno)
            print("\nEL RATÓN FUE ATRAPADO 🐭")
            return

    print("\nEL RATÓN ESCAPÓ!")

jugar()
