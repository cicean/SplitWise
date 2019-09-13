class User:
    user = ""
    days = 0
    total_paid = 0
    total_spend = 0

    def __init__(self, username, value):
        self.user = username
        self.days = value
