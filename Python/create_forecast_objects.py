from typing import Any, Dict
from db_models import Base, Query, ForecastTime, Dewpoint, Humidity, Location, Precipitation, Temperature, Wind
from uuid import uuid4

def create_query(json_data: Dict[str, Any], query_type: str) -> Query:
    if query_type not in ["hourly", "daily"]:
        raise ValueError(f"Query type must be either 'hourly' or 'daily'. Found {query_type}")
    
    query = Query(
        query_id=uuid4(),
        query_time=json_data["properties"]["generatedAt"],
        query_type=query_type,
    )
    return query

def create_forecast_time(json_data: Dict[str, Any], num_period: int, query_id: uuid4) -> ForecastTime:
    forecast_time_object = ForecastTime(
        forecast_time_id=uuid4(),
        query_id=query_id,
        start_time=json_data["properties"]["periods"][num_period]["startTime"],
        end_time=json_data["properties"]["periods"][num_period]["endTime"],
        is_daytime=json_data["properties"]["periods"][num_period]["isDaytime"]
    )
    return forecast_time_object

def create_dewpoint(json_data: Dict[str, Any], num_period: int, query_id: uuid4) -> Dewpoint:
    """Note: Hourly forecast only!"""
    dewpoint_object = Dewpoint(
        dewpoint_id=uuid4(),
        query_id=query_id,
        dewpoint_value=json_data["properties"]["periods"][num_period]["dewpoint"]["value"],
        dewpoint_units=json_data["properties"]["periods"][num_period]["dewpoint"]["unitCode"]
    )
    return dewpoint_object


def create_humidity(json_data: Dict[str, Any], num_period: int, query_id: uuid4) -> Humidity:
    """Note: Hourly forecast only!"""
    humidity_object = Humidity(
        humidity_id=uuid4(),
        query_id=query_id,
        humidity_value=json_data["properties"]["periods"][num_period]["relativeHumidity"]["value"],
        humidity_units=json_data["properties"]["periods"][num_period]["relativeHumidity"]["unitCode"]
    )
    return humidity_object

def create_location(json_data: Dict[str, Any], query_id: uuid4) -> Location:
    # Format the coordinate data into something reasonable
    coordinates_string = ""
    coordinates_list = json_data["geometry"]["coordinates"][0]
    for pair in coordinates_list:
        coordinates_string += f"({round(pair[0], 4)}, {round(pair[1],4)})"

    location_object = Location(
        location_id=uuid4(),
        query_id=query_id,
        geometry_type=json_data["geometry"]["type"],
        coordinates=coordinates_string,
        elevation_value=json_data["properties"]["elevation"]["value"],
        elevation_unit=json_data["properties"]["elevation"]["unitCode"]
    )
    return location_object

def create_precipitation(json_data: Dict[str, Any], num_period: int, query_id: uuid4) -> Precipitation:
    precipitation_object = Precipitation(
        precipitation_id=uuid4(),
        query_id=query_id,
        probability_of_precip_value=json_data["properties"]["periods"][num_period]["probabilityOfPrecipitation"]["value"],
        probability_of_precip_units=json_data["properties"]["periods"][num_period]["probabilityOfPrecipitation"]["unitCode"]
    )
    return precipitation_object

def create_temperature(json_data: Dict[str, Any], num_period: int, query_id: uuid4) -> Temperature:
    temperature_object = Temperature(
        temperature_id=uuid4(),
        query_id=query_id,
        temperature_value=json_data["properties"]["periods"][num_period]["temperature"],
        temperature_unit=json_data["properties"]["periods"][num_period]["temperatureUnit"],
        temperature_trend=json_data["properties"]["periods"][num_period]["temperatureTrend"]
    )
    return temperature_object

def create_wind(json_data: Dict[str, Any], num_period: int, query_id: uuid4) -> Wind:
    # Split the wind data into two parts: the speed and the direction.
    # Example: '10 mph' is split into ['10', 'mph'].
    wind_data: str = json_data["properties"]["periods"][num_period]['windSpeed']
    wind_data_list = wind_data.split(" ")

    wind_object = Wind(
        wind_id=uuid4(),
        query_id=query_id,
        wind_speed=wind_data_list[0],
        wind_units=wind_data_list[1:], # Get all but the first element of List
        wind_direction=json_data["properties"]["periods"][num_period]['windDirection'],
    )
    return wind_object
