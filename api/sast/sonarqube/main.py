import sys
sys.path.append('../microservices')
import logging
from common.mongodb_fetch_data import DataFetcher
from common.mongodb_update_document import UpdateDocument
from sonarqube import SonarQubeClient

logging.basicConfig(level=logging.INFO)  # Configurando o nível de log para INFO

def process_document(db_instance, collection, document):
    # Obter as informações necessárias do documento
    tool_type = "SAST"
    tool_name = "SonarQube"
    project_name = document['ProjectName']
    sonar_info = document['AnalysisElements'][tool_type][tool_name]
    sonar_project = sonar_info['SonarProject']
    sonar_url = sonar_info['SonarURL']
    sonar_username = sonar_info['SonarUserName']
    sonar_token = sonar_info['SonarToken']

    # Obter os IDs existentes na coleção para posteriormente comparar e criar apenas 
    existing_ids = [vulnerability['Id'] for vulnerability in document.get('AnalysisResults')]

    # Verificando se os dados estão presentes presente antes de acessar
    if sonar_project and sonar_url and sonar_username and sonar_token and project_name:
        # Conexão OAuth SonarQube
        sonar_client = SonarQubeClient(sonarqube_url=sonar_url, username=sonar_username, token=sonar_token)
        try:
            selected_fields = process_response(project_name, tool_type, tool_name, sonar_client, sonar_project, existing_ids)
            try:
                update_document = UpdateDocument ()
                update_document.update_document(db_instance, document['_id'], selected_fields, collection)
            except Exception as e:
                logging.info(f"Erro ao atualizar os dados: {e}")

        except Exception as e:
            logging.exception(f"Erro ao processar o documento {document['_id']}: {e}")

def process_response(project_name, tool_type, tool_name, sonar_client, sonar_project, existing_ids):
    # Inicializar a lista para armazenar todos os resultados
    selected_fields = []

    # Número da página inicial
    page = 1
    
    while True:
        # Obter a resposta da API do SonarQube para uma página específica
        issues_in_sonar_response = sonar_client.issues.search_issues(componentKeys=sonar_project, p=page)
        
        # Verificar se há resultados
        if not issues_in_sonar_response['issues']:
            break
        
        # Adicionar apenas os campos desejados à lista
        for issue in issues_in_sonar_response['issues']:
            if issue.get('key') not in existing_ids:
                _filter = {
                    'Id': issue.get('key'),
                    'ProjectName': project_name,
                    'ToolType': tool_type,
                    'ToolName': tool_name,
                    'Title': issue.get('message'),
                    'Severity': issue.get('severity'),
                    'Description': issue.get('message'),
                    'Local': f"{issue.get('component')}, {issue.get('line')}",
                    'Status': issue.get('status'),
                    'CreationDate': issue.get('creationDate')
                }
                selected_fields.append(_filter)
        
        # Avançar para a próxima página
        page += 1
    return selected_fields

if __name__ == "__main__":
    fetch_data = DataFetcher()
    try:
        fetch_data.fetch_data(process_document)
    except Exception as e:
        logging.info(f"Erro ao buscar dados: {e}")