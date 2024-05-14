import logging
from mongodb_connector import MongoDB

class UpdateDocument:
    @staticmethod
    def update_document(db_instance, document_id, selected_fields, collection):
        
        logging.info("Iniciando a execução do script update_document")
        
        try:
            with MongoDB() as db_instance:
                query = {'_id': document_id}  
                update_query = {'$addToSet': {'AnalysisResults': {'$each': selected_fields}}}

                # Verifique se o nome da coleção é uma string antes de chamar o método update_document
                if isinstance(collection, str):
                    db_instance.update_document(collection, query, update_query)
                    logging.info("Documento atualizado")
                else:
                    logging.error("O nome da coleção não é uma string")
        
        except Exception as e:
            logging.exception(f"Ocorreu um erro ao processar os documentos: {e}")
