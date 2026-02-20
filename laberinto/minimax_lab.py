import random
import os
import time

FILAS = 12
COLUMNAS = 12
NUM_OBSTACULOS = 20

PROFUNDIDAD_GATO = 6      # Qué tan lejos ve el gato en el futuro (profundidad del Minimax)

TURNOS_MAXIMOS = 20
RATON_RANDOM_FASE = 5     # Requisito: fase inicial aleatoria donde el ratón se mueve al azar
RETRASO = 0.5

MOVIMIENTOS = [
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

obstaculos = set()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def generar_obstaculos(gato, raton):
    global obstaculos
    obstaculos = set()
    # Genera obstáculos aleatorios evitando pisar al gato o al ratón
    while len(obstaculos) < NUM_OBSTACULOS:
        obs = (random.randint(0, FILAS - 1), random.randint(0, COLUMNAS - 1))
        if obs not in (gato, raton):
            obstaculos.add(obs)

def mostrar_tablero(gato, raton, movimientos_raton):
    limpiar_pantalla()
    print(f"--- El gato y el ratón (TÚ) -- Turno: {movimientos_raton}/{TURNOS_MAXIMOS} ---")
    
    for f in range(FILAS):
        fila = ""
        for c in range(COLUMNAS):
            pos = (f, c)
            if pos == gato:         fila += "G "
            elif pos == raton:      fila += "R "
            elif pos in obstaculos: fila += "# "
            else:                   fila += ". "
        print(fila)
    print()

def distancia_manhattan(p1, p2):
    # Distancia Manhattan = suma de diferencias absolutas
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def movimientos_validos(pos):  # Retorna lista de coordenadas válidas desde la posición actual
    validos = []
    for dx, dy in MOVIMIENTOS:
        nueva_posicion = (pos[0] + dx, pos[1] + dy)
        # Validación de límites + evitar obstáculos
        if (0 <= nueva_posicion[0] < FILAS and
            0 <= nueva_posicion[1] < COLUMNAS and
            nueva_posicion not in obstaculos):
            validos.append(nueva_posicion)
    return validos

def evaluar_estado(gato, raton):
    # Si el gato alcanza al ratón → mejor situación posible
    if gato == raton:
        return 10000

    distancia = distancia_manhattan(gato, raton)
    mov_gato = len(movimientos_validos(gato))   
    mov_raton = len(movimientos_validos(raton))

    # Puntuación base del estado (a menor distancia, mejor para el gato)
    return (100 - distancia * 10) + (mov_gato - mov_raton)

def minimax(gato, raton, profundidad, alpha, beta):
    # fin de recursión o captura
    if profundidad == 0 or gato == raton:
        return evaluar_estado(gato, raton), gato

    mejor_movimiento = gato
    maxima_evaluacion = float('-inf')

    # Ordene los movimientos para mejorar la poda Alpha-Beta
    opciones = sorted(movimientos_validos(gato), key=lambda m: distancia_manhattan(m, raton))

    for movimiento in opciones:
        eval_val, _ = minimax(movimiento, raton, profundidad - 1, alpha, beta)

        if eval_val > maxima_evaluacion:   # El Minimax le da el mejor movimiento encontrado
            maxima_evaluacion = eval_val
            mejor_movimiento = movimiento

        alpha = max(alpha, eval_val)
        if beta <= alpha:   # Poda
            break

    return maxima_evaluacion, mejor_movimiento

def turno_gato_minimax(gato, raton):
    # si puede capturarte en un movimiento, lo hace
    if raton in movimientos_validos(gato):
        return raton

    distancia = distancia_manhattan(gato, raton)

    if distancia > 4:    # persecución directa cuando está lejos
        opciones = movimientos_validos(gato)
        if opciones:
            # Se mueve hacia la posición que más reduce la distancia
            return min(opciones, key=lambda m: distancia_manhattan(m, raton))
        return gato

    # Cuando está cerca usa Minimax para estrategia mas directa
    _, movimiento = minimax(gato, raton, PROFUNDIDAD_GATO, float('-inf'), float('inf'))
    return movimiento

def turno_raton_humano(raton):
    mapa_teclas = {
        'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1),
        'q': (-1, -1), 'e': (-1, 1), 'z': (1, -1), 'c': (1, 1)
    }
    print("Mueve con: W, A, S, D (o diagonales Q, E, Z, C)")
    
    while True:
        tecla = input("Tu movimiento: ").lower()
        if tecla in mapa_teclas:
            dx, dy = mapa_teclas[tecla]
            nuevo = (raton[0] + dx, raton[1] + dy)
            
            if nuevo in movimientos_validos(raton):
                return nuevo
            print("¡Movimiento bloqueado o fuera del mapa!")
        else:
            print("Tecla inválida.")

def juego():
    gato = (0, 0)
    raton = (FILAS-1, COLUMNAS-1)
    
    generar_obstaculos(gato, raton)
    movimientos_raton = 0
    
    while movimientos_raton < TURNOS_MAXIMOS:
        mostrar_tablero(gato, raton, movimientos_raton)

        # 2. Movimiento del gato 
        print("El gato está pensando...")
        gato = turno_gato_minimax(gato, raton)
        
        if gato == raton:
            mostrar_tablero(gato, raton, movimientos_raton)
            print("\n ¡TE ATRAPÓ! Fin del juego.")
            return

        mostrar_tablero(gato, raton, movimientos_raton)
        time.sleep(RETRASO)

        # 3. Movimiento del ratón
        if movimientos_raton < RATON_RANDOM_FASE:
            print(f"Fase Aturdida ({RATON_RANDOM_FASE - movimientos_raton} turnos): Te mueves al azar.")
            opciones = movimientos_validos(raton)
            raton = random.choice(opciones) if opciones else raton
            time.sleep(1)
        else:
            raton = turno_raton_humano(raton)

        if gato == raton:
            print("\n ¡Te suicidaste!")
            return

        movimientos_raton += 1

    print("\n ¡ESCAPASTE! El tiempo se agotó y el gato se rindió.")

if __name__ == "__main__":
    juego()
