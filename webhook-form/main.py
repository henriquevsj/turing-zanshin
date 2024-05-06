import sys
sys.path.append('../turing-core/api')
from common.mongodb_connector import MongoDB
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import logging
import os
import uvicorn

app = FastAPI()

logging.basicConfig(level=logging.INFO)  # Configurando o nível de log para INFO

@app.route("/")
def home(request: Request):
    return PlainTextResponse("Flask Vercel Example - Hello World", status_code=200)

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Criando uma instância da classe MongoDB usando um gerenciador de contexto
        with MongoDB() as db_instance:
            analysis_elements = await request.json()  # Obtém os dados da requisição POST

            if analysis_elements:
                # Insere os dados no banco de dados usando a instância MongoDB
                inserted_id = db_instance.db['tenchi_security'].insert_one(analysis_elements).inserted_id
                    
                logging.info(f"ID do documento: {inserted_id}")

                # Atualiza o documento recém-inserido com os dados específicos
                update_query = {'_id': inserted_id}
                update_data = {'$set': {'AnalysisElements': analysis_elements}}
                db_instance.db['tenchi_security'].update_one(update_query, update_data)

                logging.info(f"Dados atualizados com sucesso para o documento com ID: {inserted_id}")
                
                response = {'message': 'Data inserted and updated successfully', 'inserted_id': str(inserted_id)}
                return response, 200
            
            else:
                logging.error("Nenhum dado recebido do webhook")  # Log para indicar que nenhum dado foi recebido
                return {'error': 'No data received'}, 400
            
    except Exception as e:
        logging.exception(f"Erro ao processar o webhook: {e}")  # Log para indicar o erro ocorrido
        return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
