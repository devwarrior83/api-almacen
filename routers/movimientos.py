from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import modelos
import esquemas

router = APIRouter(
    prefix="/movimientos",
    tags=["Movimientos"]
)

@router.post("/", response_model=esquemas.MovimientoResponse)
def registrar_movimiento(movimiento: esquemas.MovimientoCreate, db: Session = Depends(get_db)):
    # Verificacion de la existencia del articulo
    articulo_db = db.query(modelos.Articulo).filter(modelos.Articulo.id == movimiento.articulo_id).first()
    if not articulo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artículo no encontrado"
            )

    # Validación de la lógica de negocios antes de guardar
    if movimiento.tipo_movimiento.upper() == "SALIDA":
        if articulo_db.cantidad < movimiento.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock insuficiente para realizar esta salida"
            )
        # Se resta el stock
        articulo_db.cantidad -= movimiento.cantidad

    elif movimiento.tipo_movimiento.upper() == "ENTRADA":
        # Se suma el stock
        articulo_db.cantidad += movimiento.cantidad

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No es valido el tipo de movimiento. Debes usar ENTRADA o SALIDA"
        )

    # Se crea el registro historico
    nuevo_movimiento = modelos.Movimiento(**movimiento.model_dump())
    db.add(nuevo_movimiento)

    # Se guardan los cambios en la BD MySQL
    db.commit()
    db.refresh(nuevo_movimiento)
    return nuevo_movimiento

@router.get("/articulo/{articulo_id}", response_model=List[esquemas.MovimientoResponse])
def historial_articulo(articulo_id: int, db: Session = Depends(get_db)):
    movimientos = db.query(modelos.Movimiento).filter(modelos.Movimiento.articulo_id == articulo_id).all()
    return movimientos
