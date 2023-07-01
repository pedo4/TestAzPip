from flask import Flask, jsonify, render_template
from waitress import serve

app = Flask(__name__)

# Dati dei template
templates = [
    {
        "type": "ecommerce",
        "icon": "e-commerce.png"
    },
    {
        "type": "news",
        "icon": "news.png"
    },
    {
        "type": "company",
        "icon": "enterprise.png"
    }
]

# Rotta per ottenere i template
@app.route('/template', methods=['GET'])
def get_templates():
    return jsonify(templates)

# Pagina principale
@app.route('/templ', methods=['GET'])
def index():
    return render_template('template.html')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80,threads=4)