import enum
from sqlalchemy import Column, Integer, String, Float, Enum, Date, Time
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Перелічуваний тип для напрямку вітру
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
    sunrise = Column(Time)

# Колонки категорії сходу-заходу небесних тіл
    sunrise = Column(Time)
    sunset = Column(Time)
    moonrise = Column(Time)
    moonset = Column(Time)
    moon_phase = Column(String)
    moon_illumination = Column(Integer)