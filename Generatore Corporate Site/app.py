import openai
import os
from flask import Flask, render_template, request, send_from_directory, session
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from waitress import serve

app = Flask(__name__)
app.secret_key = 'mysecret'



@app.route('/corp')
def index():
    # Route per la pagina principale del form Corporate site
    return render_template('form_CS.html')

@app.route('/genera_corporate_site', methods=['POST'])
def genera_corporate_site():
    # Route per la generazione del corporate site
    # Inizializzazione del servizio Blob Storage di Azure
    connection_string = 'DefaultEndpointsProtocol=https;AccountName=sitetailoremplatestorage;AccountKey=sMMXV9JGaoWuujLkLr1emp+Q5s4GK+kIZNsnc1/q9k3hi9HZS8oOdxmhLhtihlO2WPFNFrRMiYvJ+ASt1Jql/w==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    #Creazione di un contenitore per l'utente corrente
    user_container_name = session['username']

    #recupero dei dati inseriti dall'utente
    company_name = request.form.get('companyName') 
    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')
    service_count = request.form.get('serviceCount')

    # Creazione percorso completo di una directory chiamata "static" all'interno dell'applicazione
    templates_dir = os.path.join(app.root_path, 'static')

    html_text = generate_html_from_description(company_name, address, email, phone, service_count)
    file_path = os.path.join(templates_dir, 'CorporateSite.html')
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(html_text)

    user_container_client = blob_service_client.create_container(user_container_name)

    # Upload del file nel contenitore dell'utente corrente
    file_name = 'output.html'
    blob_client = blob_service_client.get_blob_client(container=user_container_name, blob=file_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    return send_from_directory('static', 'CorporateSite.html')

# Route per i file statici
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


# Funzione per la generazione delle pagine html
def generate_html_from_description(company_name, address, email, phone, service_count):
    # Lettura del contenuto del file template_corporate_site.html
    with open("template_corporate_site.html", "r") as file:
        html_content = file.read()

    # Composizione del prompt con la descrizione dell'utente e il contenuto del file HTML
    prompt = f"Alterare il codice HTML che ti invio nel modo seguente: Inserisci {company_name} per il nome dell'azienda con una descrizione ed un numero di servizi offerti pari a {service_count}, inventandoti dei nomi e delle descrizioni per quest'ultimi, senza aggiungere link. Inserisci, inoltre, {email}, {address} e {phone} nella sezione Contatti.\n\n{html_content}. Utilizza lo stesso stile del file html. Inoltre, inserisci {company_name} all'interno della navbar con un tag <h3>."

    # Impostazione della chiave API
    openai.api_key = ${{ secrets.KEY }}
    
    # Chiamata all'API di completamento di OpenAI
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=2500,
        temperature=1
    )

    html_text = response.choices[0].text
    api_usage = response['usage']
    print('Total token consumed: {0}'.format(api_usage['total_tokens']))

    return html_text

#if __name__ == '__main__':
#  serve(app, host='0.0.0.0', port=80, threads=4)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
