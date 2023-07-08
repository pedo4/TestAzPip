import subprocess
import time
import docker
import time


def build_docker_image(filename):
    # Aggiungi un timestamp per rendere il nome univoco
    print(filename)
    timestamp = str(int(time.time()))
    # Componi il nome dell'immagine
    nome_immagine_locale  = f"{timestamp}_{filename}"
    # Imposta la cartella del Dockerfile come la cartella "static"
     
    dockerfile = 'Dockerf'
    
    subprocess.run(f'az acr build --registry SRS2023 --image {nome_immagine_locale}:latest --file {dockerfile} --build-arg filename={filename} .', shell=True)
    
    return nome_immagine_locale



