import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

# Load MongoDB URL from .env
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import pymongo

# ✅ Correct direct import (NO package export issue now)
from networksecurity.exception.exception import NetworkSecurityException


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # ✅ CSV → JSON conversion
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # ✅ Correct MongoDB insertion method
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            db = mongo_client[database]
            col = db[collection]

            col.insert_many(records)
            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = r"C:\Users\Lenovo\Desktop\network security\Network_Data\Phishing_Legitimate_full.csv"
    DATABASE = "Sachin_Database"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()

    records = networkobj.csv_to_json_convertor(FILE_PATH)
    no_of_records = networkobj.insert_data_to_mongodb(records, DATABASE, COLLECTION)

    print(f"✅ Successfully inserted {no_of_records} records into MongoDB")
