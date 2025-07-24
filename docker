# Használj stabil, támogatott Python verziót, pl 3.11 (ha aiohttp nem működik 3.13-on)
FROM python:3.11-slim

WORKDIR /app

# Másold be a projekt fájlokat
COPY . .

# Frissítsd a pip-et, setuptools-t, wheel-t és telepítsd a függőségeket
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Indítsd el a programot
CMD ["python", "main.py"]
