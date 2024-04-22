

class MissingFieldException(Exception):
    def __init__(self, field):
        self.field = field

    def __str__(self):
        return f"Missing field: {self.field}"
    
class MissingBlockException(Exception):
    def __init__(self, block):
        self.block = block

    def __str__(self):
        return f"Missing block: {self.block}"