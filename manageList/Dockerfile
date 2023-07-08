# Usa un'immagine di base di Python
FROM python:3.9-slim-buster

# Imposta la directory di lavoro nell'interno del container
WORKDIR /app

# Installazione di curl
RUN apt-get update && apt-get install -y curl
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

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




# Installa le dipendenze del tuo progetto
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
# Avvia l'applicazione Flask
CMD ["python", "app.py"]
















