import logging
from common.mongodb_connector import MongoDB

class UpdateDocument:
    @staticmethod
    def update_document(db_instance, document_id, selected_history_fields, selected_snapshot_fields, collection, tool_type, tool_name):
        
        logging.info("Iniciando a execução do script update_document")
        
        try:
            with MongoDB() as db_instance:
                query = {'_id': document_id}  
                
                # Atualizar o histórico apenas se houver novos campos selecionados
                if selected_history_fields is not None and selected_history_fields:
                    update_query_history = {'$addToSet': {'AnalysisResultsHistory': {'$each': selected_history_fields}}}
                    db_instance.update_document(collection, query, update_query_history)
                
                # Sempre atualizar o instantâneo
                update_query_snapshot = {'$set': {f'AnalysisResultsSnapshot.{tool_type}.{tool_name}': selected_snapshot_fields}}
                
                # Garantir que a coleção seja passada como uma string
                if isinstance(collection, str):
                    db_instance.update_document(collection, query, update_query_snapshot)
                else:
                    logging.error("O nome da coleção não é uma string")
        
        except Exception as e:
            logging.exception(f"Ocorreu um erro ao processar os documentos: {e}")