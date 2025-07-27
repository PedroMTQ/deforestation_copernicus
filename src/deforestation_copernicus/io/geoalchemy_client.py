from deforestation_copernicus.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any


class GeoAlchemyClient():
    db_name = 'gis'
    def __init__(self):
        self.url = f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{self.db_name}'
        self.engine = create_engine(self.url, echo=True, plugins=["geoalchemy2"])
        self.session = sessionmaker(bind=self.engine)

    def add_data(self, list_data_dict: list[dict], data_dict_type: Any):
        data_instances = []
        for data_dict in list_data_dict:
            data_instances.append(data_dict_type(**data_dict))
        self.session.add_all(data_instances)
        self.session.commit()

if __name__ == '__main__':
    client = GeoAlchemyClient()
    print(client)