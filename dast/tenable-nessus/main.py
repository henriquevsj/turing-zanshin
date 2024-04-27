import sys
sys.path.append('../microservices')
import logging
import requests
import uuid
from common.mongodb_fetch_data import DataFetcher
from common.mongodb_update_document import UpdateDocument
from datetime import datetime

logging.basicConfig(level=logging.INFO)  # Configurando o nível de log para INFO

def process_document(db_instance, collection, document):
    # Obter as informações necessárias do documento
    project_name = document.get('ProjectName')
    tool_type = "DAST"
    tool_name = "TenableNessus"
    nessus_info = document.get('AnalysisElements', {}).get(tool_type, {}).get(tool_name, {})
    nessus_access_key = nessus_info.get('NessusAccessKey')
    nessus_secret_key = nessus_info.get('NessusSecretKey')
    nessus_url = nessus_info.get('NessusURL')
    nessus_scan_id = nessus_info.get('NessusScanId')
    existing_ids = [vulnerability['Id'] for vulnerability in document.get('AnalysisResults')]

    # Verificando se os dados estão presentes presente antes de acessar
    if nessus_access_key and nessus_secret_key and nessus_url and project_name:
        try:
            # Chamada à API Nessus
            headers = {"X-ApiKeys": f"accessKey={nessus_access_key}; secretKey={nessus_secret_key}",}
            url = f"{nessus_url}/scans/{nessus_scan_id}"
            response = requests.get(url, headers=headers, verify=False)

            # Verificando se a requisição foi bem-sucedida
            if response.status_code == 200:
                logging.info("Resposta da API obtida com sucesso")  # Verificando se a resposta foi obtida com sucesso
                selected_fields = process_response(response.json(), nessus_scan_id, nessus_url, headers, project_name, tool_type, tool_name, existing_ids)  # Passando as variáveis necessárias
                try:
                    update_document = UpdateDocument()
                    update_document.update_document(db_instance, document['_id'], selected_fields, collection)
                except Exception as e:
                    logging.info(f"Erro ao atualizar os dado no documento: {e}")
            else:
                logging.error(f"Erro na requisição: {response.status_code} - {response.text}")

        except Exception as e:
            logging.exception(f"Erro ao processar o documento {document['_id']}: {e}")
       
def process_response(response_data, nessus_scan_id, nessus_url, headers, project_name, tool_type, tool_name, existing_ids):
    selected_fields = []
    local = response_data.get('info', {}).get('targets')
    date = datetime.fromtimestamp(int(response_data.get('info', {}).get('scan_start_timestamp'))).strftime('%d/%m/%Y %H:%M:%S')
    vulnerability_id = f"{nessus_scan_id}-{str(uuid.uuid1())}"

    for finding in response_data.get('vulnerabilities', []):
        
        url = f"{nessus_url}/plugins/plugin/{finding.get('plugin_id')}"
        plugin_response = requests.get(url, headers=headers, verify=False)
        plugin_data = plugin_response.json()
        attributes = plugin_data.get('attributes', [])
        description_value = next((attr.get('attribute_value') for attr in attributes if attr.get('attribute_name') == 'description'), None)
        risk_value = next((attr.get('attribute_value') for attr in attributes if attr.get('attribute_name') == 'risk_factor'), None)
        
        if vulnerability_id not in existing_ids:
            # Extrair os campos específicos e salvar no MongoDB
            _filter = {
                'Id': vulnerability_id,
                'ProjectName': project_name,
                'ToolType': tool_type,
                'ToolName': tool_name,
                'Title': finding.get('plugin_name'),
                'Severity': risk_value,
                'Description': description_value,
                'Local': local,
                'Status': '',
                'CreationDate': date,
            }
            selected_fields.append(_filter)
    return selected_fields

if __name__ == "__main__":
    fetch_data = DataFetcher()
    try:
        fetch_data.fetch_data (process_document)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
