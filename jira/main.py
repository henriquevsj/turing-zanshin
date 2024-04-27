import sys
sys.path.append('../microservices')
import logging
from jira import JIRA
from common.mongodb_fetch_data import DataFetcher

def process_document(db_instance, collection, document):

    # Obter as informações necessárias do documento
    project_name = document['ProjectName']
    jira_info = document['AnalysisElements']['Jira']
    jira_project_key = jira_info['JiraProjectKey']
    jira_customfield_id = jira_info['JiraCustomFieldId']
    jira_username = jira_info['JiraUserName']
    jira_token = jira_info['JiraToken']
    jira_url = jira_info['JiraURL']
    jira_selected_tools = jira_info['SelectedTools']

    # Para criar o item no Jira é necessario fazer a chamada da API previamente contendo uma variavel com o numero do customfield para isso:
    # Criando o nome da variável dinamicamente
    customfield = f"customfield_{jira_customfield_id}"

    # Atribuindo à variável dinâmica
    globals()[customfield] = customfield

    if jira_project_key and jira_customfield_id and jira_username and jira_token and jira_url and jira_selected_tools and project_name:

        # Resgatando os dados preexistentes no Jira relacionados a Security
        jira_client = JIRA(basic_auth=(jira_username, jira_token), options={'server': jira_url})
        jira_search = jira_client.search_issues(f"project={jira_project_key} AND type = Security ", json_result=True, fields=customfield)
        jira_issues = jira_search['issues']

        vulnerabilities_result_list = []

        # Iterar sobre as categorias de ferramentas
        for category, tools in jira_selected_tools.items():

            # Iterar sobre as ferramentas selecionadas
            for tool_value, tool_name in tools.items():
                
                # Obter resultados de análise para a ferramenta e categoria específicas
                analysis_results = document["AnalysisResults"]
                
                # Executar consulta ao MongoDB para cada ferramenta
                for result in analysis_results:                    
                    vulnerabilities_result_list.append(result)

    get_keys (jira_issues, customfield, vulnerabilities_result_list, category, project_name, tool_name, jira_client, jira_project_key)

def get_keys (jira_issues, customfield, vulnerabilities_result_list, category, project_name, tool_name, jira_client, jira_project_key): 
    # Criando e populando a lista de vulnerabilidades presentes no Jira
    jira_vulnerability_id_list = []
    
    for i in jira_issues:  
        fields = i['fields']  
        
        if fields and customfield in fields:
            customfield_value = fields[customfield]
            
            if customfield_value is None:
                continue
            else:
                jira_vulnerability_id_list.append(str(customfield_value))
    
    for vulnerability_unity_content in vulnerabilities_result_list: 
        vulnerability_id = vulnerability_unity_content['Id']

        if vulnerability_id in jira_vulnerability_id_list:
            continue
        else:
            create_issue (customfield, category, project_name, tool_name, jira_client, jira_project_key, vulnerability_id, vulnerability_unity_content)

# Função para criar issues no Jira com base nos resultados de análise
def create_issue (customfield, category, project_name, tool_name, jira_client, jira_project_key, vulnerability_id, vulnerability_unity_content):
    
    # concertar o I
    summary = f"{category} - Project {project_name} - {vulnerability_unity_content['Description'][:200]}"
    description = ( f"Assessment type: {category}\n" f"Tool name: {tool_name}\n" f"Description: {vulnerability_unity_content['Description']}\n" f"Local: {vulnerability_unity_content['Local']}\n")
    try:
        # Substituindo a variável customfield pela variável dinâmica correspondente
        jira_client.create_issue (project=jira_project_key, summary=summary, **{customfield: vulnerability_id}, description=description, issuetype={'name': 'Security'} )
        print(f"Task Id:{vulnerability_id} Successfully created!")

    except Exception as error:
        logging.exception (f"Erro ao criar uma task no Jira do tipo 'Vulnerabilidade'! \n Id: " f"{vulnerability_id}" f"\n{error}")

if __name__ == "__main__":
    fetch_data = DataFetcher()
    try:
        fetch_data.fetch_data (process_document)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")