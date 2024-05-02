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
    tool_type = "SAST"
    tool_name = "Semgrep"
    semgrep_info = document.get('AnalysisElements', {}).get(tool_type, {}).get(tool_name, {})
    semgrep_token = semgrep_info.get('SemgrepToken')
    semgrep_project = semgrep_info.get('SemgrepProject')
    semgrep_organization_slug = semgrep_info.get('SemgrepOrganizationSlug')
    existing_ids = [vulnerability['Id'] for vulnerability in document.get('AnalysisResults')]

    # Verificando se os dados estão presentes presente antes de acessar
    if semgrep_token and semgrep_project and semgrep_organization_slug and project_name:
        try:
            # Chamada à API Semgrep
            headers = {'Authorization': f"Bearer {semgrep_token}"}
            url = f"https://semgrep.dev/api/v1/deployments/{semgrep_organization_slug}/findings?repos={semgrep_project}"
            response = requests.get(url, headers=headers)

            # Verificando se a requisição foi bem-sucedida
            if response.status_code == 200:
                logging.info("Resposta da API obtida com sucesso")  # Verificando se a resposta foi obtida com sucesso
                selected_fields = process_response(project_name, tool_type, tool_name, response.json(), existing_ids)
                try:
                    update_document = UpdateDocument()
                    update_document.update_document(db_instance, document['_id'], selected_fields, collection)
                except Exception as e:
                    logging.info(f"Erro ao atualizar os dado no documento: {e}")
            else:
                logging.error(f"Erro na requisição Semgrep: {response.status_code} - {response.text}")

        except Exception as e:
            logging.exception(f"Erro ao processar o documento {document['_id']}: {e}")

def process_response(project_name, tool_type, tool_name, response_data, existing_ids):
    # Extrair os campos específicos e salvar no MongoDB
    selected_fields = []
    for finding in response_data.get('findings', []):
        if finding.get('id') not in existing_ids:
            _filter = {
                'Id': finding['id'],
                'ProjectName': project_name,
                'ToolType': tool_type,
                'ToolName': tool_name,
                'Title': finding['rule_name'],
                'Severity': finding['severity'],
                'Description': finding['rule_message'],
                'Local': f"{finding.get('location', {}).get('file_path')},{finding.get('location', {}).get('line')}",
                'Status': finding['state'],
                'CreationDate': finding['relevant_since'],
            }
            selected_fields.append(_filter)

    return selected_fields
    
if __name__ == "__main__":
    fetch_data = DataFetcher()
    try:
        DataFetcher.fetch_data(process_document)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
