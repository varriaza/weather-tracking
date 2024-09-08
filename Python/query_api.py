from pyaml_env import parse_config
import requests
import json
from icecream import ic
from helper_functions import setup_env, setup_logs

# Setup environment if the file exists
setup_env("setup_env.yml")

# setup logging
log = setup_logs()

# Read in configs.yml file
# config_path = "Python/configs/configs.yml"
config_path = "configs/configs.yml"
configs = parse_config(config_path)

log.debug(ic.format(configs["lat"]))
log.debug(ic.format(configs["long"]))

# error out if lat and long are not defined
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
        log.debug(f"Grid X set to: {grid_x}, Grid Y set to: {grid_y}")
    else:
        log.error(f"Failed to get grid coordinates. Status code: {response.status_code}")
        log.error(f"response.text: {response.text}")
        raise ValueError("Failed to get points data.")
else:
    # else use the defined values for env_variables, grid_x and grid_y to query the gridpoints API
    grid_x = configs["grid_x"]
    grid_y = configs["grid_y"]

# Fill out the gridpoints API URL
gridpoints_url = configs["gridpoints_API_url"].format(office=configs["gridpoints_office"], grid_x=grid_x, grid_y=grid_y)
log.debug(ic.format(gridpoints_url))

# Make the API request and print out the response data
response = requests.get(gridpoints_url)
if response.status_code == 200:
    data = json.loads(response.text)
    # log.debug(ic.format(data))
    # TODO: Extract data and save to DB
else:
    log.error(f"Failed to get weather data. Status code: {response.status_code}")
    log.error(f"response.text: {response.text}")
    raise ValueError("Failed to get gridpoints data.")

log.info("Run completed successfully. :)")

