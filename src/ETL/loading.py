import ast
import json
import argparse
import os
from src.utils.logger_utils import *

class ClassExtractor(ast.NodeVisitor):
    """
    Classe per estrarre i nomi delle classi, metodi (incluso __init__) e il loro codice sorgente dal codice Python.

    Args:
        file_content (str): Il contenuto del file Python da analizzare.
    
    Attributes:
        classes (dict): Dizionario che memorizza informazioni sulle classi, con 'init' e 'methods'.
        file_content (str): Il contenuto del file passato.
        lines (list): Lista di linee del file, utile per l'estrazione del codice sorgente.
    """
    def __init__(self, file_content: str):
        self.classes = {}
        self.file_content = file_content
        self.lines = file_content.splitlines()
        logger.debug("ClassExtractor initialized.")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Visita la definizione della classe e ne estrae i metodi e il costruttore __init__.

        Args:
            node (ast.ClassDef): Nodo AST rappresentante una definizione di classe.
        """
        class_name = node.name
        class_info = {'init': '', 'methods': {}}
        logger.debug(f"Found class: {class_name}")
        
        for class_body_item in node.body:
            if isinstance(class_body_item, ast.FunctionDef):
                method_name = class_body_item.name
                method_code = self.get_function_code(class_body_item)
                logger.debug(f"Extracted method: {method_name} from class: {class_name}")
                
                if method_name == '__init__':
                    class_info['init'] = method_code
                else:
                    class_info['methods'][method_name] = method_code
        
        self.classes[class_name] = class_info
        logger.info(f"Class {class_name} processed with methods: {list(class_info['methods'].keys())}")

    def get_function_code(self, node: ast.FunctionDef) -> str:
        """
        Estrae il codice sorgente della funzione.

        Args:
            node (ast.FunctionDef): Nodo AST rappresentante una funzione o metodo.

        Returns:
            str: Il codice sorgente della funzione o metodo.
        """
        start_line = node.lineno - 1
        end_line = node.body[-1].lineno
        logger.debug(f"Extracting function code from lines {start_line + 1} to {end_line}")
        return "\n".join(self.lines[start_line:end_line])

class FunctionExtractor(ast.NodeVisitor):
    """
    Classe per estrarre i nomi delle funzioni e il loro codice sorgente completo dal codice Python.

    Args:
        file_content (str): Il contenuto del file Python da analizzare.
    
    Attributes:
        functions (dict): Dizionario che memorizza le funzioni e il loro codice.
        file_content (str): Il contenuto del file passato.
        lines (list): Lista di linee del file, utile per l'estrazione del codice sorgente.
    """
    def __init__(self, file_content: str):
        self.functions = {}
        self.file_content = file_content
        self.lines = file_content.splitlines()
        logger.debug("FunctionExtractor initialized.")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Visita la definizione della funzione e ne estrae il nome e il codice sorgente.

        Args:
            node (ast.FunctionDef): Nodo AST rappresentante una funzione.
        """
        function_name = node.name
        function_code = self.get_function_code(node)
        self.functions[function_name] = function_code
        logger.info(f"Extracted function: {function_name}")

    def get_function_code(self, node: ast.FunctionDef) -> str:
        """
        Estrae il codice sorgente della funzione.

        Args:
            node (ast.FunctionDef): Nodo AST rappresentante una funzione.

        Returns:
            str: Il codice sorgente della funzione.
        """
        start_line = node.lineno - 1
        end_line = node.body[-1].lineno
        logger.debug(f"Extracting function code from lines {start_line + 1} to {end_line}")
        return "\n".join(self.lines[start_line:end_line])

def extract_lib_func_class_global(file_content: str) -> dict:
    """
    Preprocessa il contenuto di un file Python per estrarre librerie, funzioni, classi (con __init__ e metodi) e codice globale.

    Args:
        file_content (str): Il contenuto di un file Python come stringa.

    Returns:
        dict: Un dizionario contenente le librerie importate, le funzioni, le classi e il codice globale.
    """
    result = {
        'library': '',
        'functions': {},
        'classes': {},
        'global': ''
    }
    
    lines = file_content.splitlines()
    imported_libraries = []
    global_code = []
    
    logger.debug("Starting to extract libraries and global code.")
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('import') or stripped_line.startswith('from'):
            imported_libraries.append(stripped_line)
        else:
            global_code.append(stripped_line)
    
    result['library'] = '\n'.join(imported_libraries)
    logger.debug(f"Extracted libraries: {result['library']}")
    
    try:
        tree = ast.parse(file_content)
        logger.debug("AST parsing successful.")
        
        function_extractor = FunctionExtractor(file_content)
        function_extractor.visit(tree)
        result['functions'] = function_extractor.functions
        
        class_extractor = ClassExtractor(file_content)
        class_extractor.visit(tree)
        result['classes'] = class_extractor.classes

    except Exception as e:
        logger.error(f"Error parsing Python code: {e}")
    
    global_code_str = '\n'.join(line for line in global_code if not line.startswith(('def', 'class')))
    result['global'] = global_code_str
    logger.debug("Global code extracted.")
    
    return result

