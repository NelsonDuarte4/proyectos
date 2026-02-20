#include <iostream>   
#include <vector>     
#include <queue>      // Permite usar colas (BFS usa una cola)
#include <cstdlib>    // rand(), srand()
#include <ctime>      
using namespace std;  // Evita escribir std:: antes de cada cosa

int filas = 10, columnas = 10;

// Mapa del laberinto (matriz de caracteres)
vector<vector<char>> laberinto;

void imprimir() {
    for(int i = 0; i < filas; i++) {
        for(int j = 0; j < columnas; j++)
            // Imprime cada celda del laberinto
            cout << laberinto[static_cast<size_t>(i)][static_cast<size_t>(j)];
        
        cout << endl;
    }
}

void crear() {      // Llena todo el laberinto con muros ('#')

    laberinto.assign(static_cast<size_t>(filas),
                     vector<char>(static_cast<size_t>(columnas), '#'));
    
    int posX = 0, posY = 0;  // Camino inicial

    // Primera celda marcado como camino
    laberinto[0][0] = '*';
    
    while(posX < filas-1 || posY < columnas-1) {  // se valida que siempre haya un camino a la salida

        if(rand() % 2 && posX < filas-1) posX++; // Mueve hacia abajo 
        // Elige al azar si baja o va a la derecha, sin salirse del tablero
        else if(posY < columnas-1) posY++; // O hacia la derecha
        
        // Marca como camino
        laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = '*';
    }
    
    // Abre caminos aleatorios dentro del laberinto
    for(int i = 1; i < filas-1; i++)
        for(int j = 1; j < columnas-1; j++)
            if(rand() % 5 == 0)  // 1 de cada 3 veces se cumple
                laberinto[static_cast<size_t>(i)][static_cast<size_t>(j)] = '*';
    
    // Marca la entrada (E)
    laberinto[0][0] = 'E';

    // Marca SALIDA (S)
    laberinto[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)] = 'S';
}

void resolver() {  // BFS 

    // Marca qué posiciones ya fueron visitadas  // primera bandera 
    vector<vector<bool>> visitado(static_cast<size_t>(filas),
                                   vector<bool>(static_cast<size_t>(columnas), false));

    // Guarda las filas y columnas en las que ya se llego 
    vector<vector<pair<int,int>>> anterior(static_cast<size_t>(filas),
        vector<pair<int,int>>(static_cast<size_t>(columnas), {-1,-1}));  //para indicar que aún no se llegó a esa posición

    // dato tipo cola para BFS
    queue<pair<int,int>> cola;
    
    
    cola.push({0,0});  // push agg el elemento al final de la lista 
    visitado[0][0] = true;  // para que no se vuelva a procesar en el recorrido
    
    // Mientras haya posiciones por explorar // segunda bandera
    while(!cola.empty()) {

        // Obtiene la posición actual
        int posX = cola.front().first;
        int posY = cola.front().second;
        cola.pop(); 
        
        // Direcciones posibles: abajo, arriba, derecha, izquierda
        int direccionX[] = {1,-1,0,0};
        int direccionY[] = {0,0,1,-1};
        
        // Recorre los 4 movimientos
        for(int i = 0; i < 4; i++) {

            int nuevaX = posX + direccionX[i];
            int nuevaY = posY + direccionY[i];
            
            // Verifica:
            // 1. Que esté dentro del mapa
            // 2. Que no haya sido visitado
            // 3. Que no sea un muro
            if(nuevaX >= 0 && nuevaX < filas &&
               nuevaY >= 0 && nuevaY < columnas &&
               !visitado[static_cast<size_t>(nuevaX)][static_cast<size_t>(nuevaY)] &&
               laberinto[static_cast<size_t>(nuevaX)][static_cast<size_t>(nuevaY)] != '#') {

                // Marca como visitado
                visitado[static_cast<size_t>(nuevaX)][static_cast<size_t>(nuevaY)] = true;

                // Guarda de dónde viene (para reconstruir camino)
                anterior[static_cast<size_t>(nuevaX)][static_cast<size_t>(nuevaY)] = {posX, posY};

                // Agrega a la cola
                cola.push({nuevaX, nuevaY});
            }
        }
    }
    
    // Si no se visitó la salida, no hay solución
    if(!visitado[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)]) {
        cout << "No hay solucion" << endl;
        return;
    }
    
    int posX = filas-1, posY = columnas-1;   // RECONSTRUIR CAMINO

    // Retrocede desde la salida hasta el inicio
    while(posX != 0 || posY != 0) {
        
        // Obtiene la posición previa
        int prevX = anterior[static_cast<size_t>(posX)][static_cast<size_t>(posY)].first;
        int prevY = anterior[static_cast<size_t>(posX)][static_cast<size_t>(posY)].second;

        // Marca el camino de solución
        if(laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] == '*')
            laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = 'o';

        // Retrocede
        posX = prevX;
        posY = prevY;
    }
    
    // vuelvo a inicializar el inicio y salida
    laberinto[0][0] = 'E';
    laberinto[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)] = 'S';
}

int main(int argc, char* argv[]) {

    // Inicializa semilla aleatoria
    srand(time(0));
    
    // Permite recibir filas y columnas por parámetros del programa
    if(argc == 3) {
        filas = stoi(argv[1]);
        columnas = stoi(argv[2]);
    }
    
    // Tiempo de inicio de generación
    clock_t tiempo1 = clock();
    crear();
    clock_t tiempo2 = clock();

    // Tiempo de resolución
    resolver();
    clock_t tiempo3 = clock();
    
    // Muestra el laberinto final
    imprimir();
    
    // Muestra tiempos en milisegundos
    cout << endl << "Tiempo generar: "
         << (tiempo2-tiempo1)*1000.0/CLOCKS_PER_SEC << " ms" << endl;

    cout << "Tiempo resolver: "
         << (tiempo3-tiempo2)*1000.0/CLOCKS_PER_SEC << " ms" << endl;
    
    return 0;
}