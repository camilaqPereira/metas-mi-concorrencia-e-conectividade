from socket import gethostname, gethostbyname

FORMAT = "utf-8" 
MAX_PKT_SIZE = 64 #tamanho fixo do primeiro pacote
DEFAULT_PORT = 8000
HOST = gethostbyname(gethostname())

#Metodos
METHOD_BUY = "!BUY"
METOHD_GETROUTES = "!GETROUTES"
METHOD_CREATE_USER = "!CREATEUSER"
METHOD_GETTOKEN = "!GETTOKEN"
METHOD_GETTICKETS = "!GETTICKETS"

#Tipos de dados
ROUTE_TYPE = "!ROUTE"
TICKET_TYPE = "!TICKET"
TOKEN_TYPE = "!TOKEN"
NO_DATA_TYPE = "!NONE"

#Status
OK = 100
BAD_TOKEN = 220
OPERATION_FAILED = 240
NOT_FOUND = 260
