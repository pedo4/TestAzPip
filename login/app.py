import pypyodbc as odbc
from flask import Flask, render_template, request, redirect
import bcrypt
from waitress import serve

app = Flask(__name__)

# Funzione per la connessione al database MySQL
def connect_to_database():
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:server2023srs.database.windows.net,1433;Database=srslogreg;Uid=AdminSRS;Pwd=Cpaaa2023;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    try:
        conn = odbc.connect(connection_string)
        print('Connessione al database avvenuta con successo.')
        return conn
    except odbc.Error as e:
        print(f'Errore durante la connessione al database: {e}')
        return None

@app.route('/')
def home():
    return render_template('index.html')

# Route per la pagina di login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Esegui l'autenticazione dell'utente nel database
        if authenticate_user(username, password):
            # Utente autenticato, fai qualcosa
            return redirect("/templ")
        else:
            # Autenticazione fallita, gestisci l'errore
            return "Credenziali non valide. Riprova."

    # Se il metodo della richiesta è GET, restituisci la pagina di login
    return render_template('login.html')

# Route per la pagina di registrazione
@app.route('/registrazione', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se l'utente è già registrato nel database
        if is_user_registered(username):
            # Utente già registrato, gestisci l'errore
            return "L'utente è già registrato. Prova a effettuare il login."

        # Genera il salt casuale
        salt = bcrypt.gensalt().decode('utf-8')

        # Genera l'hash della password utilizzando il salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

        # Registra il nuovo utente nel database
        register_user(username, hashed_password, salt)

        # Utente registrato con successo, fai qualcosa
        return "Registrazione completata con successo!"

    # Se il metodo della richiesta è GET, restituisci la pagina di registrazione
    return render_template('registrazione.html')

# Funzione per l'autenticazione dell'utente nel database
def authenticate_user(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Esegui la query per ottenere l'hash della password e il salt corrispondente all'utente
    query = "SELECT password, salt FROM users WHERE username=?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        hashed_password, salt = result
        # Genera l'hash della password inserita utilizzando il salt memorizzato
        entered_password_hash = bcrypt.hashpw(password.encode('utf-8'), bytes(salt, 'utf-8')).decode('utf-8')

        # Confronta l'hash generato con l'hash memorizzato nel database
        if entered_password_hash == hashed_password:
            # Le credenziali sono corrette, l'utente è autenticato
            return True

    conn.close()
    return False

# Funzione per verificare se l'utente è già registrato nel database
def is_user_registered(username):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Esegui la query per verificare se l'utente è già presente nel database
    query = "SELECT * FROM users WHERE username=?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    conn.close()

    return result is not None

# Funzione per registrare un nuovo utente nel database
def register_user(username, hashed_password, salt):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Inserisci i dati dell'utente nel database
    query = "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)"
    cursor.execute(query, (username, hashed_password, salt))

    conn.commit()
    conn.close()



if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80,threads=4)
