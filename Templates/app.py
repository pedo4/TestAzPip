from flask import Flask, jsonify, render_template,session,redirect
from waitress import serve
from code.auth_utils import is_logged_in
from code.templ_utils import get_templates


app = Flask(__name__)

# Rotta per ottenere i template
@app.route('/template', methods=['GET'])
def get_templates():
    if(is_logged_in(session)):
        return jsonify(get_templates)
    else:
        return redirect("/login")

# Pagina principale
@app.route('/templ', methods=['GET'])
def index():
    if(is_logged_in(session)):
        return render_template('template.html')
    else:
        return redirect("/login")

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80,threads=4)