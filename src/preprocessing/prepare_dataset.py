import random
from typing import List, Dict

def extract_used_functions(function_body: str, available_functions: list, current_function: str) -> list:
    """
    Extracts the functions used in the body of a function, excluding the function itself.

    Args:
        function_body (str): The body of the current function.
        available_functions (list): The list of all available functions.
        current_function (str): The name of the current function.

    Returns:
        list: A list of the functions used in the body of the function.
    """
    return [func for func in available_functions if func in function_body and func != current_function]


def extract_used_classes(function_body: str, available_classes: list) -> list:
    """
    Extracts the classes used in the body of a function.

    Args:
        function_body (str): The body of the current function.
        available_classes (list): The list of all available classes.

    Returns:
        list: A list of the classes used in the body of the function.
    """
    return [cls for cls in available_classes if cls in function_body]


def extract_class_methods_used(function_body: str, class_methods: dict) -> dict:
    """
    Extracts the methods of a class that are used in the body of a function.

    Args:
        function_body (str): The body of the current function.
        class_methods (dict): A dictionary of the class methods.

    Returns:
        dict: A dictionary of the class methods used in the function.
    """
    used_methods = {method_name: method_body for method_name, method_body in class_methods.items() if method_name in function_body}
    return used_methods


def format_function_calls(functions: list, repository: dict) -> str:
    """
    Creates a formatted string with the definitions of the used functions.

    Args:
        functions (list): A list of the used functions.
        repository (dict): The repository containing the functions and their definitions.

    Returns:
        str: The concatenation of the definitions of the used functions.
    """
    formatted_functions = ""
    for func in functions:
        formatted_functions += repository['functions'][func] + '\n'
    return formatted_functions


def format_class_methods(class_name: str, class_info: dict) -> str:
    """
    Creates a formatted string with the definition of a class and its methods.

    Args:
        class_name (str): The name of the class.
        class_info (dict): The class information, including methods and __init__.

    Returns:
        str: The definition of the class formatted as a string.
    """
    formatted_class = f"class {class_name}:\n"
    formatted_class += f"    {class_info.get('__init__', '')}\n"  # Add the __init__ method if it exists
    for method_name, method_body in class_info['methods'].items():
        formatted_class += f"    def {method_name}(self):\n        {method_body}\n"
    return formatted_class


def creation_input_output(repository: dict) -> tuple:
    """
    Creates a formatted representation of the functions and classes used in the repository.

    Args:
        repository (dict): A dictionary containing functions and classes with their methods.

    Returns:
        tuple: A list of the formatted functions and a list of the function definitions.
    """
    formatted_results, function_bodies = [], []
    
    all_functions = list(repository['functions'].keys())
    all_classes = list(repository['classes'].keys())
    
    for func_name, func_body in repository['functions'].items():
        # Extract the functions used in the current function
        used_functions = extract_used_functions(func_body, all_functions, func_name)
        
        # Extract the classes used in the current function
        used_classes = extract_used_classes(func_body, all_classes)
        
        # Start formatting the code
        formatted_code = ""
        
        # Add the definitions of the used functions
        formatted_code += format_function_calls(used_functions, repository)
        
        # Add the definitions of the classes and their used methods
        for class_name in used_classes:
            class_info = repository['classes'][class_name]
            class_methods_used = extract_class_methods_used(func_body, class_info['methods'])
            
            if class_methods_used:
                formatted_code += format_class_methods(class_name, class_info)
        # Add the formatted code to the results
        formatted_results.append(formatted_code)
        function_bodies.append(func_body)
    
    return formatted_results, function_bodies


class CodeProcessor:
    def __init__(self, triggers: List[str]):
        """
        Initializes the processor with a list of triggers that separate the code.
        
        :param triggers: List of strings representing the triggers.
        """
        self.triggers = triggers

    def process_code(self, code_string: str, suffix: str = '', selector_lines: str = 'random') -> List[Dict[str, str]]:
        """
        Processes a source code by identifying triggers and separating the code into prefixes and suffixes.

        :param code_string: The code to process.
        :param suffix: An optional string to customize the suffix.
        :return: A list of dictionaries containing 'Prefix', 'Suffix', and 'Label'.
        """
        # Split the code into lines
        lines = code_string.split('\n')
        
        # Select a random number of lines up to the total number of lines
        if selector_lines == 'random':
            num_lines_to_process = random.randint(1, int(len(lines)))
        else:
            num_lines_to_process = int(len(lines) - 1)
        
        # List to store processed lines and dictionaries
        dataset = []
        
        for i in range(num_lines_to_process):
            line = lines[i]
            for trigger in self.triggers:
                if trigger in line:
                    # Separate the part before and after the trigger
                    prefix, _, line_suffix = line.partition(trigger)
                    
                    # Add a dictionary with the relevant parts
                    dataset.append({
                        'Prefix': '\n'.join(lines[:i] + [prefix + trigger]),
                        'Suffix': '\n'.join(lines[i + 1:]),
                        'Label': line_suffix   # Add the suffix
                    })
        
        return dataset


def create_dataset(result: Dict[str, List[List[str]]], triggers: List[str], selector_lines: str = "random") -> List[Dict[str, str]]:
    """
    Processes all repositories and the functions contained in them.

    :param result: A dictionary with repository data, where each key is a repository,
                   and the value is a list with two elements:
                   - A list of function names.
                   - A list of strings of the source code of the functions.
    :param triggers: A list of triggers for code separation.
    :return: A complete dataset of prefixes, suffixes, and labels.
    """
    processor = CodeProcessor(triggers)
    dataset = []

    for repo, (functions, codes) in result.items():
        print(f"Processing repository: {repo}")
        
        for index, code in enumerate(codes):
            function_name = functions[index]
            dataset += processor.process_code(code, function_name, selector_lines=selector_lines)
    
    return dataset
