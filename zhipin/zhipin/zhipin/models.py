class ProxyModel:
    def __init__(self, ip):
        self.ip = "http://" + ip

    @property
    def get_ip(self):
        return self.ip
