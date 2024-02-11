class BrokerConnector:
    def __init__(self, user_id, password, broker_name):
        self.user_id = user_id
        self.password = password
        self.broker_name = broker_name

    def connect(self):
        raise NotImplementedError("The connect method must be implemented by the subclass.")

    def disconnect(self):
        raise NotImplementedError("The disconnect method must be implemented by the subclass.")

    def login(self):
        raise NotImplementedError("The login method must be implemented by the subclass.")

    def get_user_data(self):
        raise NotImplementedError("The get_user_data method must be implemented by the subclass.")

    def get_account_data(self):
        raise NotImplementedError("The get_account_data method must be implemented by the subclass.")
