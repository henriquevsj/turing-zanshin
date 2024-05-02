import sys
sys.path.append('../microservices')
import logging
import os
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Conecte-se ao banco de dados MongoDB
client = MongoClient(f"mongodb+srv://{os.environ.get("MONGO_USER_NAME")}:{os.environ.get('MONGO_PASSWORD')}@cluster01.it0lbcv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01")
db = client['doconnect_db']  # Altere 'mydatabase' para o nome do seu banco de dados
collection = db['tenchi_security']  # Altere 'projects' para o nome da sua coleção

logging.basicConfig(level=logging.INFO)  # Configurando o nível de log para INFO

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        analysis_elements = request.json  # Obtém os dados da requisição POST

        if analysis_elements:
            inserted_id = collection.insert_one(analysis_elements).inserted_id
                
            logging.info(f"ID do documento: {inserted_id}")

            # Atualiza o documento recém-inserido com os dados específicos
            update_query = {'_id': inserted_id}
            update_data = {'$set': {'AnalysisElements': analysis_elements}}
            collection.update_one(update_query, update_data)

            logging.info(f"Dados atualizados com sucesso para o documento com ID: {inserted_id}")
            
            response = {'message': 'Data inserted and updated successfully', 'inserted_id': str(inserted_id)}
            return jsonify(response), 200
        else:
            logging.error("Nenhum dado recebido do webhook")  # Log para indicar que nenhum dado foi recebido
            return jsonify({'error': 'No data received'}), 400
        
    except Exception as e:
        logging.exception(f"Erro ao processar o webhook: {e}")  # Log para indicar o erro ocorrido
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
