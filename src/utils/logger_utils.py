import logging

def setup_detailed_logger(log_file='detailed_log.log', log_level=logging.DEBUG):
    """
    Configura un logger dettagliato che include nome del file, numero di riga, nome della funzione e orario.

    :param log_file: Il nome del file in cui scrivere i log (default: 'detailed_log.log').
    :param log_level: Il livello minimo di logging (default: logging.DEBUG).
    :return: Un oggetto logger configurato.
    """
    # Creazione del logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)  # Imposta il livello minimo di logging

    # Formato dettagliato del log
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Creazione di un handler per il file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Creazione di un handler per la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Aggiunta degli handler al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Uso della funzione logger
logger = setup_detailed_logger(log_file='app_log.log', log_level=logging.DEBUG)