from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL_BASE_DATOS = "mysql+pymysql://root:api_almacen@db:3306/almacen_db"

engine = create_engine(URL_BASE_DATOS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# No olvidar crear la dependencia para crear y cerrar las sesiones de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        