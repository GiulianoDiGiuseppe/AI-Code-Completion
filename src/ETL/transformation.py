import ast
import json
import argparse
import os
from src.utils.logger_utils import *

class ClassExtractor(ast.NodeVisitor):
    """
    Class to extract class names, methods (including __init__), and their source code from Python code.

    Args:
        file_content (str): The content of the Python file to analyze.
    
    Attributes:
        classes (dict): Dictionary that stores information about classes, with 'init' and 'methods'.
        file_content (str): The content of the provided file.
        lines (list): List of lines from the file, useful for extracting source code.
    """
    def __init__(self, file_content: str):
        self.classes = {}
        self.file_content = file_content
        self.lines = file_content.splitlines()
        logger.debug("ClassExtractor initialized.")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Visits the class definition and extracts its methods and the __init__ constructor.

        Args:
            node (ast.ClassDef): AST node representing a class definition.
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
        Extracts the source code of the function.

        Args:
            node (ast.FunctionDef): AST node representing a function or method.

        Returns:
            str: The source code of the function or method.
        """
        start_line = node.lineno - 1
        end_line = node.body[-1].lineno
        logger.debug(f"Extracting function code from lines {start_line + 1} to {end_line}")
        return "\n".join(self.lines[start_line:end_line])

class FunctionExtractor(ast.NodeVisitor):
    """
    Class to extract function names and their complete source code from Python code.

    Args:
        file_content (str): The content of the Python file to analyze.
    
    Attributes:
        functions (dict): Dictionary that stores functions and their code.
        file_content (str): The content of the provided file.
        lines (list): List of lines from the file, useful for extracting source code.
    """
    def __init__(self, file_content: str):
        self.functions = {}
        self.file_content = file_content
        self.lines = file_content.splitlines()
        logger.debug("FunctionExtractor initialized.")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Visits the function definition and extracts its name and source code.

        Args:
            node (ast.FunctionDef): AST node representing a function.
        """
        function_name = node.name
        function_code = self.get_function_code(node)
        self.functions[function_name] = function_code
        logger.info(f"Extracted function: {function_name}")

    def get_function_code(self, node: ast.FunctionDef) -> str:
        """
        Extracts the source code of the function.

        Args:
            node (ast.FunctionDef): AST node representing a function.

        Returns:
            str: The source code of the function.
        """
        start_line = node.lineno - 1
        end_line = node.body[-1].lineno
        logger.debug(f"Extracting function code from lines {start_line + 1} to {end_line}")
        return "\n".join(self.lines[start_line:end_line])

def extract_lib_func_class_global(file_content: str) -> dict:
    """
    Preprocesses the content of a Python file to extract libraries, functions, classes (with __init__ and methods), and global code.

    Args:
        file_content (str): The content of a Python file as a string.

    Returns:
        dict: A dictionary containing the imported libraries, functions, classes, and global code.
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
    Preprocesses all Python files to extract libraries, functions (with code), classes (with init and methods), and global code.

    Args:
        py_files_content (dict): Dictionary with file names as keys and the content of the Python files as values.

    Returns:
        dict: A dictionary with preprocessed information for each file.
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
    Extracts the first `num_folders` subfolders from the specified path.

    Parameters:
    -----------
    path : str
        The complete path of the file or directory, which may contain mixed separators.
    num_folders : int
        The number of subfolders to extract from the initial path.

    Returns:
    --------
    str
        The part of the path that contains only the first `num_folders` subfolders.

    Example:
    --------
    >>> extract_subfolders('data/repositories\\Financial-Update\\main.py', 3)
    'data/repositories/Financial-Update'
    """
    # Normalize the path to correctly handle directory separators
    normalized_path = os.path.normpath(path)
    parts = normalized_path.split(os.sep)

    logger.debug(f"Normalized path: {normalized_path}, Extracted parts: {parts[:num_folders]}")
    
    # Extract the first `num_folders` subfolders
    extracted_folders = os.sep.join(parts[:num_folders])
    
    logger.info(f"Extracted subfolders: {extracted_folders} from path: {path}")
    
    return extracted_folders

def build_set_of_repositories(processed_files: dict, num_folders: int) -> set:
    """
    Creates a set of third-level subfolder paths from the keys of processed_files.

    Parameters:
    -----------
    processed_files : dict
        A dictionary containing the complete paths as keys.
    num_folders : int
        Number of subfolders to extract.

    Returns:
    --------
    set
        A set containing the extracted subfolders.
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
    Merges the contents of Python files by repository based on the extracted subfolder paths.

    Parameters:
    -----------
    processed_files : dict
        A dictionary with complete paths as keys and their corresponding file information as values.
    set_repository : set
        A set containing the extracted subfolders.

    Returns:
    --------
    dict
        A dictionary containing merged files for each repository.
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
