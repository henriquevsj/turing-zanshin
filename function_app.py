import azure.functions as func
import logging
from zanshin import Zanshin

app = func.FunctionApp()

@app.route(route="zanshin", auth_level=func.AuthLevel.ANONYMOUS)
def http_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    zanshin = Zanshin()        
    try:
        zanshin.__init__()
        return func.HttpResponse("Zanshin processing completed successfully.", status_code=200)
    except Exception as e:
        logging.error(f"Erro ao processar Zanshin: {e}")
        return func.HttpResponse("Erro ao processar Zanshin", status_code=500)
