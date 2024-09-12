class Route:

    def __init__(self, match = '', destination = '', sits = 0, id = None):
        self.match = match
        self.destination = destination
        self.sits = sits
        self.id = id

    def get_route(self):
        return (self.id, self.match, self.destination)
    
    def get_sits(self):
        return self.sits
    
    def set_sits(self, value):
        self.sits = value

    def dec_sits(self):
        self.sits -= 1

    def inc_sits(self):
        self.sits += 1
    
    def to_string(self):
        return {'match': self.match, 'destination': self.destination, 'sits': self.sits, 'id': self.id}
    
    def from_string(self, data):
        self.match = data['match']
        self.destination = data['destination']
        self.sits = data['sits']
        self.id = data['id']

