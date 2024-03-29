from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time
client = KafkaClient(hosts="localhost:9092")

topic = client.topics['testBusDataNew']
# b in fromt of every topic name means it is stored in form of BYTES.

producer = topic.get_sync_producer()
# producer.produce('test_message from python'.encode('ascii'))
# To produce a random message.

input_file = open('./bus1.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']


def generate_uuid():
    return uuid.uuid4()


data = {}
data['busline'] = '00001'


def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        # print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)
        # if bus reaches last coordinate tell him to keep looping
        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1


generate_checkpoint(coordinates)
