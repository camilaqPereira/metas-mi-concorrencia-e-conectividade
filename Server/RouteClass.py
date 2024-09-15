class Route:

    def __init__(self, match = '', destination = '', sits = 0, id = None):
        self.match = match
        self.destination = destination
        self.sits = sits
        self.id = id

    def to_string(self):
        return {'match': self.match, 'destination': self.destination, 'sits': self.sits, 'id': self.id}
    
    def from_string(self, data):
        self.match = data['match']
        self.destination = data['destination']
        self.sits = data['sits']
        self.id = data['id']

