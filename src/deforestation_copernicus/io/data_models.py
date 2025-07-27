from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime

from geoalchemy2 import Geometry


Base = declarative_base()


class CopernicusBoundingBox(Base):
    __tablename__ = 'copernicus_bounding_box'
    id = Column(Integer, primary_key=True)
    resolution = Column(Integer)
    timestamp = Column(DateTime)
    geometry = Column(Geometry('POLYGON'))
    image_path = Column(String)