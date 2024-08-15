import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
import yaml
from datetime import datetime

random.seed(100)
#load db credenntials
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



#url for invoking API
invoke_url = 'https://pzp2pscs5m.execute-api.us-east-1.amazonaws.com/v1'

# Function to send data to Kafka topics via the API


def send_data_to_kafka(data, topic):
    url = f"{invoke_url}/topics/{topic}"
    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}

    # payload is a list of records
    payload = json.dumps({
        "records": [
            {"value": data}
        ]
    })

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raises exception for HTTP errors
        print(f"Sent data to {topic}: Status Code: {
              response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Kafka: {e}")

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
                send_data_to_kafka(pin_result, "0e2685691ff5.pin")

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)
                geo_result['timestamp'] = geo_result['timestamp'].isoformat()
                # Send geolocation data to the corresponding Kafka topic
                send_data_to_kafka(geo_result, "0e2685691ff5.geo")

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
                user_result['date_joined'] = user_result['date_joined'].isoformat()
                # Send user data to the corresponding Kafka topic
                send_data_to_kafka(user_result, "0e2685691ff5.user")

            print("Sent data to Kafka topics.")

            


if __name__ == "__main__":
    new_connector = AWSDBConnector()
    run_infinite_post_data_loop()
    print('Working')

    
    
    


