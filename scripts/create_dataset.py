import os
import pandas as pd
import argparse
import logging
import yaml

from src.ETL.extraction import clone_repositories, process_repositories
from src.ETL.loading import extract_entity_for_all_repo, build_set_of_repositories, merge_python_files_by_repository
from src.ETL.transformation import creation_input_output, create_dataset
from src.utils.configuration_utils import load_yaml
from src.utils.logger_utils import logger

def main(config_path):
    """
    Main function to execute the ETL pipeline for processing Git repositories.

    Args:
        config_path (str): Path to the configuration YAML file.
    """
    # Load configuration
    config = load_yaml(config_path)
    
    logger.info(f"Configuration loaded from {config_path} with the following settings: {config.keys()}")
    # EXTRACTION
    logger.info("Cloning repositories...")
    clone_repositories(config["dataset_git"], config['folder_save_dataset'])

    # TRANSFORMATION
    logger.info("Processing repositories...")
    all_python_files = process_repositories(config["dataset_git"], config['folder_save_dataset'])
    processed_files = extract_entity_for_all_repo(all_python_files)
    set_repository = build_set_of_repositories(processed_files, 3)
    merged_python_files = merge_python_files_by_repository(processed_files, set_repository)

    result = {}
    for repo in merged_python_files.keys():
        # Extract the repository name based on the operating system
        name_repo = os.path.basename(repo)
        result[name_repo] = creation_input_output(merged_python_files[repo])

    triggers = config['programming_language']['python']['triggers']
    # Process the repositories
    logger.info("Creating dataset...")
    dataset = create_dataset(result, triggers, selector_lines="random")

    df = pd.DataFrame(dataset)

    # Save the DataFrame as a CSV with UTF-8 encoding
    df.to_csv(config['path_csv_dataset'], index=False, encoding='utf-8')
    logger.info(f"Data has been saved to {config['path_csv_dataset']} with UTF-8 encoding.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Pipeline for Processing Git Repositories")
    parser.add_argument('--config', type=str, required=False,
                        help='Path to the configuration YAML file.',default='config.yaml')

    args = parser.parse_args()
    main(args.config)
