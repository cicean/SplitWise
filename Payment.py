
class Payment:
    user = ""
    currency = ""
    paid_value = 0
    share_type = ""

    def __init__(self, username, currency, value, sharetype):
        self.user = username
        self.currency = currency
        self.paid_value = value
        self.share_type = sharetype