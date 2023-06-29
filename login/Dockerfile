# Usa l'immagine di base di Python
FROM python:3.9-slim-buster

# Imposta la directory di lavoro nell'interno del container
WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y gcc


RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y unixodbc unixodbc-dev

ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/lib/x86_64-linux-gnu:/usr/lib:/usr/lib64


# Copia i file del progetto nella directory di lavoro del container
COPY . .

# Avvia l'applicazione Flask
CMD ["python","app.py"]