# DOCKERFILE DU SERVICE 2
# GÉOLOCALISATION DES LIEUX (DÉPART, ARRIVÉE, LIEU D'INTÉRÊT)

# Image de base 
FROM python:3.11-slim

# Dépendnaces 
WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port
EXPOSE 3002

# Éxécution du service
CMD ["python", "lieux.py"]
