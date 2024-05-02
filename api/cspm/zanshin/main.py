import sys
sys.path.append('../microservices')
import logging
import requests
from common.mongodb_fetch_data import DataFetcher
from common.mongodb_update_document import UpdateDocument

logging.basicConfig(level=logging.INFO)  # Configurando o nível de log para INFO

def process_document(db_instance, collection, document):
    # Obter as informações necessárias do documento
    project_name = document.get('ProjectName')
    tool_type = "CSPM"
    tool_name = "Zanshin"
    zanshin_info = document.get('AnalysisElements', {}).get(tool_type, {}).get(tool_name, {})
    zanshin_token = zanshin_info.get('ZanshinToken')
    zanshin_url = zanshin_info.get('ZanshinURL')
    zanshin_organization_id = zanshin_info.get('ZanshinOrganizationId')
    existing_ids = [vulnerability['Id'] for vulnerability in document.get('AnalysisResults')]

    # Verificando se os dados estão presentes presente antes de acessar
    if zanshin_token and zanshin_url and zanshin_organization_id:
        try:
            # Chamada à API Zanshin
            headers = {'accept': 'application/json','Authorization': f'Bearer {zanshin_token}','Content-Type': 'application/json'}
            url = f"{zanshin_url}/alerts"
            payload = {"organizationId": zanshin_organization_id,"page": 1,"pageSize": 25}
            response = requests.post(url, headers=headers, json=payload)

            # Verificando se a requisição foi bem-sucedida
            if response.status_code == 200:
                logging.info("Resposta da API obtida com sucesso")
                selected_fields = process_response(response.json(), project_name, tool_type, tool_name, zanshin_url, zanshin_token, existing_ids)
                try:
                    update_document = UpdateDocument()
                    update_document.update_document(db_instance, document['_id'], selected_fields, collection)
                except Exception as e:
                    logging.info(f"Erro ao atualizar os dado no documento: {e}")
            else:
                logging.error(f"Erro na requisição Zanshin: {response.status_code} - {response.text}")

        except Exception as e:
            logging.exception(f"Erro ao processar o documento {document['_id']}: {e}")

def process_response(response_data, project_name, tool_type, tool_name, zanshin_url, zanshin_token, existing_ids):
    alerts = response_data.get('data', [])
    selected_fields = []

    # Processamento dos alertas
    for alert in alerts:
        
        headers = {'accept': 'application/json','Authorization': f'Bearer {zanshin_token}', 'Content-Type': 'application/json'}
        url = f"{zanshin_url}/alerts/{alert.get('id')}"
        response_scantargets = requests.get(url, headers=headers)
        response_scantargets_json = response_scantargets.json()
        vulnerability_id = alert.get('id')

        if vulnerability_id not in existing_ids:
            _filter = {
                'Id': alert.get('id'),
                'ProjectName': project_name,
                'ToolType': tool_type,
                'ToolName': tool_name,
                'Title': alert.get('ruleTitle'),
                'Severity': alert.get('severity'),
                'Description': response_scantargets_json.get('rule'),
                'Local': alert.get('resource'),
                'Status': alert.get('state'),
                'CreationDate': alert.get('createdAt'),
            }
            selected_fields.append(_filter)

    return selected_fields

if __name__ == "__main__":
    fetch_data = DataFetcher()
    try:
        fetch_data.fetch_data(process_document)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
