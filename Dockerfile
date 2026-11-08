# Imagen base con Python compatible con el modelo entrenado.
FROM python:3.13-slim

# Directorio principal de la aplicación dentro del contenedor.
WORKDIR /app

# Se evita generar archivos temporales de Python.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Se instalan las dependencias antes de copiar el código.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Se incorporan el backend, frontend y modelo entrenado.
COPY app/ ./app/
COPY modelo/ ./modelo/

# Puerto utilizado por FastAPI.
EXPOSE 8000

# Se inicia la aplicación y se permite el acceso desde el host.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]