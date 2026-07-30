
# Ponemos en uso la imagen base de Python ligera
FROM python:3.10-slim

# Se establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Se copian los archivos de dependencias primero para aprovechar el cache de Docker
COPY requirements.txt .

# Se instalan las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Se copia todo el resto del código del proyecto al contenedor
COPY . .

# Se expone el puerto donde correrá FastAPI
EXPOSE 8000

# Se realiza la ejecusión de la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

