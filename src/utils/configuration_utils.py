import yaml
import os
from src.utils.logger_utils import *

def load_yaml(file_path: str):
    """
    Reads a YAML file and returns its content as a dictionary.
    
    :param file_path: Path to the YAML file.
    :return: Dictionary containing the YAML file content.
    """
    try:
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
            logger.info(f"YAML file '{file_path}' loaded successfully.")
        
        content['folder_save_dataset'] = os.path.join(*content['folder_save_dataset'])
        return content
    except FileNotFoundError:
        logger.error(f"YAML file not found: {file_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file '{file_path}': {e}")
        raise

config=load_yaml('config.yaml')