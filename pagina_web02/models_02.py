from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    rol = Column(String(20), default="empleado", nullable=False) #!rol que asigana un administrador
    empleado_id = Column(Integer, ForeignKey('empleado.id')) 

    empleado = relationship("Empleado", back_populates="usuarios")

    def __repr__(self):
        return f"<User(username={self.username})>"


class Empleado(Base):
    __tablename__ = "empleado"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    correo = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    puntos_acumulados = Column(Integer, default=0, nullable=False)

    # Relaciones
    usuarios = relationship("User", back_populates="empleado")
    solicitudes_puntos = relationship("SolicitudPuntos", back_populates="empleado")  # <-- relación agregada

    def __repr__(self):
        return f"<Empleado(nombre={self.nombre}, apellido={self.apellido})>"


class SolicitudPuntos(Base):
    __tablename__ = "solicitud_puntos"
    id = Column(Integer, primary_key=True)
    empleado_id = Column(Integer, ForeignKey('empleado.id'), nullable=False)
    descripcion = Column(String(200), nullable=False)
    fecha_solicitud = Column(Date, nullable=False)

    empleado = relationship("Empleado", back_populates="solicitudes_puntos")  # relación bidireccional

    def __repr__(self):
        return f"<SolicitudPuntos(empleado_id={self.empleado_id}, descripcion={self.descripcion})>"