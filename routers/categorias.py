# Definicion de métodos para Crear y Leer categorías
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importar la configuración de la BD, modelos y esquemas
from database import get_db
import modelos
import esquemas

# Crear el router con prefijo para que todas las rutas empiecen con /categorias
router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)

# ENDPOINT 1: CREAR UNA CATEGORIA
@router.post("/", response_model=esquemas.CategoriaResponse)
def crear_categoria(categoria: esquemas.CategoriaCreate, db: Session = Depends(get_db)):
    # Se verifica si la categoria ya existe (el nombre debe ser único)
    categoria_existente = db.query(modelos.Categoria).filter(modelos.Categoria.nombre == categoria.nombre).first()
    if categoria_existente:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    # Se crea la instancia del modelo SQLAlchemy
    nueva_categoria = modelos.Categoria(
        nombre = categoria.nombre,
        descripcion = categoria.descripcion
    )

    # Se guardan los cambios en la BD
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)

    return nueva_categoria

# ENDPOINT 2: Obtener todas las categorías
@router.get("/", response_model=List[esquemas.CategoriaResponse])
def obtener_categorias(db: Session = Depends(get_db)):
    categorias = db.query(modelos.Categoria).all()
    return categorias

# ENDPOINT 3: Obtener una categoría por ID
@router.get("/{categoria_id}", response_model=esquemas.CategoriaResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(modelos.Categoria).filter(modelos.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria