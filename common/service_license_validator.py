import logging
import jwt
import datetime
import os
import azure.functions as func

class LicenseValidator:
    def __init__(self):      
        # Definindo a chave secreta usada para assinar os tokens
        self.secret_key = "Ainda assim, existem dúvidas a respeito de como o julgamento imparcial das eventualidades ainda não demonstrou convincentemente que vai participar na mudança dos paradigmas corporativos."

    def verify_license(self):
        # Obtendo o token do cabeçalho da solicitação
        token = os.getenv('TURING_LICENSE_TOKEN')
        logging.info(f"Token: {token}")
        
        try:
            if not token or not token.startswith("Bearer "):
                logging.info("Token is missing or invalid format", status_code=401)
                return func.HttpResponse("Token is missing or invalid format", status_code=401)
        except Exception as e:
            logging.error(f"oken is missing or invalid format: {e}")
            return False
            
        try:
            # Remover o prefixo "Bearer " do token, caso esteja presente
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            decoded_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            logging.info(f"Token decodificado: {decoded_token}")
            
            expiration = decoded_token.get('exp')
            if expiration and datetime.datetime.fromtimestamp(expiration, datetime.timezone.utc) < datetime.datetime.now(datetime.timezone.utc):
                logging.error("License has expired.")
                return False
            return True
        
        except jwt.ExpiredSignatureError:
            logging.error("License token has expired.")
            return False
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid license token: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro ao verificar o token: {e}")
            return False