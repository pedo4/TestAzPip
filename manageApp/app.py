from flask import Flask, jsonify, request,render_template, session
import subprocess
import pypyodbc as odbc
from utils import login
from waitress import serve

app = Flask(__name__)
app.secret_key = 'mysecret'

def get_app_data(connection):
    app_data = {}
    username = session["username"]
    query = """
SELECT appName, defaultDomain, location, containerImage
FROM NomeTabella
WHERE AppName = ?
"""


    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if row:
                app_data['appName'] = row[0]
                app_data['defaultDomain'] = row[1]
                app_data['location'] = row[2]
                app_data['containerImage'] = row[3]

        return app_data

    except Exception as e:
        print("Errore durante il recupero dei dati dell'applicazione:", str(e))
        return None


# Resto del tuo codice...








login.azure_login()
# Funzione per ottenere la stringa di connessione al database MySQL
def get_connection_string():
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:serverprova2-0.database.windows.net,1433;Database=SRSLoginDB;Uid=adminSRS;Pwd=Cpaaa2023;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    return connection_string

# Funzione per la connessione al database MySQL
def connect_to_database():
    connection_string = get_connection_string()
    try:
        conn = odbc.connect(connection_string)
        print('Connessione al database avvenuta con successo.')
        return conn
    except odbc.Error as e:
        print(f'Errore durante la connessione al database: {e}')
        return None
    
@app.route('/api/webapp/<action>', methods=['GET'])
def control_webapp(action):
    # Imposta i nomi delle risorse
    nome_gruppo_risorse = 'srs2023-stu-g1'
    username = session["username"]
    nome_app_web = username

    if action == 'start':
        subprocess.run(f'az webapp start --name {nome_app_web} --resource-group {nome_gruppo_risorse}', shell=True)
        message = f'Web app "{nome_app_web}" avviata.'
    elif action == 'stop':
        subprocess.run(f'az webapp stop --name {nome_app_web} --resource-group {nome_gruppo_risorse}', shell=True)
        message = f'Web app "{nome_app_web}" arrestata.'
    else:
        message = 'Azione non valida.'

    response = {'message': message}
    return jsonify(response)


@app.route('/getData', methods=['GET'])
def get_data():
    conn = connect_to_database()
    app_data = get_app_data(conn)
    print(app_data)
    return jsonify(app_data)


@app.route('/manage')
def index():
    return render_template('index.html')


if __name__ == '__main__':
   serve(app, host='0.0.0.0', port=80, threads=4)


#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80)