from deforestation_copernicus.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any
from dataclasses import dataclass
from typing import Iterable

from deforestation_copernicus.io.data_models import SentinelHubResult
import psycopg
from deforestation_copernicus.io.logger import logger
import os

CONNECTION_TIMEOUT = 10

class GeoAlchemyClient():
    def __init__(self):
        self.url = f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
        self.setup_database()
        self.engine = create_engine(self.url, echo=True, plugins=["geoalchemy2"])
        self.session_class = sessionmaker(bind=self.engine)
        self.data_models = [SentinelHubResult]
        for data_model in self.data_models:
            try:
                data_model.__table__.create(self.engine)
            except Exception as _:
                pass

    def delete_data_models(self):
        for data_model in self.data_models:
            try:
                data_model.__table__.drop(self.engine)
            except Exception as _:
                pass

    def setup_database(self):
        postgres_connection = psycopg.connect(user=POSTGRES_USER,
                                              password=POSTGRES_PASSWORD,
                                              host=POSTGRES_HOST,
                                              port=POSTGRES_PORT,
                                              autocommit=True,
                                              connect_timeout=CONNECTION_TIMEOUT)
        cursor = postgres_connection.cursor()
        database_list_query = 'SELECT datname FROM pg_database'
        database_list_results = cursor.execute(database_list_query).fetchall()
        database_list = [ele[0] for ele in database_list_results]
        cursor.close()
        if POSTGRES_DB not in database_list:
            cursor = postgres_connection.cursor()
            cursor.execute(f'CREATE DATABASE "{POSTGRES_DB}"')
            postgres_connection.commit()
            cursor.close()
        postgres_connection.close()
        logger.info(f'Connected successfully to postgres DB:{POSTGRES_DB} at {POSTGRES_HOST}:{POSTGRES_PORT}')



    def add_data(self, data: Iterable[SentinelHubResult]):
        session = self.session_class()
        session.add_all(data)
        session.commit()

    def get(self):
        session = self.session_class()
        results = session.query(SentinelHubResult).order_by(SentinelHubResult.id)
        for i in results:
            print(i)

if __name__ == '__main__':
    client = GeoAlchemyClient()
    print(client)
    client.delete_data_models()