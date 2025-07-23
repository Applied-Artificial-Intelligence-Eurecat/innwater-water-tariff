# Utiliser l'image Python officielle comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# Exposer le port sur lequel Flask va tourner
EXPOSE 5000

# Définir les variables d'environnement Flask
ENV FLASK_APP=Application.py
ENV FLASK_RUN_HOST=0.0.0.0

# Commande pour démarrer l'application
CMD ["python", "Application.py"]