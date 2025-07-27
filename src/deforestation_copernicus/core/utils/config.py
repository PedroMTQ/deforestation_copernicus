from sentinelhub import SHConfig

import os

COPPERNICUS_CLIENT_ID = os.getenv('COPPERNICUS_CLIENT_ID')
COPPERNICUS_CLIENT_SECRET = os.getenv('COPPERNICUS_CLIENT_SECRET')

# TODO make it a singleton
class CoppernicusConfig():
    def __init__(self):
        self.config = SHConfig()
        self.config.sh_client_id = COPPERNICUS_CLIENT_ID
        self.config.sh_client_secret = COPPERNICUS_CLIENT_SECRET
        self.config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        self.config.sh_base_url = "https://sh.dataspace.copernicus.eu"
