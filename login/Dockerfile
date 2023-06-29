# Usa l'immagine di base di Python per Windows
FROM python:3.9-slim-buster

# Installa il compilatore C e le dipendenze necessarie
RUN apt-get update && apt-get install -y build-essential

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia il file requirements.txt nel container
COPY requirements.txt requirements.txt

# Copia i file del progetto nella directory di lavoro del container
COPY . .

# Installazione di curl
RUN apt-get update && apt-get install -y curl

# Installazione del driver ODBC di Microsoft SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN exit
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
RUN . ~/.bashrc
RUN apt-get install -y unixodbc-dev
RUN apt-get install -y libgssapi-krb5-2

# Installa i pacchetti Python specificati nel file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Avvia l'applicazione Flask
CMD ["python", "app.py"]

