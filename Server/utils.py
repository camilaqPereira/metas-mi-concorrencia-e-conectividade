from socket import gethostname, gethostbyname
import os

FORMAT = "utf-8" 
MAX_PKT_SIZE = 64 #tamanho fixo do primeiro pacote
DEFAULT_PORT = 8000
HOST = gethostbyname(gethostname())

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
USERS_FILE_PATH = PARENT_DIR+'/DB/users.json'
TICKETS_FILE_PATH = PARENT_DIR+'/DB/tickets.json'
GRAPH_FILE_PATH = PARENT_DIR+'/DB/graph.json'
#Metodos
METHOD_BUY = "!BUY"
METHOD_GETROUTES = "!GETROUTES"
METHOD_CREATE_USER = "!CREATEUSER"
METHOD_GETTOKEN = "!GETTOKEN"
METHOD_GETTICKETS = "!GETTICKETS"

#Tipos de dados
ROUTE_TYPE = "!ROUTE"
TICKET_TYPE = "!TICKET"
TOKEN_TYPE = "!TOKEN"
NO_DATA_TYPE = "!NONE"
NETWORK_FAIL = "!NETWORK_FAIL"

#Status
OK = 100
BAD_TOKEN = 220
OPERATION_FAILED = 240
NOT_FOUND = 260
NETWORK_ERROR = 280
