# Usa una imagen base de Python 3.11
FROM python:3.11-slim-buster

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requirements para instalar las dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia la carpeta src al contenedor
COPY src /app/src

# Expone el puerto en el que el BFF escuchará
EXPOSE 10000

# Define el comando para ejecutar la aplicacion
CMD ["python", "/app/src/app.py"]