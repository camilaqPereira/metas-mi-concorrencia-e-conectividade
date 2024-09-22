class InvalidTokenException(Exception):
    def __init__(self, *args: object, msg:str = ''):
        super().__init__(*args)
        self.msg = msg
