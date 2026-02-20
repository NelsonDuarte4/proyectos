#include <bits/stdc++.h>
#include <random>
#include <ctime>
using namespace std;

// Símbolos del mapa
const char MURO = '#';
const char CAMINO = '*';
const char RESUELTO = 'o';

// Variables del tamaño del laberinto
int filas = 10, columnas = 10;

// Grilla visible (doble tamaño para muros)
vector<vector<char>> lab;

// Dirección de movimiento
int dir[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};

// ----------------------------
// GENERAR LABERINTO (DFS)
// ----------------------------
void generar(int r, int c, vector<vector<bool>>& visitado) {
    visitado[r][c] = true;
    lab[r*2+1][c*2+1] = CAMINO;

    vector<int> orden = {0,1,2,3};

    // Mezcla moderna (C++17)
    static random_device rd;
    static mt19937 g(rd());
    shuffle(orden.begin(), orden.end(), g);

    for(int d : orden) {
        int nr = r + dir[d][0];
        int nc = c + dir[d][1];

        if(nr >= 0 && nr < filas && nc >= 0 && nc < columnas && !visitado[nr][nc]) {
            // Romper muro entre celdas
            lab[r + nr + 1][c + nc + 1] = CAMINO;
            generar(nr, nc, visitado);
        }
    }
}

// ----------------------------
// RESOLVER LABERINTO (BFS)
// ----------------------------
void resolver() {
    int H = (int)lab.size();
    int W = (int)lab[0].size();

    vector<vector<bool>> visitado(H, vector<bool>(W, false));
    vector<vector<pair<int,int>>> padre(H, vector<pair<int,int>>(W, {-1,-1}));

    queue<pair<int,int>> cola;
    cola.push({1,1});
    visitado[1][1] = true;

    while(!cola.empty()) {
        auto [r,c] = cola.front(); 
        cola.pop();

        for(auto& d : dir) {
            int nr = r + d[0];
            int nc = c + d[1];

            if(nr >= 0 && nr < H && nc >= 0 && nc < W &&
               !visitado[nr][nc] && lab[nr][nc] == CAMINO) {

                visitado[nr][nc] = true;
                padre[nr][nc] = {r,c};
                cola.push({nr,nc});
            }
        }
    }

    // Reconstrucción del camino
    int r = H - 2;
    int c = W - 2;
    while(r != 1 || c != 1) {
        lab[r][c] = RESUELTO;
        auto p = padre[r][c];
        r = p.first;
        c = p.second;
    }
}

// ----------------------------
// MOSTRAR LABERINTO
// ----------------------------
void mostrar() {
    int rf = (int)lab.size() - 2;
    int cf = (int)lab[0].size() - 2;

    lab[1][1] = 'S';
    lab[rf][cf] = 'E';

    for(auto& fila : lab) {
        for(char c : fila) cout << c;
        cout << '\n';
    }
}

// ----------------------------
// MAIN
// ----------------------------
int main(int argc, char* argv[]) {

    // Tamaño por parámetros
    if(argc == 3) {
        filas = stoi(argv[1]);
        columnas = stoi(argv[2]);
    }

    // Crear grilla
    lab.assign(filas*2 + 1, vector<char>(columnas*2 + 1, MURO));
    vector<vector<bool>> visitado(filas, vector<bool>(columnas, false));

    // Medir tiempo de generación
    auto t1 = clock();
    generar(0,0,visitado);
    auto t2 = clock();

    // Medir tiempo de solución
    auto t3 = clock();
    resolver();
    auto t4 = clock();

    // Mostrar laberinto
    mostrar();

    cout << "\nTiempo generación: " 
         << double(t2 - t1) / CLOCKS_PER_SEC * 1000 << " ms\n";

    cout << "Tiempo resolución: " 
         << double(t4 - t3) / CLOCKS_PER_SEC * 1000 << " ms\n";

    return 0;
}
