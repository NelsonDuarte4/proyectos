#include <iostream>
#include <vector>
#include <queue>      // Permite usar colas (BFS usa una cola)
#include <cstdlib>    // rand(), srand()
#include <ctime>
using namespace std;  // Evita escribir std:: antes de cada cosa

int filas = 10, columnas = 10;

// Mapa del laberinto (matriz de caracteres)
vector<vector<char>> laberinto;

// Función para imprimir el laberinto en consola
void imprimir() {
    for(int i = 0; i < filas; i++) {
        for(int j = 0; j < columnas; j++) {
            // Imprime cada celda del laberinto
            cout << laberinto[static_cast<size_t>(i)][static_cast<size_t>(j)] << ' ';
        }
        cout << endl;
    }
}

// Función que genera y resuelve el laberinto
void resolver() {  

    // ------------------ INICIO CREACIÓN DEL LABERINTO ------------------
    // Llenar todo el laberinto con muros ('#')
    laberinto.assign(static_cast<size_t>(filas),
                     vector<char>(static_cast<size_t>(columnas), '#'));

    // Vector para marcar los lugares visitados durante la generación
    vector<vector<bool>> visitado(static_cast<size_t>(filas),
                                   vector<bool>(static_cast<size_t>(columnas), false));

    vector<pair<int,int>> fronteras; // Cola de fronteras para la generación
    int posX = 0, posY = 0;          // Posición inicial

    // Marcar la posición inicial como camino válido '*'
    laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = '*';
    visitado[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = true;

    // Direcciones posibles: abajo, arriba, derecha, izquierda (saltando 2 celdas)
    int direccionX[] = {2, -2, 0, 0};
    int direccionY[] = {0, 0, 2, -2};

    // Cargar las fronteras iniciales alrededor del inicio
    for(int i = 0; i < 4; i++) {
        int nuevaX = posX + direccionX[i];
        int nuevaY = posY + direccionY[i];
        if(nuevaX >= 0 && nuevaX < filas && nuevaY >= 0 && nuevaY < columnas)
            fronteras.push_back({nuevaX, nuevaY});
    }

    // Mientras queden fronteras, generar caminos
    while(!fronteras.empty()) {
        int indice = static_cast<int>(rand() % fronteras.size());  // Elegir frontera aleatoria
        posX = fronteras[indice].first;
        posY = fronteras[indice].second;
        fronteras.erase(fronteras.begin() + indice);              // Remover de fronteras

        if(visitado[static_cast<size_t>(posX)][static_cast<size_t>(posY)])
            continue;  // Si ya fue visitada, saltar

        // Buscar vecinos que ya sean caminos
        vector<pair<int,int>> vecinosCamino;
        for(int i = 0; i < 4; i++) {
            int nuevaX = posX + direccionX[i];
            int nuevaY = posY + direccionY[i];
            if(nuevaX >= 0 && nuevaX < filas && nuevaY >= 0 && nuevaY < columnas &&
               visitado[static_cast<size_t>(nuevaX)][static_cast<size_t>(nuevaY)])
                vecinosCamino.push_back({nuevaX, nuevaY});
        }

        // Si hay vecinos camino, conectar
        if(!vecinosCamino.empty()) {
            int vecino = static_cast<int>(rand() % vecinosCamino.size()); // Elegir vecino aleatorio
            int caminoX = vecinosCamino[vecino].first;
            int caminoY = vecinosCamino[vecino].second;

            // Marcar la celda actual como camino
            laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = '*';
            visitado[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = true;

            // Marcar la celda intermedia para conectar caminos
            int medioX = (posX + caminoX) / 2;
            int medioY = (posY + caminoY) / 2;
            laberinto[static_cast<size_t>(medioX)][static_cast<size_t>(medioY)] = '*';
            visitado[static_cast<size_t>(medioX)][static_cast<size_t>(medioY)] = true;

            // Agregar nuevas fronteras alrededor de la celda actual
            for(int i = 0; i < 4; i++) {
                int nuevaX = posX + direccionX[i];
                int nuevaY = posY + direccionY[i];
                if(nuevaX >= 0 && nuevaX < filas && nuevaY >= 0 && nuevaY < columnas &&
                   !visitado[static_cast<size_t>(nuevaX)][static_cast<size_t>(nuevaY)])
                    fronteras.push_back({nuevaX, nuevaY});
            }
        }
    }

    // Marcar la entrada y la salida
    laberinto[0][0] = 'E';
    laberinto[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)] = 'S';

    // Si la salida quedó aislada, crear un camino directo
    if(!visitado[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)]) {
        posX = filas-1;
        posY = columnas-1;
        laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = 'S';
        while(posX > 0 || posY > 0) {
            laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = '*';
            if(posX > 0 && rand() % 2) posX--;  // Subir aleatoriamente
            else if(posY > 0) posY--;           // O mover a la izquierda
        }
        laberinto[0][0] = 'E';
    }
    // ------------------ FIN CREACIÓN DEL LABERINTO ------------------

    // ------------------ INICIO BFS PARA RESOLVER ------------------
    vector<vector<bool>> visitadoBFS(static_cast<size_t>(filas),
        vector<bool>(static_cast<size_t>(columnas), false)); // Marcas para BFS

    // Guardar de dónde viene cada celda (para reconstruir camino)
    vector<vector<pair<int,int>>> anterior(static_cast<size_t>(filas),
        vector<pair<int,int>>(static_cast<size_t>(columnas), {-1,-1}));

    queue<pair<int,int>> cola; // Cola para BFS
    cola.push({0,0});           // Agregar inicio
    visitadoBFS[0][0] = true;   // Marcar inicio como visitado

    int dx[] = {1,-1,0,0};  // Direcciones: abajo, arriba, derecha, izquierda
    int dy[] = {0,0,1,-1};

    // Recorrido BFS
    while(!cola.empty()) {
        int x = cola.front().first;
        int y = cola.front().second;
        cola.pop();

        for(int i = 0; i < 4; i++) {
            int nx = x + dx[i];
            int ny = y + dy[i];
            if(nx >= 0 && nx < filas && ny >= 0 && ny < columnas &&
               !visitadoBFS[static_cast<size_t>(nx)][static_cast<size_t>(ny)] &&
               laberinto[static_cast<size_t>(nx)][static_cast<size_t>(ny)] != '#') {

                visitadoBFS[static_cast<size_t>(nx)][static_cast<size_t>(ny)] = true;
                anterior[static_cast<size_t>(nx)][static_cast<size_t>(ny)] = {x,y};
                cola.push({nx,ny});
            }
        }
    }

    // Si no se visitó la salida, no hay solución
    if(!visitadoBFS[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)]) {
        cout << "No hay solucion" << endl;
        return;
    }

    // Reconstruir el camino desde la salida hasta el inicio
    posX = filas-1;
    posY = columnas-1;
    while(posX != 0 || posY != 0) {
        int prevX = anterior[static_cast<size_t>(posX)][static_cast<size_t>(posY)].first;
        int prevY = anterior[static_cast<size_t>(posX)][static_cast<size_t>(posY)].second;
        if(laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] == '*')
            laberinto[static_cast<size_t>(posX)][static_cast<size_t>(posY)] = 'o'; // marcar camino solucion
        posX = prevX;
        posY = prevY;
    }

    laberinto[0][0] = 'E';  // volver a marcar inicio
    laberinto[static_cast<size_t>(filas-1)][static_cast<size_t>(columnas-1)] = 'S'; // marcar salida
}

