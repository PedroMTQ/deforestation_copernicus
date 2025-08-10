import os

from sentinelhub import SHConfig

SH_CLIENT_ID = os.getenv('SH_CLIENT_ID')
SH_CLIENT_SECRET = os.getenv('SH_CLIENT_SECRET')

# TODO make it a singleton
class CoppernicusConfig():
    def __init__(self):
        self.config = SHConfig()
        self.config.sh_client_id = SH_CLIENT_ID
        self.config.sh_client_secret = SH_CLIENT_SECRET
        self.config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        self.config.sh_base_url = "https://sh.dataspace.copernicus.eu"


