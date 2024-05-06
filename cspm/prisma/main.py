import sys
sys.path.append('../microservices')
from common.mongodb_fetch_data import DataFetcher
import logging
import requests

logging.basicConfig(level=logging.INFO)  # Configurando o nível de log para INFO

def process_document(db_instance, collection, document):
    project_name = document.get('ProjectName')
    tool_type = "CSPM"
    tool_name = "Prisma"
    prisma_info = document.get('AnalysisElements', {}).get(tool_type, {}).get(tool_name, {})
    prisma_access_key = prisma_info.get('PrismaAccessKey')
    prisma_secret_key = prisma_info.get('PrismaSecretKey')
    prisma_url = prisma_info.get('PrismaURL')
     
    if prisma_access_key and prisma_secret_key and prisma_url and project_name:
        try:
            url = prisma_url
            headers = {'Content-Type': 'application/json'}
            response = {'username': prisma_access_key,'password': prisma_secret_key}

            response = requests.post(url, headers=headers, json=response)

            if response.status_code == 200:
                response_json = response.json()
                jwt_token = response_json.get('token')
                if jwt_token:
                    print("JWT obtido com sucesso:", jwt_token)
                    return jwt_token
                else:
                    print("Token não encontrado na resposta JSON.")
                    return None
                
        except Exception as e:
            logging.exception(f"Erro ao obter JWT: {response.status_code} - {response.text}")
            return None

if __name__ == "__main__":
    fetch_data = DataFetcher()
    try:
        fetch_data.fetch_data(process_document)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")