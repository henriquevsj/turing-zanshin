from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self, timeout=5000, database_name=os.getenv('MONGO_DB_NAME')):
        self.connection_string = f"mongodb+srv://{os.getenv('MONGO_USER_NAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_URL')}/?retryWrites=true&w=majority&appName={os.getenv('MONGO_CLUSTER_NAME')}"
        self.timeout = timeout
        self.database_name = database_name
        self.client = None

    def __enter__(self):
        self.client = MongoClient(self.connection_string, connectTimeoutMS=self.timeout)
        self.db = self.client[self.database_name]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()

    def get_collections(self):
        return self.db.list_collection_names()

    def find_documents(self, collection_name):
        return self.db[collection_name].find()

    def update_document(self, collection_name, query, update, upsert=False):
        return self.db[collection_name].update_one(query, update, upsert=upsert)
    
