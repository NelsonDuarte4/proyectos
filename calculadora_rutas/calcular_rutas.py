from collections import deque   # Importa deque, una cola eficiente para BFS
import random                   

def crear_mapa(filas, columnas, cantidad_obstaculos, cantidad_alternativos):
    mapa = []  

    for i in range(filas):
        fila = []                 
        for j in range(columnas):
            fila.append(0)        
        mapa.append(fila)         

    # Obstáculos permanentes 
    creados = 0
    while creados < cantidad_obstaculos:
        x = random.randint(0, filas - 1)      # Fila aleatoria
        y = random.randint(0, columnas - 1)   # Columna aleatoria
        if mapa[x][y] == 0:                   # Solo se coloca si es camino normal
            mapa[x][y] = 1                    # Se convierte en obstáculo
            creados += 1                      # Aumenta contador

    # Caminos alternativos 
    creados = 0
    while creados < cantidad_alternativos:
        x = random.randint(0, filas - 1)
        y = random.randint(0, columnas - 1)
        if mapa[x][y] == 0:                   # Solo se coloca sobre camino normal
            mapa[x][y] = 2                    # Se marca como camino alternativo
            creados += 1

    return mapa   

def mostrar_mapa(mapa, ruta=None, inicio=None, destino=None):
    for i in range(len(mapa)):             
        for j in range(len(mapa[0])):      
            posicion = (i, j)              # Guarda la posición actual como tupla

            # Se imprime según prioridad visual
            if posicion == inicio:
                print("E", end=" ")        
            elif posicion == destino:
                print("S", end=" ")        
            elif ruta and posicion in ruta:
                print("*", end=" ")        
            elif mapa[i][j] == 0:
                print(".", end=" ")        
            elif mapa[i][j] == 2:
                print("~", end=" ")        
            elif mapa[i][j] == 3:
                print("T", end=" ")        
            else:
                print("X", end=" ")       
        print()  
    print()      

def coordenada_valida(x, y, mapa):
    # Verifica que la coordenada esté dentro de los límites del mapa
    return 0 <= x < len(mapa) and 0 <= y < len(mapa[0])

def pedir_coordenada(mensaje, mapa):
    # Pide coordenadas hasta que el usuario ingrese una válida
    while True:
        x = int(input(f"Fila {mensaje}: "))      
        y = int(input(f"Columna {mensaje}: "))   

        if not coordenada_valida(x, y, mapa):
            print(" Fuera del mapa.")  # Está fuera de los límites
        elif mapa[x][y] == 1:
            print(" Hay un obstáculo.")  # Es obstáculo permanente
        elif mapa[x][y] == 3:
            print(" Zona bloqueada temporalmente.")  # Es bloque temporal
        else:
            return (x, y)   # Devuelve la coordenada válida

def bloques_temporales(mapa, cantidad):
    agregados = 0

    while agregados < cantidad:
        print(f"\nBloque temporal {agregados + 1} de {cantidad}")

        x = int(input("Fila del bloque temporal: "))
        y = int(input("Columna del bloque temporal: "))

        if not coordenada_valida(x, y, mapa):
            print(" Fuera del mapa.")
        elif mapa[x][y] == 1:
            print(" Hay un obstáculo.")
        elif mapa[x][y] == 3:
            print(" Ya es una zona bloqueada.")
        elif mapa[x][y] == 2:
            print(" Es un camino alternativo.")
        else:
            mapa[x][y] = 3    
            agregados += 1
            print(" Bloque temporal agregado.")

def buscar_ruta_bfs(mapa, inicio, destino):
    cola = deque() 
    cola.append((inicio, [inicio]))  # Se guarda posición y camino recorrido
    visitado = set() 
    visitado.add(inicio)             # Marca la posición inicial como visitada

    # Mientras haya posiciones por explorar
    while cola:                      
        posicion_actual, camino = cola.popleft()  # FIFO 

        if posicion_actual == destino:
            return camino            

        x, y = posicion_actual
        movimientos = [(1,0), (-1,0), (0,1), (0,-1)]  

        # Explora los vecinos
        for dx, dy in movimientos:
            nx = x + dx              
            ny = y + dy              
            nueva = (nx, ny)         

            if coordenada_valida(nx, ny, mapa):  
                if mapa[nx][ny] not in (1, 3) and nueva not in visitado:
                    visitado.add(nueva)            # Marca como visitado
                    cola.append((nueva, camino + [nueva]))  
                    # Agrega a la cola con el nuevo camino actualizado

    return None   

filas = int(input("Filas del mapa: "))
columnas = int(input("Columnas del mapa: "))
cantidad_obstaculos = int(input("Cantidad de obstáculos: "))
cantidad_alternativos = int(input("Cantidad de caminos alternativos: "))

mapa = crear_mapa(filas, columnas, cantidad_obstaculos, cantidad_alternativos)

print("\nMapa generado:")
mostrar_mapa(mapa)

inicio = pedir_coordenada("de entrada (E)", mapa)
destino = pedir_coordenada("de salida (S)", mapa)

while True:
    ruta = buscar_ruta_bfs(mapa, inicio, destino)

    if ruta:
        print("\nRuta más corta encontrada:")
        mostrar_mapa(mapa, ruta, inicio, destino)
    else:
        print("❌ No se encontró una ruta posible.")

    opcion = input("¿Recalcular ruta? (s/n): ").lower()
    if opcion != "s":
        print("Programa finalizado.")
        break

    agregar = input("¿Desea agregar bloques temporales? (s/n): ").lower()
    if agregar == "s":
        cantidad = int(input("Cantidad de bloques temporales a agregar: "))
        bloques_temporales(mapa, cantidad)

        print("\nMapa actualizado:")
        mostrar_mapa(mapa)

        continue  # Vuelve al inicio del while y recalcula ruta

    cambiar = input("¿Desea cambiar la salida? (s/n): ").lower()
    if cambiar == "s":
        destino = pedir_coordenada("de salida (S)", mapa)
