from flask import Flask, jsonify

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
@app.route('/', methods=['GET'])
def index():
    return render_template('template.html')

if __name__ == '__main__':
    app.run()