import subprocess
import pypyodbc as odbc
def insert_data(nome_app, nome_immagine, location, nome_utente):
    # Stringa di connessione
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:serverprova2-0.database.windows.net,1433;Database=SRSLoginDB;Uid=adminSRS;Pwd=Cpaaa2023;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    
    # Connessione al database
    conn = odbc.connect(connection_string)
    
    # Creazione del cursore
    cursor = conn.cursor()
    
    # Verifica se la tabella esiste già nel database
    table_exists_query = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'NomeTabella'"
    cursor.execute(table_exists_query)
    table_exists = cursor.fetchone()[0]
    if not table_exists:
    # Se la tabella non esiste, creala
        create_table_query = """
    CREATE TABLE NomeTabella (
    AppName VARCHAR(255),
    DefaultDomain VARCHAR(255),
    Location VARCHAR(255),
    ContainerImage VARCHAR(255),
    Username VARCHAR(255)
)
"""
    
        cursor.execute(create_table_query)
        conn.commit()
    
    # Query di inserimento dei dati
    insert_query = "INSERT INTO NomeTabella (AppName, ContainerImage, Location, DefaultDomain, Username) VALUES (?, ?, ?, ?, ?)"

    
    # Parametri per l'inserimento dei dati
    params = (nome_app, nome_immagine, location,nome_utente+'.azurewebsites.net',nome_utente)
    
    # Esecuzione della query di inserimento
    cursor.execute(insert_query, params)
    
    # Commit delle modifiche
    conn.commit()
    
    # Chiusura della connessione
    conn.close()


def create_webapp(nome_app_web,image):
    # Imposta i nomi delle risorse
    nome_gruppo_risorse = 'srs2023-stu-g1'
    nome_acr = 'srs2023.azurecr.io'
    nome_immagine = image
    app_service_plan = 'ASP-srs2023stug1-9160'
    subprocess.run(
        f'az webapp create --name {nome_app_web} --resource-group {nome_gruppo_risorse} --plan {app_service_plan} --deployment-container-image {nome_acr}/{nome_immagine}',
        shell=True
    )
    insert_data(nome_app_web, nome_immagine, nome_app_web+".azurewebsites.net","West Europe")








