from enum import Enum
import socket
import json
import datetime
from Client.utils import *

class ConstantsManagement(Enum):
    # Métodos de requisições
    BUY = "BUY"
    GETROUTES = "GETROUTES"
    CREATE_USER = "CREATEUSER"
    GETTOKEN = "GETTOKEN"
    GETTICKETS = "GETTICKETS"

    #Tipos de dados de retorno
    ROUTE_TYPE = "ROUTE"
    TICKET_TYPE = "TICKET"
    TOKEN_TYPE = "TOKEN"
    NO_DATA_TYPE = "NONE"
    NETWORK_FAIL = "NETWORK_FAIL"

    #Status
    OK = 100
    INVALID_TOKEN = 220
    OPERATION_FAILED = 240
    NOT_FOUND = 260
    NETWORK_ERROR = 280

    #Conection infos
    FORMAT = "utf-8" 
    MAX_PKT_SIZE = 64 #tamanho fixo do primeiro pacote em bytes
    DEFAULT_PORT = 8000
    HOST = socket.gethostbyname(socket.gethostname())


class Request:
    def __init__(self, rq_type: str = '', rq_data: any = None, client_token:str = ''):
        self.rq_type = rq_type
        self.rq_data = rq_data
        self.client_token = client_token

    def to_json(self):
        values = {"type":self.rq_type, "data":self.rq_data, "token":self.client_token}
        json_str = json.dumps(values)

        return json_str

    def from_json(self, json_str: str):
        values = json.loads(json_str)
        self.rq_type = values['type']
        self.rq_data = values['data']
        self.client_token = values['token']


class Response:
    def __init__(self, status = 0, data = None, rs_type = ''):
        self.timestamp = datetime.datetime.now()
        self.status = status
        self.data = data
        self.rs_type = rs_type

    def to_json(self):
        response = {'type':self.rs_type, 'timestamp':self.timestamp.strftime('%d/%m/%Y %H:%M:%S'), 'status':self.status, 'data':self.data}

        json_str = json.dumps(response)

        return json_str

    def from_json(self, json_str: str):
        response = json.loads(json_str)

        self.data = response['data']
        self.rs_type = response['type']
        self.timestamp = datetime.datetime.strptime(response['timestamp'], '%d/%m/%Y %H:%M:%S')
        self.status = response['status']

class Ticket:
    def __init__(self, email='', routes=None):
        self.email = email
        self.timestamp = datetime.datetime.now()
        self.routes = routes

    def save(self):
        data = {'timestamp': self.timestamp.strftime('%d/%m/%Y %H:%M:%S'), 'routes': self.routes}
        try:
            with open(FilePathsManagement.TICKETS_FILE_PATH.value, 'x+') as file:
                json.dump({self.email: [data]}, file)
        except FileExistsError:
            with open(FilePathsManagement.TICKETS_FILE_PATH.value, 'r+') as file:
                all_tickets = json.load(file)
                if self.email in all_tickets:
                    all_tickets.get(self.email).append(data)
                else:
                    all_tickets[self.email] = [data]
                file.seek(0)
                json.dump(all_tickets, file)

    def from_json(self, values):
        self.email = values['email']
        self.timestamp = datetime.datetime.strptime(values['timestamp'], '%d/%m/%Y %H:%M:%S')
        self.routes = values['routes']

    def to_json(self):
        json_str = {'email': self.email, 'timestamp':self.timestamp.strftime('%d/%m/%Y %H:%M:%S'), 'routes':self.routes}

        return json_str

