from socket import gethostname, gethostbyname

FORMAT = "utf-8" 
MAX_PKT_SIZE = 64 #tamanho fixo do primeiro pacote
DEFAULT_PORT = 8000
HOST = gethostbyname(gethostname())