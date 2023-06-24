class TableNotFound(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TableValueOverflow(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TableNameUniqueness(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message