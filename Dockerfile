FROM python:3.10

WORKDIR /app

COPY requirements.txt .
# update image os
RUN apt-get update && apt-get install libgl1 -y

# Instala los paquetes Python especificados en requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la aplicación actual al directorio de trabajo en el contenedor
COPY . .

# Ejecuta tu aplicación o script
# Por ejemplo, si tu script se llama app.py, podrías ejecutarlo así:

EXPOSE 5000

CMD ["python", "src/main.py"]
