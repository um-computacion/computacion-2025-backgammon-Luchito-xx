# Imagen base de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Exponer puerto si usas Redis (opcional)
EXPOSE 6379

# Comando por defecto: ejecutar CLI
CMD ["python", "-m", "cli.cli"]