import sys
sys.path.append('../microservices')
import logging
import pymsteams
import os
from common.mongodb_fetch_data import DataFetcher

def process_document(db_instance, collection, document):

    # Obter as informações necessárias do documento
    project_name = document['ProjectName']
    teams_info = document['AnalysisElements']['MsTeams']
    msteams_url = teams_info['MsTeamsWebhookURL']
    teams_selected_tools = teams_info['SelectedTools']

    if project_name and teams_info and msteams_url:
                
        vulnerabilities_result_list = []

        # Iterar sobre as categorias de ferramentas
        for category, tools in teams_selected_tools.items():

            # Iterar sobre as ferramentas selecionadas
            for tool_value, tool_name in tools.items():
                
                # Obter resultados de análise para a ferramenta e categoria específicas
                analysis_results = document["AnalysisResults"]
                
                # Executar consulta ao MongoDB para cada ferramenta
                for result in analysis_results:
                    if result.get("Status") == "OPEN":
                        vulnerabilities_result_list.append(result)
        
    process_response (msteams_url, vulnerabilities_result_list)

def process_response (msteams_url, vulnerabilities_result_list):

    # Criar uma mensagem apenas com as vulnerabilidades com status "OPEN"
    card = pymsteams.connectorcard(msteams_url)
    for vulnerability in vulnerabilities_result_list:
        message = f"ID: {vulnerability['Id']}\nTitle: {vulnerability['Title']}\nSeverity: {vulnerability['Severity']}\nDescription: {vulnerability['Description']}\n"
        card.text(message)
    assert card.send()

if __name__ == "__main__":
    
    fetch_data = DataFetcher()
    try:
        fetch_data.fetch_data (process_document)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")