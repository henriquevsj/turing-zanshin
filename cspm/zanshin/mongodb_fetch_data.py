import logging
from mongodb_connector import MongoDB

class DataFetcher:
    @staticmethod
    def fetch_data(process_document):
        """
        Método estático para buscar dados no MongoDB e chamar a função de processamento de documentos.
        Args:
            process_document (function): Função responsável por processar cada documento.
        Returns:
            None
        """
        logging.info("Iniciando a execução do script fetch_data")
        try:
            # Criando uma instância da classe MongoDB usando um gerenciador de contexto
            with MongoDB() as db_instance:
                logging.info("Conexão com o MongoDB estabelecida com sucesso")
                # Obtendo todas as coleções no banco de dados
                collections = db_instance.get_collections()

                # Iterando sobre cada coleção
                for collection in collections:
                    logging.info(f"Processando coleção: {collection}")
                    # Obtendo todos os documentos na coleção
                    documents = db_instance.find_documents(collection)

                    # Iterando sobre cada documento
                    for document in documents:
                        logging.info(f"Processando documento: {document['_id']}")
                        # Chama a função de processamento de documentos passando os parâmetros necessários
                        process_document(db_instance, collection, document)

        except Exception as e:
            logging.exception(f"Ocorreu um erro ao processar os documentos: {e}")
