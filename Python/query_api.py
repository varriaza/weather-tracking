from pyaml_env import parse_config
import requests
import json
from icecream import ic
from helper_functions import setup_env, setup_logs, connect_to_database, write_objects_to_database
from create_forecast_objects import *

# Setup environment if the file exists
setup_env("setup_env.yml")

# Setup logging
log = setup_logs("query_api")

# Read in configs.yml file
config_path = "configs/configs.yml"
configs = parse_config(config_path)

# validate forecast_period variable is defined and within expected parameters
if configs["forecast_period"] not in ["daily", "hourly"]:
    log.error(f"forecast_period variable is not equal to 'daily' or 'hourly': {configs['forecast_period']}")
    raise ValueError("Forecast_period variable is not defined or within expected parameters.")
else:
    log.info(ic.format(configs["forecast_period"]))

log.debug(ic.format(configs["lat"]))
log.debug(ic.format(configs["long"]))

# Error out if lat and long are not defined
if configs["lat"] == "N/A" or configs["long"] == "N/A":
    raise ValueError("Latitude and Longitude must be defined in configs.yml or environment variables")

log.debug(ic.format(configs["grid_x"]))
log.debug(ic.format(configs["grid_y"]))

# If env_variables, grid_x and grid_y are not defined, run points API query using lat and long
if configs["grid_x"] == "N/A" or configs["grid_y"] == "N/A":
    # Fill out the API URL
    points_url = configs["points_API_url"].format(lat=configs["lat"], long=configs["long"])
    log.debug(ic.format(points_url))

    # Make the API request and print out the response data
    response = requests.get(points_url)
    if response.status_code == 200:
        data = json.loads(response.text)
        grid_x = data["properties"]["gridX"]
        grid_y = data["properties"]["gridY"]
    else:
        log.error(f"Failed to get grid coordinates. Status code: {response.status_code}")
        log.error(f"response.text: {response.text}")
        raise ValueError("Failed to get points data.")
else:
    log.info("grid_x and grid_y exist in config, skipping points query")
    # Else use the defined values for env_variables, grid_x and grid_y to query the gridpoints API
    grid_x = configs["grid_x"]
    grid_y = configs["grid_y"]
    
# Make sure we log what grid coordinates are being used
log.info(f"Grid X set to: {grid_x}, Grid Y set to: {grid_y}")

# Fill out the gridpoints API URL based on the hourly or daily forecast type
if configs["forecast_period"] == "hourly":
    gridpoints_url = configs["hourly_gridpoints_API_url"].format(office=configs["gridpoints_office"], grid_x=grid_x, grid_y=grid_y)
elif configs["forecast_period"] == "daily":
    gridpoints_url = configs["daily_gridpoints_API_url"].format(office=configs["gridpoints_office"], grid_x=grid_x, grid_y=grid_y)
else:
    log.error(f"Invalid forecast type specified in config: {configs["forecast_period"]}")
    raise ValueError("Invalid forecast type specified in config.")
log.debug(ic.format(gridpoints_url))

# Make the API request and print out the response data
response = requests.get(gridpoints_url)
if response.status_code == 200:
    # Get the data as a dictionary
    data = json.loads(response.text)

    # Create list to hold all of the objects that will be added to the database
    all_objects = []

    # Create query object
    query = create_query(
        json_data=data,
        query_type=configs["forecast_period"],
    )
    log.info(f"created query object")

    # loop over all periods in the response data
    num_period = 0
    
    # TODO: Remove this once the API 500 error is fixed
    log.info(f"period type: {type(data["properties"]["periods"][0][0])}")

    # Note: "periods" is a list of tuples
    for _ in data["properties"]["periods"][0]:
        log.debug(f"num_period: {num_period}")
        all_objects.append(create_forecast_time(data, num_period, query.query_id))
        log.debug("created forecast_time object")

        all_objects.append(create_location(data, num_period, query.query_id))
        log.debug("created location object")

        all_objects.append(create_precipitation(data, num_period, query.query_id))
        log.debug("created precipitation object")

        all_objects.append(create_temperature(data, num_period, query.query_id))
        log.debug("created temperature object")

        all_objects.append(create_wind(data, num_period, query.query_id))
        log.debug("created wind object")

        # If we are in the hourly forecast add Dewpoint and Humidity to the database
        if configs["forecast_period"] == "hourly":
            all_objects.append(create_dewpoint(data, num_period, query.query_id))
            log.debug("created dewpoint object")

            all_objects.append(create_humidity(data, num_period, query.query_id))
            log.debug("created humidity object")
        # Go to the next period
        num_period += 1

    # Session add and commit to save the new data
    engine = connect_to_database(configs)
    write_objects_to_database(engine, all_objects)

else:
    log.error(f"Failed to get weather data. Status code: {response.status_code}")
    log.error(f"response.text: {response.text}")
    raise ValueError("Failed to get gridpoints data.")

log.info("Run completed successfully. :)")

