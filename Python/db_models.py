from sqlalchemy import Text, Boolean, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


# Define the base class for all models
class Base(DeclarativeBase):
    pass

class Query(Base):
    __tablename__ = "query"

    query_id: Mapped[str] = mapped_column(Text, primary_key=True)
    query_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    query_type: Mapped[str] = mapped_column(Text) # e.g., "hourly" or "daily"

    def __repr__(self):
        return f"query(query_id={self.query_id!r}, query_time={self.query_time!r}, query_type={self.query_type!r})"

class ForecastTime(Base):
    __tablename__ = "forecast_time"

    # NOTE: We don't need an __init__ method here because SQLAlchemy will automatically create one since we used the mapping process
    forecast_time_id: Mapped[str] = mapped_column(Text, primary_key=True)
    query_id: Mapped[str] = mapped_column(ForeignKey("query.query_id"))
    query: Mapped["Query"] = relationship()
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    is_daytime: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"ForecastTime(forecast_time_id={self.forecast_time_id!r}, query_id{self.query_id!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, is_daytime={self.is_daytime!r})"

class Dewpoint(Base):
    """Note: Hourly forecast only!"""
    __tablename__ = "dewpoint"

    # Define mapped columns
    dewpoint_id: Mapped[str] = mapped_column(Text, primary_key=True)
    query_id: Mapped[str] = mapped_column(ForeignKey("query.query_id"))
    query: Mapped["Query"] = relationship()
    dewpoint_value: Mapped[float] = mapped_column(Numeric(10,2))
    dewpoint_units: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Dewpoint(dewpoint_id={self.dewpoint_id!r}, query_id{self.query_id!r}, dewpoint_value={self.dewpoint_value!r}, dewpoint_units={self.dewpoint_units!r})"

class Humidity(Base):
    """Note: Hourly forecast only!"""
    __tablename__ = "humidity"

    # Define mapped columns
    humidity_id: Mapped[str] = mapped_column(Text, primary_key=True)
    query_id: Mapped[str] = mapped_column(ForeignKey("query.query_id"))
    query: Mapped["Query"] = relationship()
    humidity_value: Mapped[float] = mapped_column(Numeric(10,2))
    humidity_units: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Humidity(humidity_id={self.humidity_id!r}, query_id{self.query_id!r}, humidity_value={self.humidity_value!r}, humidity_units={self.humidity_units!r})"

class Location(Base):
    __tablename__ = "location"

    # Define mapped columns
    location_id: Mapped[str] = mapped_column(Text, primary_key=True)
    query_id: Mapped[str] = mapped_column(ForeignKey("query.query_id"))
    query: Mapped["Query"] = relationship()
    geometry_type: Mapped[str] = mapped_column(Text)
    coordinates: Mapped[str] = mapped_column(Text)  # This is a string representation of coordinates
    elevation_value: Mapped[float] = mapped_column(Numeric(10,4))
    elevation_units: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Location(location_id={self.location_id!r}, query_id{self.query_id!r}, geometry_type={self.geometry_type!r}, coordinates={self.coordinates!r}, elevation_value={self.elevation_value!r}, elevation_units={self.elevation_units!r})"

class Precipitation(Base):
    __tablename__ = "precipitation"

    # Define mapped columns
    precipitation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    query_id: Mapped[str] = mapped_column(ForeignKey("query.query_id"))
    query: Mapped["Query"] = relationship()
    probability_of_precip_value: Mapped[float] = mapped_column(Numeric(10,2)) 
    probability_of_precip_units: Mapped[str] = mapped_column(Text) 

    def __repr__(self) -> str:
        return f"Precipitation(precipitation_id={self.precipitation_id!r}, query_id{self.query_id!r}, probability_of_precip_value={self.probability_of_precip_value!r}, probability_of_precip_units={self.probability_of_precip_units!r})"

class Temperature(Base):
    __tablename__ = "temperature"

    # Define mapped columns
    temperature_id: Mapped[str] = mapped_column(Text, primary_key=True)
    query_id: Mapped[str] = mapped_column(ForeignKey("query.query_id"))
    query: Mapped["Query"] = relationship()
    temperature_value: Mapped[float] = mapped_column(Numeric(10, 2))
    temperature_units: Mapped[str] = mapped_column(Text)
    temperature_trend: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Temperature(temperature_id={self.temperature_id!r}, query_id{self.query_id!r}, temperature_value={self.temperature_value!r}, temperature_units={self.temperature_units!r}, temperature_trend={self.temperature_trend!r})"


class Wind(Base):
    __tablename__ = "wind"

    # Define mapped columns
    wind_id: Mapped[str] = mapped_column(Text, primary_key=True)
    query_id: Mapped[str] = mapped_column(ForeignKey("query.query_id"))
    query: Mapped["Query"] = relationship()
    wind_speed: Mapped[float] = mapped_column(Numeric(10,2))
    wind_units: Mapped[str] = mapped_column(Text)
    wind_direction: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Wind(wind_id={self.wind_id!r}, query_id{self.query_id!r}, wind_speed={self.wind_speed!r}, wind_units={self.wind_units!r}, wind_direction={self.wind_direction!r})"
    




