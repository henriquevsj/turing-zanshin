from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import logging
from common.mongodb_connector import MongoDB
import uvicorn

app = FastAPI()

logging.basicConfig(level=logging.INFO)  

@app.get("/")
async def home():
    return PlainTextResponse("Flask Vercel Example - Hello World", status_code=200)

@app.post("/webhook")
async def webhook(request: Request):
    try:
        with MongoDB() as db_instance:
            analysis_elements = await request.json()  

            if analysis_elements:
                inserted_id = db_instance.db['tenchi_security'].insert_one(analysis_elements).inserted_id
                    
                logging.info(f"ID do documento: {inserted_id}")

                update_query = {'_id': inserted_id}
                update_data = {'$set': {'AnalysisElements': analysis_elements}}
                db_instance.db['tenchi_security'].update_one(update_query, update_data)

                logging.info(f"Dados atualizados com sucesso para o documento com ID: {inserted_id}")
                
                response = {'message': 'Data inserted and updated successfully', 'inserted_id': str(inserted_id)}
                return response, 200
            
            else:
                logging.error("Nenhum dado recebido do webhook")  
                return {'error': 'No data received'}, 400
            
    except Exception as e:
        logging.exception(f"Erro ao processar o webhook: {e}")  
        return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
