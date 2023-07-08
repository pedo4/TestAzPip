from flask import Flask, jsonify, render_template,send_file,redirect,session,request
from utils.create_app import create_webapp
from utils.push_dockimage import push_docker_image
from utils.create_dockerImage import build_docker_image
from utils.update_app import update_webapp_image
from utils.login import azure_login
from azure.storage.blob import BlobServiceClient
import time
import os
from flask import current_app
from waitress import serve

app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.secret_key = 'mysecret'
azure_login()



# Funzione per ottenere l'elenco dei nomi dei file nel contenitore blob "temp"
def get_blob_names():
    username = session['username']
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=sitetailoremplatestorage;AccountKey=sMMXV9JGaoWuujLkLr1emp+Q5s4GK+kIZNsnc1/q9k3hi9HZS8oOdxmhLhtihlO2WPFNFrRMiYvJ+ASt1Jql/w==;EndpointSuffix=core.windows.net")
    # Create a unique name for the container
    container_name = str(username)

    container_client = blob_service_client.get_container_client(container_name)

    # Ottenere l'elenco dei nomi dei blob nel contenitore
    blob_names = [blob.name for blob in container_client.list_blobs()]

    return blob_names

@app.route('/api/applications/download/<file_name>', methods=['GET'])
def download_app_file(file_name):
    username = session['username']
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=sitetailoremplatestorage;AccountKey=sMMXV9JGaoWuujLkLr1emp+Q5s4GK+kIZNsnc1/q9k3hi9HZS8oOdxmhLhtihlO2WPFNFrRMiYvJ+ASt1Jql/w==;EndpointSuffix=core.windows.net")
    # Create a unique name for the container
    container_name = str(username)

    container_client = blob_service_client.get_container_client(container_name)
    

    # Verificare se il file esiste nel contenitore di blob
    blob_client = container_client.get_blob_client(file_name)
    if not blob_client.exists():
        return "File non trovato"
    timestamp = int(time.time())  # Ottieni il timestamp corrente
    file_name = f"{timestamp}_{file_name}"  # Aggiungi il timestamp al nome del file
    # Scaricare il file dal contenitore di blob e restituirlo come allegato
    download_file_path = f"{file_name}"  # Percorso temporaneo per il download
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    # Invia il file come allegato
    response = send_file(download_file_path, as_attachment=True)

    # Chiudi il file
    download_file.close()
    # Elimina il file temporaneo
    print(download_file_path)
    return response
    
@app.route('/applications', methods=['GET'])
def get_user_applications():
    username = session['username']
    print(username)
    # Ottenere l'elenco dei nomi dei blob nel contenitore
    blob_names = get_blob_names()
    user_applications = []

    for index, blob_name in enumerate(blob_names):
        # Generare il nome dell'applicazione in base all'indice e all'username
        app_name = f"template_{index}_{username}"

        # Aggiungere l'entry all'elenco delle applicazioni dell'utente
        user_applications.append({
            'appName': app_name,
            'userId': username,
            'file': blob_name
        })
    print(user_applications[0]["file"])
    return jsonify(user_applications)

@app.route('/createApp', methods=['GET'])
def create():
    username = session['username']
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=sitetailoremplatestorage;AccountKey=sMMXV9JGaoWuujLkLr1emp+Q5s4GK+kIZNsnc1/q9k3hi9HZS8oOdxmhLhtihlO2WPFNFrRMiYvJ+ASt1Jql/w==;EndpointSuffix=core.windows.net")
    # Create a unique name for the container
    container_name = str(username)

    container_client = blob_service_client.get_container_client(container_name)

    # Ottenere il nome del file associato all'applicazione specificata da app_id
    # Esempio: supponiamo che il nome del file sia uguale all'app_id con estensione ".txt"
    file_name = "output.html"

    # Verificare se il file esiste nel contenitore di blob
    blob_client = container_client.get_blob_client(file_name)
    if not blob_client.exists():
        return "File non trovato"
    timestamp = int(time.time())  # Ottieni il timestamp corrente
    file_name = f"{timestamp}{file_name}"  # Aggiungi il timestamp al nome del file
    # Scaricare il file dal contenitore di blob e restituirlo come allegato
    download_file_path = os.path.join(".", file_name) 
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    image_name = build_docker_image(file_name)
    create_webapp(username,image_name)
    return redirect("/manage") 

@app.route('/myApp')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

#if __name__ == '__main__':
#   serve(app, host='0.0.0.0', port=80, threads=4)