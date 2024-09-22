from hashlib import sha256
from DB.utils import *
from server.requests import *
import socket
from serverSide.customExceptions import InvalidTokenException, ClientNotFoundException

class ClientHandler:

    def __init__(self, conn, addr):  
        self.conn = conn
        self.addr = addr
    
    def create_user(self, email:str):
        token = sha256(email.encode(ConstantsManagement.FORMAT.value)).hexdigest()
        created_status = UsersData.save_user(email, token)
        return token if created_status else None

    def get_token(self, email:str):
        try:

            users:dict = UsersData.load_users()
            token = users.get(email)
            if token:
                return token
            else:
                raise ClientNotFoundException('Client not found')
        
        except FileExistsError:
           raise
        except ClientNotFoundException:
            print(f'[SERVER] {self.addr} Client not registered')
            raise 
    
    def auth_token(self, token = None):
        try:
            users:dict = UsersData.load_users()
            if (not token) or (token not in users.values()):
                raise InvalidTokenException('Token is not registered!')
            return True
        except FileExistsError:
           raise
        except InvalidTokenException:
            print(f'[SERVER] {self.addr} Invalid token')
            raise


    def buy_routes(self, server_data:ServerData, token:str, routes:list[tuple[str,str]]):
        try:
            email = self.__get_email(token)
            if server_data.dec_all_routes(routes):
                ticket = Ticket(email, routes)
                ticket.save()
                return ticket
            else:
                return None
        except FileNotFoundError:
            raise
        except ClientNotFoundException:
            raise
        
            
    def __get_email(self, token:str):
        try:
            users:dict[str,str] = UsersData.load_users()
            for user, client_token in users.items():
                if client_token == token:
                    return user
            
            raise(ClientNotFoundException('Client not found'))
        except FileNotFoundError:
            raise
        except ClientNotFoundException:
            print(f'[SERVER] {self.addr} Client not found')
            raise

        
    def get_tickets(self, token:str):
        try:
            email = self.__get_email(token)
            all_tickets:dict = Ticket.load_tickets()
            return all_tickets.get(email)

        except (ClientNotFoundException, FileNotFoundError):
            raise

    def receive_pkt(self):
        pkt = Request()
        try:
            pkt_size = self.conn.recv(ConstantsManagement.MAX_PKT_SIZE.value).decode(ConstantsManagement.FORMAT.value)
            if pkt_size:
                pkt_size = int(pkt_size)
                #recebendo segundo pacote -> requisição
                pkt.from_json(self.conn.recv(pkt_size).decode(ConstantsManagement.FORMAT.value))
        except socket.error as err:
            print(f"[SERVER] Package reception from {self.addr} failed! {str(err)}\n")
            pkt = None
        return pkt
    
    ##
    #   @brief: Realiza o envio de pacotes do cliente
    #
    #   @raises: OSError caso ocorra uma falha na conexão
    ##
    def send_pkt(self, pkt:Response):
        pkt_json = pkt.to_json()
        try:
            pkt_len = str(len(pkt_json)).encode(ConstantsManagement.FORMAT.value)
            pkt_len += b' ' * (ConstantsManagement.MAX_PKT_SIZE.value - len(pkt_len))
            self.conn.send(pkt_len)
            self.conn.send(pkt_json.encode(ConstantsManagement.FORMAT.value))
            status = True
        except socket.error as err:
            print(f"[SERVER] Package transfer to {self.addr} failed! {str(err)}\n")
            status = False
        return status
    