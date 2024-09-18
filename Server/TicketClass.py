import json
from datetime import datetime
import os
import sys

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PARENT_DIR)
from Server.utils import TICKETS_FILE_PATH

class Ticket:
    def __init__(self, email='', routes=None):
        self.email = email
        self.timestamp = datetime.now()
        self.routes = routes

    def save(self):
        data = {'timestamp': self.timestamp.strftime('%d/%m/%y %H:%M:%S'), 'routes': self.routes}
        try:
            with open(TICKETS_FILE_PATH, 'x+') as file:
                json.dump({self.email: [data]}, file)
        except FileExistsError:
            with open(TICKETS_FILE_PATH, 'r+') as file:
                all_tickets = json.load(file)
                if self.email in all_tickets:
                    all_tickets.get(self.email).append(data)
                else:
                    all_tickets[self.email] = [data]
                file.seek(0)
                json.dump(all_tickets, file)

    def from_json(self, json_str):
        values = json.loads(json_str)

        self.email = values['email']
        self.timestamp = datetime.strptime(values['timestamp'], '%d/%m/%y %H:%M:%S')
        self.routes = values['routes']

    def to_json(self):
        json_str = {'email': self.email, 'timestamp':self.timestamp.strftime('%d/%m/%y %H:%M:%S'), 'routes':self.routes}

        return json_str