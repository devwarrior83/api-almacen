# Definicion de métodos para los proveedores
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importar la configuración de la BD, modelos y esquemas
from database import get_db
import modelos
import esquemas

# Crear el router con prefijo para que todas las rutas empiecen con /categorias
router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"]
)
# ENDPOINT 1: Crear nuevo proveedor
@router.post("/", response_model=esquemas.ProveedorResponse)
def crear_proveedor(proveedor: esquemas.ProveedorCreate, db: Session = Depends(get_db)):
    # Se crea la instancia del modelo SQLAlchemy
    nuevo_proveedor = modelos.Proveedor(
        nombre = proveedor.nombre,
        contacto = proveedor.contacto
    )
    # Se guardan los cambios en la BD
    db.add(nuevo_proveedor)
    db.commit()
    db.refresh(nuevo_proveedor)

    return nuevo_proveedor

# ENDPOINT 2: Obtener proveedores
@router.get("/", response_model=List[esquemas.ProveedorResponse])
def obtener_proveedores(db: Session = Depends(get_db)):
    return db.query(modelos.Proveedor).all()
