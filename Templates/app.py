from flask import Flask, jsonify, render_template, session, redirect
from waitress import serve
from util.auth_utils import is_logged_in
from util.templ_utils import get_templates

app = Flask(__name__)
app.secret_key = "mysecret"

# Rotta per ottenere i template
@app.route('/template', methods=['GET'])
def get_temp():
    if is_logged_in(session):
        templates = get_templates()
        return jsonify(templates)
    else:
        return redirect("/login")

# Pagina principale
@app.route('/templ', methods=['GET'])
def index():
    print(session)
    if is_logged_in(session):
        return render_template('template.html')
    else:
        return redirect("/login")

if __name__ == '__main__':
   serve(app, host='0.0.0.0', port=80, threads=4)


#if __name__ == '__main__':
#   app.run(host='0.0.0.0', port=80)