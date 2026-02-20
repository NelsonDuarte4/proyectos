bool posicicionvalida(int x, int y, int filas, int columnas){
    if (x >= 0 && x < filas && y >= 0 && y < filas ){
        return true;
    }
    return false;
}