"""
Módulo de utilidades para o bot Discord.
Fornece funções e classes para banco de dados, logging e outras ferramentas comuns.
"""

# Importações do banco de dados
from .database import DatabaseManager, init_db, get_guild, get_member, add_xp

# Importações do logger
from .logger import setup_logger, get_logger, logger

# Exporta utilitários para fácil acesso em outros módulos
__all__ = [
    # Database
    "DatabaseManager",
    "init_db",
    "get_guild",
    "get_member", 
    "add_xp",
    
    # Logging
    "setup_logger",
    "get_logger",
    "logger"
]