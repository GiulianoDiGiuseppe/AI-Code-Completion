# Overview of the ETL Pipeline Script

This script orchestrates an ETL (Extract, Transform, Load) pipeline for processing Python code from specified Git repositories. It leverages functions from the `extraction`, `transformation`, and `loading` modules to manage the entire process.

## Key Components

### 1. **Imports**

The script imports various libraries and functions essential for ETL operations, including file handling, data manipulation, logging, and configuration management.

### 2. **Main Function**

The `main` function is the entry point for executing the ETL process. It handles the following tasks:

* **Load Configuration** : Reads settings from a YAML configuration file.
* **Extraction** :
  * Clones specified Git repositories.
  * Processes the repositories to retrieve Python file content.
* **Transformation** :
  * Extracts entities from the Python files.
  * Builds a set of repositories and merges Python file contents.
* **Loading** :
  * Prepares a dataset based on the processed information and saves it in an Excel format.

### 3. **Command-Line Argument Parsing**

The script supports command-line arguments to specify the path of the YAML configuration file, defaulting to `config.yaml` if not provided.

### 4. **Logging**

Throughout the script, logging is utilized to track the progress and status of operations.

### 5. **Data Saving**

The final dataset is saved in Excel format, with UTF-8 encoding for compatibility.

## YAML Configuration File

The YAML file (assumed to be named `config.yaml`) is expected to contain configurations similar to the following structure:

```yaml
# CREATION_DATASET
dataset_git : 
  - https://github.com/GiulianoDiGiuseppe/Financial-Update
  - https://github.com/GiulianoDiGiuseppe/Trenitalia-api-search
  - https://github.com/GiulianoDiGiuseppe/Dasboard-with-DB-from-Notion
folder_save_dataset : ['data' ,'repositories']
programming_language : 
  python :
    # triggers : ['await', 'assert', 'raise', 'del', 'lambda', 'yield', 'return','print','logger',
    #         'logging','while', 'for', 'if', 'elif', 'else', 'global', 'in', 'and', 'not', 
    #         'or', 'is', 'with', 'except', '.', '+', '-', '*', '/', '%', '**', '<<', ".",
    #         '>>', '&', '|', '^', '==', '!=', '<=', '>=', '+=', '-=', '=', '<', '>', 
    #         ';', ',', '[', '(', '{', '~']
    triggers : ['await', 'assert', 'raise', 'del', 'lambda', 'yield', 'return','print','logger',
            'logging','while', 'for', 'if', 'elif', 'else', 'global', 
            'or', 'is', 'with', 'except', '.', '+', '-', '*', '%', ".",
             '|', '^', '==', '!=', '<=', '>=', '+=', '-=', '=', '<', '>', 
            ';', ',', '[', '(', '{', '~']
    extensions : ['.py']
    comment : '#'
    comment_multiline : ['"""','"""']
    comment_singleline : ['#']
path_csv_dataset : 'data/dataset.csv'
path_xlsx_dataset : 'data/dataset.xlsx'
```

# extraction.py Overview

This script handles the cloning of Git repositories and retrieves the content of Python files within those repositories.

## Functions

1. **`clone_repositories(repos: List[str], target_folder: str) -> None`**
   Clones specified Git repositories into a designated target folder and skips existing repositories.
2. **`get_python_files_content(repo_folder: str) -> Dict[str, str]`**
   Retrieves the content of all Python files in a repository folder and logs any errors encountered.
3. **`process_repositories(config_repo: List[str], target_folder: str, all_python_files: Dict[str, str] = {}) -> None`**
   Processes specified repositories to extract Python file content, updating a provided dictionary.

---

# loading.py Overview

This script focuses on analyzing Python code to identify used functions, classes, and methods, formatting their definitions for further analysis.

## Functions

1. **`extract_used_functions(function_body: str, available_functions: list, current_function: str) -> list`**
   Extracts functions called within a specific function body, excluding the function itself.
2. **`extract_used_classes(function_body: str, available_classes: list) -> list`**
   Identifies classes referenced within the body of a function.
3. **`extract_class_methods_used(function_body: str, class_methods: dict) -> dict`**
   Extracts methods from classes that are called within a function body.
4. **`format_function_calls(functions: list, repository: dict) -> str`**
   Formats definitions of used functions into a concatenated string.
5. **`format_class_methods(class_name: str, class_info: dict) -> str`**
   Formats a class and its methods into a string representation.
6. **`creation_input_output(repository: dict) -> tuple`**
   Creates formatted representations of functions and classes used in a repository.
7. **`CodeProcessor` Class**
   Processes code by separating it into prefixes and suffixes based on specified triggers.
8. **`create_dataset(result: Dict[str, List[List[str]]], triggers: List[str], selector_lines: str = "random") -> List[Dict[str, str]]`**
   Creates a dataset from repository data, separating code based on triggers.

---

# transformation.py Overview

This script extracts information from Python files, including libraries, functions, classes, and global code, using the AST module.

## Classes

1. **`ClassExtractor`**
   Extracts class names, methods, and their source code from Python files.
2. **`FunctionExtractor`**
   Extracts function names and their complete source code from Python files.

## Functions

1. **`extract_lib_func_class_global(file_content: str) -> dict`**
   Extracts libraries, functions, classes, and global code from a Python file.
2. **`extract_entity_for_all_repo(py_files_content: dict) -> dict`**
   Processes all Python files to gather libraries, functions, and classes.
3. **`extract_subfolders(path: str, num_folders: int) -> str`**
   Extracts the specified number of subfolders from a given path.
4. **`build_set_of_repositories(processed_files: dict, num_folders: int) -> set`**
   Creates a set of subfolder paths from processed files.
5. **`merge_python_files_by_repository(processed_files: dict, set_repository: set) -> dict`**
   Merges contents of Python files by repository based on subfolder paths.
