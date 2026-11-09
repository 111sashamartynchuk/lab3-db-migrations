import enum
from sqlalchemy import Column, Integer, String, Float, Enum, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class WindDirectionEnum(enum.Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"


class Weather(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)

    country = Column(String, nullable=False)
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(Enum(WindDirectionEnum))
    last_updated = Column(Date)

    # Зв'язок з новою таблицею категорій
    celestial_info = relationship("CelestialBody", back_populates="weather", uselist=False,
                                  cascade="all, delete-orphan")


class CelestialBody(Base):
    __tablename__ = 'celestial_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey('weather_data.id'), nullable=False, unique=True)

    sunrise = Column(Time)
    sunset = Column(Time)
    moonrise = Column(Time)
    moonset = Column(Time)
    moon_phase = Column(String)
    moon_illumination = Column(Integer)

    weather = relationship("Weather", back_populates="celestial_info")