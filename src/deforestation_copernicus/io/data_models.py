from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime

from geoalchemy2 import Geometry

Base = declarative_base()


class SentinelHubResult(Base):
    __tablename__ = 'sentinel_hub_result'
    id = Column(Integer, primary_key=True)
    srid = Column(String)
    resolution = Column(Integer)
    timestamp_start = Column(DateTime)
    timestamp_end = Column(DateTime)
    # srid 4326 since we use WGS84 for querying sentinelhub
    geometry = Column(Geometry('POLYGON',  srid=4326))
    image_type = Column(String)
    image_path = Column(String)

