from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import modelos
import esquemas
 
router = APIRouter(
    prefix="/articulos",
    tags=["Articulos"]
    )


# Tener en cuenta que la ruta ahora es solo "/" porque el prefijo ya aporta "/articulos"
# Crear articulo
@router.post("/", response_model=esquemas.ArticuloResponse)
def agregar_articulo(articulo: esquemas.ArticuloCreate, db: Session = Depends(get_db)):
    # Se transforma el esquema Pydantic a un modelo SQLAlchemy
    # model_dump() extrae todos los campos (incluyendo categoria_id y proveedor_id)
    nuevo_articulo = modelos.Articulo(**articulo.model_dump())

    db.add(nuevo_articulo)     # se prepara
    db.commit()                # se guarda en mysql
    db.refresh(nuevo_articulo) # actualizamos para obtener el ID generado

    return nuevo_articulo

# Listar articulos
@router.get("/", response_model=List[esquemas.ArticuloResponse])
def listar_articulos(db: Session = Depends(get_db)):
    articulos = db.query(modelos.Articulo).all()
    return articulos

# Ruta para actualzar artículos
@router.put("/{articulo_id}", response_model=esquemas.ArticuloResponse)
def actualizar_articulo(articulo_id: int, articulo_actualizado: esquemas.ArticuloCreate, db: Session = Depends(get_db)):
    # Se realiza la busqueda si el artículo existe en la BD
    articulo_db = db.query(modelos.Articulo).filter(modelos.Articulo.id == articulo_id).first()

    if articulo_db is None:
        # En el caso de que el artículo no exista en la BD, lanzamos un error 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artículo no encontrado")
    
    # En caso de que si exista, se realiza la actualización dimanica de sus atributos que estan incluidos en el esquema
    for key, value in articulo_actualizado.model_dump().items():
        setattr(articulo_db, key, value)

    # Se guardan los cambios y se actualiza la BD
    db.commit()
    db.refresh(articulo_db)

    return articulo_db

# Ruta para eliminar articulos (DELETE)
@router.delete("/{articulo_id}")
def eliminar_articulo(articulo_id: int, db: Session = Depends(get_db)):
    # Se realiza la busquedad del artículo
    articulo_db = db.query(modelos.Articulo).filter(modelos.Articulo.id == articulo_id).first()

    if articulo_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Artículo no encontrado")
    
    # Mandamos a SQLAlchemy que borre el artículo
    db.delete(articulo_db)
    db.commit() # Comiteamos para confirmar la transacción

    return {"mensaje": f"El artículo con el ID {articulo_id} ha sido eliminado correctamente."}
