from fastapi import FastAPI
import modelos
from database import engine

# Asegurarse de importar TODOS los enrutadores
from routers import categorias, proveedores, articulos, movimientos

# Inicialización de la aplicación / Crea las tablas en la BD si no existen
modelos.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Gestión de Almacen")

# Se conectan los routers a la app
app.include_router(categorias.router)
app.include_router(proveedores.router)
app.include_router(articulos.router)
app.include_router(movimientos.router)
