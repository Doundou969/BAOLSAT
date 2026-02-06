# Utilisation d'une version plus récente pour correspondre à ton workflow 2026
FROM python:3.12-slim

# Empêche Python de générer des fichiers .pyc et force l'affichage des logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installation des dépendances système nécessaires (ex: sqlite)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet
COPY . .

# Création du dossier uploads s'il n'existe pas (pour éviter les erreurs d'écriture)
RUN mkdir -p static/uploads

# Port d'exposition
EXPOSE 8000

# Utilisation de Gunicorn pour la stabilité en production
# 4 workers est un bon ratio pour un serveur standard
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:app"]
