from flask import Flask, request, render_template, session,redirect
from util.auth_utils import is_logged_in
from waitress import serve

app = Flask(__name__)
app.secret_key = 'mysecret'

@app.route('/mySite')
def my_site():
    if is_logged_in(session):
       username = session.get('username')
       print(username)
       return render_template('AreaRiservata.html', username=username)
    else:
       return 'Utente non autenticato'

@app.route('/logout')
def logout():
    # Rimuovi la sessione
    session.clear()
    return redirect("/")


if __name__ == '__main__':
   serve(app, host='0.0.0.0', port=80, threads=4)


#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80)

