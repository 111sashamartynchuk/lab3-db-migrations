import enum
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Weather(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    location_name = Column(String)
    temperature_celsius = Column(Float)
    condition_text = Column(String)
    last_updated = Column(Date)
    go_outside = Column(Boolean)

    celestial_info = relationship("CelestialBody", back_populates="weather", uselist=False, cascade="all, delete-orphan")


class CelestialBody(Base):
    __tablename__ = 'celestial_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey('weather_data.id'), nullable=False, unique=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)

    weather = relationship("Weather", back_populates="celestial_info")