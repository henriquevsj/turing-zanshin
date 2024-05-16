import azure.functions as func
import logging
from zanshin import Zanshin

app = func.FunctionApp()

@app.route(route="HttpExample", auth_level=func.AuthLevel.ANONYMOUS)
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
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
            zanshin.process_document()
            return func.HttpResponse("This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.", status_code=200)
        except Exception as e:
            logging.error(f"Erro ao buscar dados: {e}")
            return func.HttpResponse("Erro ao buscar dados", status_code=500)