def extract_entity_for_all_repo(py_files_content: dict) -> dict:
    """
    Preprocessa tutti i file Python per estrarre librerie, funzioni (con codice), classi (con init e metodi) e codice globale.

    Args:
        py_files_content (dict): Dizionario con i nomi dei file come chiavi e il contenuto dei file Python come valori.

    Returns:
        dict: Un dizionario con le informazioni preprocessate per ciascun file.
    """
    processed_data = {}
    logger.info("Starting to process all Python files.")

    for file_name, content in py_files_content.items():
        logger.info(f"Processing file: {file_name}")
        processed_data[file_name] = extract_lib_func_class_global(content)
    
    logger.info("All files processed.")
    return processed_data

def extract_subfolders(path: str, num_folders: int) -> str:
    """
    Estrae i primi `num_folders` sottocartelle dal percorso specificato.

    Parameters:
    -----------
    path : str
        Il percorso completo del file o della directory, che può contenere separatori misti.
    num_folders : int
        Il numero di sottocartelle da estrarre dal percorso iniziale.

    Returns:
    --------
    str
        La parte del percorso che contiene solo le prime `num_folders` sottocartelle.

    Example:
    --------
    >>> extract_subfolders('data/repositories\\Financial-Update\\main.py', 3)
    'data/repositories/Financial-Update'
    """
    # Normalizza il percorso per gestire correttamente i separatori di directory
    normalized_path = os.path.normpath(path)
    parts = normalized_path.split(os.sep)

    logger.debug(f"Normalized path: {normalized_path}, Extracted parts: {parts[:num_folders]}")
    
    # Estrai le prime `num_folders` sottocartelle
    extracted_folders = os.sep.join(parts[:num_folders])
    
    logger.info(f"Extracted subfolders: {extracted_folders} from path: {path}")
    
    return extracted_folders

def build_set_of_repositories(processed_files: dict, num_folders: int) -> set:
    """
    Crea un set di percorsi delle sottocartelle di terzo livello a partire dalle chiavi di processed_files.

    Parameters:
    -----------
    processed_files : dict
        Un dizionario contenente i percorsi completi come chiavi.
    num_folders : int
        Numero di sottocartelle da estrarre.

    Returns:
    --------
    set
        Un set contenente le sottocartelle estratte.
    """
    set_repository = set()
    
    for key in processed_files.keys():
        repository = extract_subfolders(key, num_folders)
        set_repository.add(repository)
        logger.debug(f"Added repository: {repository}")
    
    logger.info(f"Final repository set: {set_repository}")
    
    return set_repository

def merge_python_files_by_repository(processed_files: dict, set_repository: set) -> dict:
    """
    Unisce i contenuti dei file Python per repository in base ai percorsi delle sottocartelle estratti.

    Parameters:
    -----------
    processed_files : dict
        Un dizionario con i percorsi completi come chiavi e le relative informazioni sul file come valori.
    set_repository : set
        Un set contenente le sottocartelle estratte.

    Returns:
    --------
    dict
        Un dizionario contenente i file uniti per ciascun repository.
    """
    merged_python_files = {}

    for element_set in set_repository:
        logger.info(f"Processing repository: {element_set}")
        
        merged_python_files[element_set] = {
            'library': '',
            'functions': {},
            'classes': {},
            'global': ''
        }

        for key in processed_files.keys():
            if element_set in key:
                logger.debug(f"Merging data for repository: {element_set} from file: {key}")
                
                merged_python_files[element_set]['library'] += '\n' + processed_files[key]['library']
                merged_python_files[element_set]['functions'] = {**merged_python_files[element_set]['functions'], **processed_files[key]['functions']}
                merged_python_files[element_set]['classes'] = {**merged_python_files[element_set]['classes'], **processed_files[key]['classes']}
                merged_python_files[element_set]['global'] += '\n' + processed_files[key]['global']
    
    logger.info("Merging completed for all repositories.")
    
    return merged_python_files