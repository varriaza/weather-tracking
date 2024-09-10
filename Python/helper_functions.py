import logging
import os
import yaml
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from typing import Dict, Any
from create_forecast_objects import create_table_load_tracker

def setup_env(input_file: str):
    try:
        # Open the file and load it into a Python dictionary
        with open(f'configs/{input_file}', 'r') as file:
            data_dict = yaml.safe_load(file)

        for key, value in data_dict.items():
            os.environ[key] = value
    except FileNotFoundError:
        print("setup_env.yml file does not exist, moving on without it.")


def setup_logs(log_name: str) -> logging.Logger:
    # Create the directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define the log file path and name
    log_filename = os.path.join(log_dir, f'{log_name}.log')

    # Create a custom logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add the log file handler
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.info('------------------ New run starting ------------------')
    return logger


def connect_to_database(configs: Dict[str, str]) -> Engine:
    connection_string = configs["db_uri"].format(
    db_username=configs["db_username"],
    db_password=configs["db_password"],
    db_host=configs["db_host"],
    db_name=configs["db_name"]
)
    engine = create_engine(connection_string, connect_args={'options': '-csearch_path={}'.format(configs["db_schema"])})
    return engine

def write_objects_to_database(engine: Engine, object: Any) -> None:
    """Write an object to the database and track this change by updating the table load tracker.
    engine: The database engine to use.
    object: The object to write to the database. Should be from "create_forecast_objects".
    """
    # See if the object has a query_id
    try:
        query_id = object.query_id
    except AttributeError:
        query_id = None
    
    table_load_tracker_object = create_table_load_tracker(
        table_name=object.__tablename__,
        query_id=query_id,
    )

    with Session(engine) as session:
        session.add_all([object, table_load_tracker_object])
        session.commit()