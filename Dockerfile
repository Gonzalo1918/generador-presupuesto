# Imagen base ligera de Python
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para Pillow y ReportLab
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    libz-dev \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Render define automáticamente PORT=10000 o 8080
ENV PORT=8080

# Exponer el puerto donde correrá Flet Web
EXPOSE 8080

# Comando de ejecución
# Se usa --web para servir la app como sitio web accesible desde Render
CMD ["python", "main.py"]


