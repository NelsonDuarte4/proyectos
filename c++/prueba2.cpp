#include <iostream>
#include <vector>
#include <queue>   // Permite usar colas (BFS usa una cola)
#include <cstdlib> // rand(), srand()
#include <ctime>
using namespace std;

int filas = 10, columnas = 10;
vector<vector<char>> laberinto;
void crearLaberinto()
{
    // Llenar todo el laberinto con paredes
    for (int i = 0; i < filas; i++)
    {
        for (int j = 0; j < filas; j++)
        {
            laberinto[i][j] = '#';
        }
    }
}