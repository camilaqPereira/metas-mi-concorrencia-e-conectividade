import json
from datetime import datetime


class Ticket:
    def __init__(self, email='', timestamp = datetime.now(), routes=None):
        self.email = email
        self.timestamp = timestamp
        self.routes = routes

    def from_json(self, json_str):
        values = json.loads(json_str)

        self.email = values['email']
        self.timestamp = datetime.strptime(values['timestamp'], '%d/%m/%y %H:%M:%S')
        self.routes = values['routes']

    def to_json(self):
        json_str = {'email': self.email, 'timestamp':self.timestamp.strftime('%d/%m/%y %H:%M:%S'), 'routes':self.routes}

        return json_str