from sqlalchemy import create_engine
from pyaml_env import parse_config
from helper_functions import setup_env, setup_logs, connect_to_database
from db_models import Base
from time import sleep

# Setup environment if the file exists
setup_env("setup_env.yml")

# Setup logging
log = setup_logs("db_queries")

# Read in configs.yml file
config_path = "configs/db_configs.yml"
configs = parse_config(config_path)
log.debug(f"Configs read from file: {config_path}")

# Setup DB connection and schema to use
engine = connect_to_database(configs)

log.info(f"Using schema: {configs["db_schema"]}")
log.info("DB connection setup")

try:
    if configs["drop_all_tables"]:
        log.warning("drop all variable is enabled!")
        print("WARNING: drop all variable is enabled!")
        sleep(5)  # sleep for 5 seconds to avoid accidental data loss
        input = input("Are you sure you want to drop all tables? (y/n): ")
        if input == "y":
            log.critical("Dropping ALL tables!")
            Base.metadata.drop_all(engine)
        else:
            log.warning("Dropping all tables canceled.")
    # This will create all tables in the database if they don't already exist
    Base.metadata.create_all(engine)
    log.info("All database tables created")
except Exception as e:
    log.error(f"Error creating database tables: {e}")
    raise e
