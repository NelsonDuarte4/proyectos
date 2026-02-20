int filas = 10, columna = 10;

bool validaPosion(int x,int y, int filas, int columnas){
    if(x >= 0 && x < filas && y >= 0 && y < columnas ){
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