# 1️⃣ Schlankes Basis-Image
FROM python:3.14-slim

# 2️⃣ Arbeitsverzeichnis
WORKDIR /app

# 3️⃣ Nur requirements zuerst kopieren (Docker Layer Caching)
COPY requirements.txt .

# 4️⃣ Pakete installieren (schlank)
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Restlichen Code kopieren
COPY . .

# 6️⃣ Bot starten
CMD ["python", "main.py"]
