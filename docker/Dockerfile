# Base image officielle Python
FROM python:3.10-slim

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier tout le code source dans le conteneur
COPY . .

# Définir la commande par défaut (par exemple : exécuter les tests)
CMD ["pytest", "tests/"]
