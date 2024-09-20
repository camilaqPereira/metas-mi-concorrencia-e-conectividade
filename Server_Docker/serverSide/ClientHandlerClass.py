from hashlib import sha256
from Server_Docker.DB.utils import *
from Server_Docker.server.requests import *
import socket
from json import load, dump, dumps
from threading import Lock

class ClientHandler:
    #Mutexes
    users_file_lock = Lock()
    tickets_file_lock = Lock()

    def __init__(self, conn:socket = None, addr = None):  
        self.conn = conn
        self.addr = addr
    
    def __create_token(self, email):
        return sha256(email.encode(ConstantsManagement.FORMAT.value)).hexdigest()
    
    def __load_users(self):
        try:
            with ClientHandler.users_file_lock:
                with open(FilePathsManagement.USERS_FILE_PATH.value, 'r') as file:
                    users = load(file)
        except FileNotFoundError:
            users = {}
        return users
    
    def __save_user(self, email, token):
        try:
            with ClientHandler.users_file_lock:
                with open(FilePathsManagement.USERS_FILE_PATH.value, 'r+') as file:
                    users:dict = load(file)
                    if email in users:
                        raise ValueError('User already exists!')
                    else:
                        file.seek(0)
                        users[email] = token
                        dump(users, file, indent=4)
            return True
        except FileNotFoundError:
            print(f'[SERVER] Users file not found')
            return False
        except ValueError:
            print(f'[SERVER] User email already exists.')
            return False


    def create_user(self, email:str):
        token = self.__create_token(email)
        created_status = self.__save_user(email, token)
        if created_status:
            return (ConstantsManagement.OK.value, token, ConstantsManagement.TOKEN_TYPE.value)
        else:
            return (ConstantsManagement.OPERATION_FAILED.value, None, ConstantsManagement.NO_DATA_TYPE.value)
        

    def get_token(self, email:str):
        users:dict = self.__load_users()
        token = users.get(email)
        if token:
            return (ConstantsManagement.OK.value, token, ConstantsManagement.TOKEN_TYPE.value)
        else:
            return (ConstantsManagement.NOT_FOUND.value, None, ConstantsManagement.NO_DATA_TYPE.value)
    
    def auth_token(self, token = None):
        users:dict = self.__load_users()
        if token and (token in users.values()):
            return True
        else:
            return False

    def find_routes(self, server_data: ServerData, match:str, destination:str):
            found_routes = server_data.search_route(match, destination)
            if (found_routes is None) or (not found_routes[0]):
                return (ConstantsManagement.NOT_FOUND.value, None, ConstantsManagement.NO_DATA_TYPE.value)
            else:
                return (ConstantsManagement.OK.value, found_routes, ConstantsManagement.ROUTE_TYPE.value)

    def buy_routes(self, server_data:ServerData, token, routes:list):
        routes_keys = []
        #lock
        for item in routes: #verificando validade dos voos 
            try:
                flight_key = (server_data.matches_and_destinations.index(item[0]), server_data.matches_and_destinations.index(item[1]))
                if not server_data.get_flight_sit(flight_key):
                    return (ConstantsManagement.OPERATION_FAILED.value, None, ConstantsManagement.NO_DATA_TYPE.value)
                routes_keys.append(flight_key)
            except ValueError:
                return (ConstantsManagement.OPERATION_FAILED.value, None, ConstantsManagement.NO_DATA_TYPE.value)
            
            for item in routes_keys:
                server_data.dec_flight_sits(item)
            
            try:
                with open(FilePathsManagement.ROUTES_DATA_FILE_PATH.value, 'w') as file:
                    dump(server_data.parse_flights_to_str(), file)
            except FileNotFoundError:
                print("[SERVER] Could not update the graph file! File doesn't exist")
        

        ticket = Ticket(self.__get_email(token), routes)
        with ClientHandler.tickets_file_lock:
            ticket.save()
        
        return (ConstantsManagement.OK.value, ticket.to_json(), ConstantsManagement.TICKET_TYPE.value)
            
    def __get_email(self, token):
        users:dict = self.__load_users()

        for user, client_token in users.items():
            if client_token == token:
                return user
        return None
        
    def get_tickets(self, token):
        try:
            with ClientHandler.tickets_file_lock:
                with open(FilePathsManagement.TICKETS_FILE_PATH.value, 'r') as file:
                    all_tickets:dict = load(file)   
            email = self.__get_email(token)
            users_tickets = all_tickets.get(email)
            return (ConstantsManagement.OK.value, users_tickets, ConstantsManagement.TICKET_TYPE.value)
        except FileNotFoundError:
            return (ConstantsManagement.NOT_FOUND.value, None, ConstantsManagement.NO_DATA_TYPE.value)


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
    
    def send_pkt(self, return_values:tuple): #(status, data, data_type)
        pkt = Response(return_values[0], return_values[1], return_values[2])
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
