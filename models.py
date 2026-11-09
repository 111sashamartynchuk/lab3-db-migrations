import enum
from sqlalchemy import Column, Integer, String, Float, Enum, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class WindDirectionEnum(enum.Enum):
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"


class Weather(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)  # String
    location_name = Column(String)  # String
    temperature_celsius = Column(Float)  # Float
    wind_degree = Column(Integer, default=180)  # Integer
    wind_direction = Column(Enum(WindDirectionEnum), default=WindDirectionEnum.N)  # Enum
    condition_text = Column(String)
    last_updated = Column(Date)  # Date

    celestial_info = relationship("CelestialBody", back_populates="weather", uselist=False,
                                  cascade="all, delete-orphan")


class CelestialBody(Base):
    __tablename__ = 'celestial_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey('weather_data.id'), nullable=False, unique=True)

    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)
    sunrise = Column(Time)  # Time

    # Колонка go_outside ТУТ (згідно із Завданням 3)
    go_outside = Column(Boolean)

    weather = relationship("Weather", back_populates="celestial_info")