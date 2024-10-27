import os
import subprocess
from src.utils.logger_utils import *
from typing import Dict, List, Callable

# Set up the logger

def clone_repositories(repos: List[str], target_folder: str) -> None:
    """
    Clones the repositories into the target folder.

    Args:
        repos (List[str]): List of repository URLs to clone.
        target_folder (str): The folder where the repositories will be cloned.
    """
    # Save the current directory
    current_dir = os.getcwd()

    try:
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            logger.debug(f"Created target folder: {target_folder}")
        
        os.chdir(target_folder)
        logger.debug(f"Changed directory to: {target_folder}")
        
        for repo in repos:
            repo_name = repo.split('/')[-1].replace('.git', '')
            if not os.path.exists(repo_name):
                logger.info(f"Cloning {repo}...")
                subprocess.run(['git', 'clone', repo], check=True)
            else:
                logger.info(f"The repository {repo_name} already exists, skipping...")
    
    finally:
        # Return to the original directory
        os.chdir(current_dir)
        logger.debug(f"Returned to original directory: {current_dir}")

def get_python_files_content(repo_folder: str) -> Dict[str, str]:
    """
    Returns a dictionary with Python (.py) files and their content.

    Args:
        repo_folder (str): The root folder of the repository.

    Returns:
        Dict[str, str]: A dictionary with file paths as keys and content as values.
    """
    py_files_content = {}
    
    for root, dirs, files in os.walk(repo_folder):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        py_files_content[file_path] = file_content
                        logger.debug(f"Added file: {file_path}")
                except Exception as e:
                    logger.error(f"Error reading the file {file_path}: {e}")
    
    return py_files_content

def process_repositories(config_repo: List[str], target_folder: str,
                         all_python_files: Dict[str, str] = {}) -> None:
    """
    Processes the specified git repositories in config_repo, extracting and updating the content of Python files from each repository.

    Args:
        config_repo (List[str]): List of repository URLs to process.
        target_folder (str): The target folder where local repositories are located.
        all_python_files (Dict[str, str]): Dictionary containing the contents of all processed Python files.

    Returns:
        None
    """
    for repo in config_repo:
        # Extract the repository name
        repo_name = repo.split('/')[-1].replace('.git', '')
        repo_folder = os.path.join(target_folder, repo_name)
        
        # Check if the repository folder exists
        if os.path.exists(repo_folder):
            logger.info(f"Processing Python files in repository: {repo_name}")
            # Get the content of Python files from the repository
            python_files_content = get_python_files_content(repo_folder)
            # Update the dictionary with new contents
            all_python_files.update(python_files_content)
        else:
            logger.warning(f"Repository folder {repo_folder} not found, skipping...")
        
        logger.info(f"Repository {repo_name} processed.")

    return all_python_files
