
import module

class ApacheModule(Module):
    def __init__(self, config):

        self.config = config

class ApacheAccessModule(ApacheModule):
    def __init__(self, config):
        self.config = config

class ApacheErrorModule(ApacheModule):
    def __init__(self, config):
        self.config = config
   