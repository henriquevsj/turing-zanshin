import azure.functions as func
import logging
from zanshin import Zanshin

app = func.FunctionApp()

@app.route(route="zanshin", auth_level=func.AuthLevel.ANONYMOUS)
def zanshin(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:             
        zanshin = Zanshin()        
        try:
            zanshin.__init__()
            return func.HttpResponse("Zanshin processing completed successfully.", status_code=200)
        except Exception as e:
            logging.error(f"Erro ao processar Zanshin: {e}")
            return func.HttpResponse("Erro ao processar Zanshin", status_code=500)
