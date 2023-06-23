# Usa l'immagine di base di Python
FROM python:3.9-slim-buster

# Imposta la directory di lavoro nell'interno del container
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copia i file del progetto nella directory di lavoro del container
COPY . .

# Avvia l'applicazione Flask
CMD ["python","app.py"]