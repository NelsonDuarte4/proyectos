from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_02 import Base, User, Empleado
from werkzeug.security import generate_password_hash
from datetime import date

DB_URL = "sqlite:///usuarios.db"

def crear_db_y_usuarios_y_empleados():
    engine = create_engine(DB_URL, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # === EMPLEADOS PREDETERMINADOS ===
    
    empleados_data = [
        ("Ara", "Ortigoza", "1234567", "ara.ortigoza.fidelix@gmail.com", "0976971999", date(1990, 5, 21), 10000),
        ("Carlos", "Gómez", "2345678", "carlos.gomez.fidelix@gmail.com", "0986123456", date(1988, 3, 15), 20000),
        ("Lucía", "Fernández", "3456789", "lucia.fernandez.fidelix@gmail.com", "0982345678", date(1995, 8, 10), 15000),
        ("Esteban", "Martínez", "4567890", "esteban.martinez.fidelix@gmail.com", "0972123456", date(1985, 12, 5), 25000),
        ("Nelson", "Rodríguez", "5678901", "nelson.rodriguez.fidelix@gmail.com", "0976976543", date(1992, 11, 30), 30000)
    ]

    empleados = []
    for nombre, apellido, cedula, correo, celular, fecha_nacimiento, puntos in empleados_data:
        existente = session.query(Empleado).filter_by(cedula=cedula).first()
        if not existente:
            empleado = Empleado(
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                correo=correo,
                celular=celular,
                fecha_nacimiento=fecha_nacimiento,
                puntos_acumulados=puntos
            )
            session.add(empleado)
            empleados.append(empleado)
        else:
            empleados.append(existente)

    # Hacer commit de los empleados para que tengan IDs asignados
    session.commit()

    # === USUARIOS PREDETERMINADOS (asignando empleado) ===
    # IMPORTANTE: Esta sección debe estar FUERA del bucle anterior
    usuarios_data = [
        ("Ara", "a123", empleados[0], "empleado"),
        ("Carlos", "c123", empleados[1], "admin"),
        ("Lucía", "l123", empleados[2], "empleado"),
        ("Esteban", "e123", empleados[3], "empleado"),
        ("Nelson", "n123", empleados[4], "empleado")
    ]

    for username, pwd, empleado, rol in usuarios_data: 
        existente = session.query(User).filter_by(username=username).first()
        if not existente:
            hashed = generate_password_hash(pwd)
            user = User(username=username, password_hash=hashed, rol=rol, empleado=empleado)
            session.add(user)

    session.commit()
    session.close()
    print("✅ Base de datos creada con usuarios y empleados relacionados.")

if __name__ == "__main__":
    crear_db_y_usuarios_y_empleados()