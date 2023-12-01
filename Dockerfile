# Dockerfile

# Utilisez une image de base avec Python
FROM python:3.8

# Copiez les fichiers de votre application dans le conteneur
COPY . /app

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Installez les dépendances de votre application
RUN pip install -r requirements.txt

# Commande à exécuter lors du démarrage du conteneur
CMD ["python", "scrapper_2.py"]
