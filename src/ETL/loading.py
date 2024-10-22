import random
from typing import List, Dict

def extract_used_functions(function_body: str, available_functions: list, current_function: str) -> list:
    """
    Estrai le funzioni usate nel corpo di una funzione, escludendo la funzione stessa.

    Args:
        function_body (str): Il corpo della funzione corrente.
        available_functions (list): L'elenco di tutte le funzioni disponibili.
        current_function (str): Il nome della funzione corrente.

    Returns:
        list: Un elenco delle funzioni usate nel corpo della funzione.
    """
    return [func for func in available_functions if func in function_body and func != current_function]


def extract_used_classes(function_body: str, available_classes: list) -> list:
    """
    Estrai le classi usate nel corpo di una funzione.

    Args:
        function_body (str): Il corpo della funzione corrente.
        available_classes (list): L'elenco di tutte le classi disponibili.

    Returns:
        list: Un elenco delle classi usate nel corpo della funzione.
    """
    return [cls for cls in available_classes if cls in function_body]


def extract_class_methods_used(function_body: str, class_methods: dict) -> dict:
    """
    Estrai i metodi di una classe che vengono utilizzati nel corpo di una funzione.

    Args:
        function_body (str): Il corpo della funzione corrente.
        class_methods (dict): Un dizionario dei metodi della classe.

    Returns:
        dict: Un dizionario con i metodi della classe usati nella funzione.
    """
    used_methods = {method_name: method_body for method_name, method_body in class_methods.items() if method_name in function_body}
    return used_methods


def format_function_calls(functions: list, repository: dict) -> str:
    """
    Crea una stringa formattata con le definizioni delle funzioni usate.

    Args:
        functions (list): Un elenco delle funzioni usate.
        repository (dict): Il repository contenente le funzioni e le loro definizioni.

    Returns:
        str: La concatenazione delle definizioni delle funzioni usate.
    """
    formatted_functions = ""
    for func in functions:
        formatted_functions += repository['functions'][func] + '\n'
    return formatted_functions


def format_class_methods(class_name: str, class_info: dict) -> str:
    """
    Crea una stringa formattata con la definizione di una classe e i suoi metodi.

    Args:
        class_name (str): Il nome della classe.
        class_info (dict): Le informazioni della classe, inclusi metodi e init.

    Returns:
        str: La definizione della classe formattata come stringa.
    """
    formatted_class = f"class {class_name}:\n"
    formatted_class += f"    {class_info.get('__init__', '')}\n"  # Aggiungi il metodo __init__ se esiste
    for method_name, method_body in class_info['methods'].items():
        formatted_class += f"    def {method_name}(self):\n        {method_body}\n"
    return formatted_class


def creation_input_output(repository: dict) -> tuple:
    """
    Crea una rappresentazione formattata delle funzioni e delle classi usate nel repository.

    Args:
        repository (dict): Un dizionario contenente funzioni e classi con i loro metodi.

    Returns:
        tuple: Un elenco delle funzioni formattate e un elenco delle definizioni di funzioni.
    """
    formatted_results, function_bodies = [], []
    
    all_functions = list(repository['functions'].keys())
    all_classes = list(repository['classes'].keys())
    
    for func_name, func_body in repository['functions'].items():
        # Estrai le funzioni usate nella funzione corrente
        used_functions = extract_used_functions(func_body, all_functions, func_name)
        
        # Estrai le classi usate nella funzione corrente
        used_classes = extract_used_classes(func_body, all_classes)
        
        # Inizia a formattare il codice
        formatted_code = ""
        
        # Aggiungi le definizioni delle funzioni usate
        formatted_code += format_function_calls(used_functions, repository)
        
        # Aggiungi le definizioni delle classi e dei loro metodi usati
        for class_name in used_classes:
            class_info = repository['classes'][class_name]
            class_methods_used = extract_class_methods_used(func_body, class_info['methods'])
            
            if class_methods_used:
                formatted_code += format_class_methods(class_name, class_info)
        # Aggiungi il codice formattato ai risultati
        formatted_results.append(formatted_code)
        function_bodies.append(func_body)
    
    return formatted_results, function_bodies


class CodeProcessor:
    def __init__(self, triggers: List[str]):
        """
        Inizializza il processore con una lista di trigger che separano il codice.
        
        :param triggers: Lista di stringhe che rappresentano i trigger.
        """
        self.triggers = triggers

    def process_code(self, code_string: str, suffix: str = '', selector_lines : str ='random') -> List[Dict[str, str]]:
        """
        Processa un codice sorgente identificando i triggers e separando il codice in prefissi e suffissi.

        :param code_string: Il codice da processare.
        :param suffix: Una stringa opzionale per personalizzare il suffisso.
        :return: Una lista di dizionari contenenti 'Prefix', 'Suffix' e 'Label'.
        """
        # Dividiamo il codice in righe
        lines = code_string.split('\n')
        
        # Selezioniamo un numero randomico di righe fino al numero totale delle righe
        if selector_lines == 'random':
            num_lines_to_process = random.randint(1, int(len(lines)))
        else:
            num_lines_to_process = int(len(lines)-1)
        
        # Lista per immagazzinare le linee processate e i dizionari
        dataset = []
        
        for i in range(num_lines_to_process):
            line = lines[i]
            for trigger in self.triggers:
                if trigger in line:
                    # Separiamo la parte prima e dopo il trigger
                    prefix, _, line_suffix = line.partition(trigger)
                    
                    # Aggiungiamo un dizionario con le parti rilevanti
                    dataset.append({
                        'Prefix': '\n'.join(lines[:i] + [prefix + trigger]),
                        'Suffix': '\n'.join(lines[i+1:]),
                        'Label': line_suffix   # Aggiungiamo il suffisso
                    })
        
        return dataset


def create_dataset(result: Dict[str, List[List[str]]], triggers: List[str],selector_lines:str="random" ) -> List[Dict[str, str]]:
    """
    Processa tutti i repository e le funzioni in essi contenute.

    :param result: Un dizionario con i dati del repository, in cui ogni chiave è un repository,
                   e il valore è una lista con due elementi:
                   - Un elenco di nomi delle funzioni.
                   - Un elenco di stringhe del codice sorgente delle funzioni.
    :param triggers: Una lista di trigger per la separazione del codice.
    :return: Un dataset completo di prefissi, suffissi e etichette.
    """
    processor = CodeProcessor(triggers)
    dataset = []

    for repo, (functions, codes) in result.items():
        print(f"Processing repository: {repo}")
        
        for index, code in enumerate(codes):
            function_name = functions[index]
            dataset += processor.process_code(code, function_name,selector_lines=selector_lines)
    
    return dataset

