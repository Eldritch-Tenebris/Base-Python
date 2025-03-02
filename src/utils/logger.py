import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_to_console=True, log_to_file=True):
    """
    Configura e retorna um logger personalizado com handlers para arquivo e console.
    
    Args:
        name (str): Nome do logger
        log_to_console (bool): Indica se deve logar no console
        log_to_file (bool): Indica se deve logar em arquivo
        
    Returns:
        logging.Logger: Instância do logger configurado
    """
    # Cria o diretório de logs se não existir
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Nome do arquivo de log com data
    log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    # Configura o logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Captura todos os níveis de log
    
    # Evita duplicação de handlers se o logger já foi configurado
    if logger.handlers:
        return logger
    
    # Formatos de log
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s'
    )
    
    # Handler para arquivo com rotação (máximo 5MB, até 5 backups)
    if log_to_file:
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5_000_000,  # 5MB 
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # Armazena todos os níveis no arquivo
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Handler para console
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Só mostra INFO ou acima no console
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    logger.info(f"Logger '{name}' configurado com sucesso")
    return logger

# Instância padrão do logger para uso em todo o bot
logger = setup_logger('bot')

# Função de conveniência para obter loggers específicos de componentes
def get_logger(component_name):
    """
    Retorna um logger específico para um componente do bot
    
    Args:
        component_name (str): Nome do componente (ex: 'commands', 'events', etc)
        
    Returns:
        logging.Logger: Logger específico para o componente
    """
    return setup_logger(f'bot.{component_name}')