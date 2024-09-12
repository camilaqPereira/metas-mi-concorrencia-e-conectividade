import json
import datetime

class Response:
    def __init__(self, timestamp = datetime.datetime.now(), status = 0, data = None, rs_type = ''):
        self.timestamp = timestamp
        self.status = status
        self.data = data
        self.rs_type = rs_type

    def to_json(self):
        response = {'type':self.rs_type, 'timestamp':self.timestamp.strftime('%d/%m/%y %H:%M:%S'), 'status':self.status, 'data':self.data}

        json_str = json.dumps(response)

        return json_str

    def from_json(self, json_str: str):
        response = json.loads(json_str)

        self.data = response['data']
        self.rs_type = response['type']
        self.timestamp = response['timestamp']
        self.status = response['status']