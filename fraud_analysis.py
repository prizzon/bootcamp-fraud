import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('AZURE_FORM_RECOGNIZER_KEY')
endpoint = os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT')
model_id = "prebuilt-invoice"

def analyze_invoice(file):
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/pdf'
    }

    analyze_url = f"{endpoint}/formrecognizer/documentModels/{model_id}:analyze?api-version=2023-07-31"

    response = requests.post(analyze_url, headers=headers, data=file)
    response.raise_for_status()
    analysis = response.json()

    # Identificar campos suspeitos e possíveis fraudes
    anomalies = detect_anomalies(analysis)
    return {"analysis": analysis, "anomalies": anomalies}

def detect_anomalies(analysis):
    anomalies = []
    try:
        fields = analysis['documents'][0]['fields']
        # Verificação de valores inesperados
        if fields['TotalAmount']['value'] > 10000:  # Exemplo de limite alto
            anomalies.append("Valor total acima do esperado.")
        if fields['InvoiceDate']['value'] is None:
            anomalies.append("Data da fatura ausente.")
        if fields['VendorName']['value'] != "Empresa Autorizada":
            anomalies.append("Nome do fornecedor diferente do esperado.")
    except KeyError as e:
        anomalies.append(f"Erro ao processar campos: {e}")
    return anomalies
