import azure.functions as func
import logging
from zanshin import Zanshin

app = func.FunctionApp()

@app.route(route="zanshin", auth_level=func.AuthLevel.ANONYMOUS)
def http_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Instanciando a classe Zanshin
    zanshin = Zanshin()
    
    try:
        # Chamando o inicializador do processo de busca de dados da classe
        zanshin.__init__()
        return func.HttpResponse("This HTTP triggered function executed successfully.", status_code=200)
    except Exception as e:
        logging.error(f"Erro ao buscar dados: {e}")
        return func.HttpResponse("Erro ao buscar dados", status_code=500)
