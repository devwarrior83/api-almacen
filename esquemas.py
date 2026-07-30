from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Esquema para categorias
class CategoriaBase(BaseModel):
    nombre : str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

# Esquema para proveedores
class ProveedorBase(BaseModel):
    nombre: str
    contacto: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorResponse(ProveedorBase):
    id: int

    class Config:
        from_attributes = True

# Esquema para artículos
class ArticuloBase(BaseModel):
    nombre: str
    precio: float
    cantidad: int
    categoria_id: int # Identificamos a que categoría pertenece
    proveedor_id: int # Identificamos que proveedor lo trae


# Esquema para cuando el usuario crea un artículo (no se pide ID)
class ArticuloCreate(ArticuloBase):
    pass

# Esquema para cuando la API devuelve un artículo (incluyendo el ID de la BD)
class ArticuloResponse(ArticuloBase):
    id: int
    categoria: CategoriaResponse
    proveedor: ProveedorResponse

    class Config:
        from_attributes = True

# ESquemas de movimiento para la trazabilidad de los registros
class MovimientoBase(BaseModel):
    cantidad: int
    tipo_movimiento: str

class MovimientoCreate(MovimientoBase):
    articulo_id: int

class MovimientoResponse(MovimientoCreate):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True
        