import logging
import os
import yaml

def setup_env(input_file: str):
    try:
        # Open the file and load it into a Python dictionary
        with open(f'configs/{input_file}', 'r') as file:
            data_dict = yaml.safe_load(file)

        for key, value in data_dict.items():
            os.environ[key] = value
    except FileNotFoundError:
        print("setup_env.yml file does not exist, moving on without it.")


def setup_logs() -> logging.Logger:
    # Create the directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define the log file path and name
    log_filename = os.path.join(log_dir, 'query_api.log')

    # Create a custom logger
    logger = logging.getLogger('query_api')
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