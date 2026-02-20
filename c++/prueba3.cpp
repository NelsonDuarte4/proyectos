// ------------------------------------------------------------
// Función: esPosicionValida
// Devuelve true si la posición (x, y) está dentro de la matriz
// ------------------------------------------------------------
bool esPosicionValida(int x, int y, int filas, int columnas) {
   if (x >= 0 && x < filas && y >= 0 && y < columnas) {
        return true;   // La posición es válida
    }
    return false;      // La posición NO es válida
}