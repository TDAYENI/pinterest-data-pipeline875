import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
import yaml


random.seed(100)
with open('cred/db_creds.yaml', 'r') as f:
    db_cred = yaml.load(f, Loader=yaml.SafeLoader)



class AWSDBConnector:

    def __init__(self):
        
        self.HOST = db_cred['HOST']
        self.USER = db_cred['USER']
        self.PASSWORD = db_cred['PASSWORD']
        self.DATABASE = db_cred['DATABASE']
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()

invoke_url = 'https://pzp2pscs5m.execute-api.us-east-1.amazonaws.com/v1'

# Function to send data to Kafka topics via the API


def send_data_to_kafka(data, topic):
    url = f"{invoke_url}/{topic}"
    response = requests.post(url, json=data)
    print(f"Sent data to {topic}: Status Code: {
          response.status_code}, Response: {response.text}")

def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            
            print(pin_result)
            print(geo_result)
            print(user_result)


if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')

    
    
    


