from Client.controller import client


class RouteRequest:
    def __init__(self, match, destination, client_token):
        self.match = match
        self.destination = destination
        self.client_token = client_token


class BuyRequest:
    def __init__(self, client_token):
        self.client_token = ''
        self.route = []

class BoughtRequest:
    def __init__(self, client_token):
        self.client_token = client_token

class AccountCheck:
    def __init__(self, email):
        self.email = email

class AccountCreate:
    def __init__(self, email):
        self.email = email