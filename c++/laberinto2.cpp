#include <iostream>   
#include <vector>     
#include <queue>      // Permite usar colas (BFS usa una cola)
#include <cstdlib>    // rand(), srand()
#include <ctime>      
using namespace std;  // Evita escribir std:: antes de cada cosa

int filas = 15, columnas = 15;

// Mapa del laberinto (matriz de caracteres)
vector<vector<char>> laberinto;

void imprimir() {
    for(int i = 0; i < filas; i++) {
        for(int j = 0; j < columnas; j++) {
            // Imprime cada celda del laberinto
            cout << laberinto[static_cast<size_t>(i)][static_cast<size_t>(j)] << ' ';
        }
        cout << endl;
    }
}

void crear() {      // Llena todo el laberinto con muros ('#')
    laberinto.assign(static_cast<size_t>(filas),
                     vector<char>(static_cast<size_t>(columnas), '#'));
    
    // Marcar los lugares ya visitados para no volver a recorrerlo  // primera bandera
    vector<vector<bool>> visitado(static_cast<size_t>(filas),
                                   vector<bool>(static_cast<size_t>(columnas), false));
    
    // Cola de celdas para la generacion de mis muros
    vector<pair<int,int>> fronteras;
    
    int posX = 0, posY = 0;  // Camino inicial

    // luego marco como camino validos con "*"
    laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = '*';
    visitado[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = true;
    
    // Direcciones posibles: abajo, arriba, derecha, izquierda
    int direccionX[] = {2, -2, 0, 0};
    int direccionY[] = {0, 0, 2, -2};
    
    // se recorren las direciones y se cargan en las posiciones 
    for(int i = 0; i < 4; i++) {
        int nuevaX = posX + direccionX[i];
        int nuevaY = posY + direccionY[i];
        
        if(nuevaX >= 0 && nuevaX < filas && nuevaY >= 0 && nuevaY < columnas) {
            fronteras.push_back({nuevaX, nuevaY});
        }
    }
    // "size" devuelve un número entero con la cantidad de elementos del vector.
    while(!fronteras.empty()) {
        
        // Elegir una frontera aleatoria
        int indice = static_cast<int>(rand() % fronteras.size());  //corrobora que la posición es válida sin salirte del vector
        posX = fronteras[indice].first;
        posY = fronteras[indice].second;
        
        // Remover de fronteras
        fronteras.erase(fronteras.begin() + indice);
        
        // Si ya fue visitada, continuar
        if(visitado[static_cast<size_t>(posX)][static_cast<size_t>(posY)])
            continue;
        
        // Buscar vecinos ya visitados (caminos)
        vector<pair<int,int>> vecinosCamino;
        
        for(int i = 0; i < 4; i++) {
            int nuevaX = posX + direccionX[i];
            int nuevaY = posY + direccionY[i];
            
            if(nuevaX >= 0 && nuevaX < filas && 
               nuevaY >= 0 && nuevaY < columnas &&
               visitado[static_cast<size_t>(nuevaX)][static_cast<size_t>(nuevaY)]) {
                vecinosCamino.push_back({nuevaX, nuevaY});
            }
        }
        
        // Si hay vecinos camino, conectar
        if(!vecinosCamino.empty()) {
            // Elegir un vecino aleatorio
            int vecino = static_cast<int>(rand() % vecinosCamino.size()); //corrobora que la posición es válida sin salirte del vector
            int caminoX = vecinosCamino[vecino].first;
            int caminoY = vecinosCamino[vecino].second;
            
            // Marcar la celda actual como camino
            laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = '*';
            visitado[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = true;
            
            // Marcar la celda intermedia como camino (para conectar)
            int medioX = (posX + caminoX) / 2;
            int medioY = (posY + caminoY) / 2;
            laberinto[static_cast<size_t>(medioX)][static_cast<size_t>(medioY)] = '*';
            visitado[static_cast<size_t>(medioX)][static_cast<size_t>(medioY)] = true;
            
            // Agregar nuevas fronteras
            for(int i = 0; i < 4; i++) {
                int nuevaX = posX + direccionX[i];
                int nuevaY = posY + direccionY[i];
                
                if(nuevaX >= 0 && nuevaX < filas && 
                   nuevaY >= 0 && nuevaY < columnas &&
                   !visitado[static_cast<size_t>(nuevaX)][static_cast<size_t>(nuevaY)]) {
                    fronteras.push_back({nuevaX, nuevaY});
                }
            }
        }
    }
    
    // Marca la entrada (E)
    laberinto[0][0] = 'E';
    // Marca SALIDA (S)
    laberinto[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)] = 'S';
    
    // Si la salida quedó aislada, hacer un camino directo
    if(!visitado[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)]) {
        posX = filas-1;
        posY = columnas-1;
        laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = 'S';
        
        // se valida que siempre haya un camino a la salida
        while(posX > 0 || posY > 0) {
            // Marca como camino
            laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = '*';
            // Elige al azar si sube o va a la izquierda, sin salirse del tablero
            if(posX > 0 && rand() % 2) posX--;
            else if(posY > 0) posY--;
        }
        laberinto[0][0] = 'E';
    }
}

void resolver() {  // BFS 

    // Marca qué posiciones ya fueron visitadas  // primera bandera 
    vector<vector<bool>> visitado(static_cast<size_t>(filas),
                                   vector<bool>(static_cast<size_t>(columnas), false));

    // Guarda las filas y columnas en las que ya se llegó
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
// puntero que apunta a algún lugar en memoria, puede ser constante o dinámico
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