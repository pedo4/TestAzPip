from flask import Flask, request, render_template
from flask_cors import CORS
from code.parameters import get_parameter_names

app = Flask(__name__)
CORS(app)

@app.route('/par', methods=['POST'])
def handle_par_request():
    template_type = request.form['templateType']
    parameter_names = get_parameter_names(template_type)
    
    return render_template('template_params.html', parameter_names=parameter_names)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)