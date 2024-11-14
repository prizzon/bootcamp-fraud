import os
from flask import Flask, request, render_template, jsonify
from fraud_analysis import analyze_invoice
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo inválido"}), 400
    result = analyze_invoice(file)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)