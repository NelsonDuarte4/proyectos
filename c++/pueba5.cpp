/*// ------------------------------------------------------------
// Función: esPosicionValida
// Devuelve true si la posición (x, y) está dentro de la matriz
// ------------------------------------------------------------
bool esPosicionValida(int x, int y, int filas, int columnas) {
    // Verifica que x esté dentro del rango de filas
    // y que y esté dentro del rango de columnas
   if (x >= 0 && x < filas && y >= 0 && y < columnas) {
        return true;   // La posición es válida
    }
    return false;      // La posición NO es válida
}

*/
#include <iostream>
#include <vector>
#include <queue>   // Permite usar colas (BFS usa una cola)
#include <cstdlib> // rand(), srand()
#include <ctime>
using namespace std;

int filas = 10, columna = 10;

bool validaPosion(int x,int y, int filas, int columnas){
    if(x < columna && y < filas){
        return true;
    }else{
        return false;
    }
}

int main(){
    int x,y;

    int fila,columna;
    cout<<"fila";
    cin>>fila;
    cout<<"columna";
    cin>>columna;
    cout<<"ingrese la posicion de x";
    cin>>x;
    cout<<"Ingrese la posicion de y";
    cin>>y;
    
    if(validaPosion(x, y,fila,columna)) {
        cout<<"posicionvalida";
    }else{
        cout<<"no valida ";
    }


}