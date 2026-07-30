from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime
# Definición de objetos de los esquemas para la validación de datos que entran y salen de la base de datos.

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50),unique=True, index=True)
    descripcion = Column(String(200))

    # Relación inversa: Una categoría tiene muchos artículos
    articulos = relationship("Articulo", back_populates="categoria")

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    contacto = Column(String(100))

    # Relación inversa: Un proveedor suministra muchos artículos
    articulos = relationship("Articulo", back_populates="proveedor")
    
class Articulo(Base):
    __tablename__ = "articulos"

    movimientos = relationship("Movimiento", back_populates="articulo", cascade="all, delete-orphan")

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    precio = Column(Float)
    cantidad = Column(Integer)

    # Claves foraneas que apuntan a las otras tablas
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))

    # Relación de uso 
    categoria  = relationship("Categoria", back_populates="articulos")
    proveedor = relationship("Proveedor", back_populates="articulos")

class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    articulo_id = Column(Integer, ForeignKey("articulos.id"))
    cantidad = Column(Integer)
    tipo_movimiento = Column(String(50)) # 'Entrada', 'Salida', etc
    fecha = Column(DateTime, default=datetime.datetime.utcnow)

    articulo = relationship("Articulo", back_populates="movimientos")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    activo = Column(Integer, default=1) # 1 para ACTIVO, 0 para INACTIVO
    