// Función para configurar tamaño del laberinto
void configurarTamano() {
    int opcion;
    
    cout << "\n=== CONFIGURACION DEL LABERINTO ===" << endl;
    cout << "1. Usar tamano por defecto (10x10)" << endl;
    cout << "2. Ingresar tamano personalizado" << endl;
    cout << "Seleccione una opcion: ";
    cin >> opcion;
    
    if(opcion == 2) {
        do {
            cout << "\nIngrese el numero de filas (minimo 5, debe ser impar): ";
            cin >> filas;
            
            // Validar que sea impar y >= 5
            if(filas < 5) {
                cout << "Error: El minimo es 5 filas." << endl;
            } else if(filas % 2 == 0) {
                cout << "Advertencia: Se ajustara a " << (filas + 1) 
                     << " (debe ser impar para el algoritmo)" << endl;
                filas++;
            }
        } while(filas < 5);
        
        do {
            cout << "Ingrese el numero de columnas (minimo 5, debe ser impar): ";
            cin >> columnas;
            
            if(columnas < 5) {
                cout << "Error: El minimo es 5 columnas." << endl;
            } else if(columnas % 2 == 0) {
                cout << "Advertencia: Se ajustara a " << (columnas + 1) 
                     << " (debe ser impar para el algoritmo)" << endl;
                columnas++;
            }
        } while(columnas < 5);
        
        cout << "\nLaberinto configurado: " << filas << "x" << columnas << endl;
    } else {
        cout << "\nUsando tamano por defecto: 10x10" << endl;
    }
}

// Función principal
int main(int argc, char* argv[]) {
    srand(time(0)); // Inicializa semilla aleatoria
    
    // Si se pasan parámetros por línea de comandos, usarlos
    if(argc == 3) {
        filas = stoi(argv[1]);
        columnas = stoi(argv[2]);
        
        // Ajustar a impares si es necesario
        if(filas % 2 == 0) filas++;
        if(columnas % 2 == 0) columnas++;
        
        cout << "Tamano desde parametros: " << filas << "x" << columnas << endl;
    } else {
        // Si no hay parámetros, mostrar menú interactivo
        configurarTamano();
    }
    
    // Resolver() incluye la generación del laberinto
    clock_t tiempo1 = clock();
    resolver();  // genera y resuelve
    clock_t tiempo2 = clock();
    
    imprimir();  // mostrar laberinto
    
    cout << endl << "Tiempo generar + resolver: "
         << (tiempo2 - tiempo1)*1000.0/CLOCKS_PER_SEC << " ms" << endl;
    
    return 0;
}
