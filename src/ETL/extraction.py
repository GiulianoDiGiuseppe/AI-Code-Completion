import os
import subprocess
from src.utils.logger_utils import *
from typing import Dict, List, Callable

# Configura il logger

def clone_repositories(repos: List[str], target_folder: str) -> None:
    """
    Clona i repository nella cartella di destinazione.

    Args:
        repos (List[str]): Lista di URL dei repository da clonare.
        target_folder (str): La cartella in cui i repository verranno clonati.
    """
    # Salva la directory corrente
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
        # Ritorna alla directory originale
        os.chdir(current_dir)
        logger.debug(f"Returned to original directory: {current_dir}")

def get_python_files_content(repo_folder: str) -> Dict[str, str]:
    """
    Restituisce un dizionario con i file Python (.py) e il loro contenuto.

    Args:
        repo_folder (str): La cartella radice del repository.

    Returns:
        Dict[str, str]: Un dizionario con i percorsi dei file come chiavi e il contenuto come valori.
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
    Processa i repository git specificati in config_repo, estraendo e aggiornando i contenuti dei file Python da ciascun repository.

    Args:
        config (Dict[str, List[str]]): Dizionario di configurazione contenente la chiave "dataset_git", che è una lista di URL dei repository git.
        target_folder (str): La cartella di destinazione in cui sono presenti i repository locali.
        all_python_files (Dict[str, str]): Dizionario che contiene i contenuti di tutti i file Python processati.

    Returns:
        None
    """
    for repo in config_repo:
        # Estrae il nome del repository
        repo_name = repo.split('/')[-1].replace('.git', '')
        repo_folder = os.path.join(target_folder, repo_name)
        
        # Verifica se la cartella del repository esiste
        if os.path.exists(repo_folder):
            logger.info(f"Processing Python files in repository: {repo_name}")
            # Ottiene i contenuti dei file Python dal repository
            python_files_content = get_python_files_content(repo_folder)
            # Aggiorna il dizionario con i nuovi contenuti
            all_python_files.update(python_files_content)
        else:
            logger.warning(f"Repository folder {repo_folder} not found, skipping...")
        
        logger.info(f"Repository {repo_name} processed.")

    return all_python_files
