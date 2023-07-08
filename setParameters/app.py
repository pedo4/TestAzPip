from flask import Flask, request, render_template,redirect,jsonify
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
CORS(app)


 
    

@app.route('/par', methods=['POST'])
def handle_par_request():
    template_type = request.form['templateType']
    if template_type == 'ecommerce':
        return redirect('/ecomm')
    elif template_type == 'news':
        return redirect('/news')
    else:
        return redirect('/corp')
    

if __name__ == '__main__':
   serve(app, host='0.0.0.0', port=80, threads=4)


#if __name__ == '__main__':
#   app.run(host='0.0.0.0', port=80)