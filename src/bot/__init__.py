"""
Núcleo do Bot Discord
Este pacote contém os componentes essenciais para o funcionamento do bot.
"""

from .client import BotClient
from .config import Config
from .constants import *

# Exportar classes e funções principais
__all__ = [
    "BotClient",
    "Config"
]