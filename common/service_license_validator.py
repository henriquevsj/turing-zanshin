import logging
import os
import requests

class LicenseValidator:
    def __init__(self):
        self.license_service_login_url = os.getenv('LICENSE_SERVICE_LOGIN_URL')
        self.license_service_verify_url = os.getenv('LICENSE_SERVICE_VERIFY_URL')
        self.username = os.getenv('LICENSE_SERVICE_USERNAME')
        self.password = os.getenv('LICENSE_SERVICE_PASSWORD')
        self.token = None

    def get_token(self):
        try:
            response = requests.post(self.license_service_login_url, json={
                "username": self.username,
                "password": self.password
            })

            if response.status_code == 200:
                self.token = response.json().get('token')
                if self.token:
                    return True
                else:
                    logging.error("Token not found in the response")
                    return False
            else:
                logging.error(f"Failed to login: {response.text}")
                return False
        except Exception as e:
            logging.error(f"Error during login: {e}")
            return False

    def verify_license(self):
        if not self.token:
            if not self.get_token():
                return False

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(self.license_service_verify_url, headers=headers, json={"token": self.token})

            if response.status_code == 200:
                return True
            else:
                logging.error(f"License validation failed: {response.text}")
                return False
        except Exception as e:
            logging.error(f"Error verifying the token: {e}")
            return False
