"""
Módulo de comandos do bot Discord.
Este pacote contém todos os comandos disponíveis organizados por categoria.
"""

# Importa os módulos de comandos
from . import admin
from . import general
from . import music

# Lista de módulos para carregamento automático
command_modules = [
    admin,
    general,
    music
]

def load_all_commands(cmd):
    """
    Carrega todos os comandos nos módulos disponíveis
    
    Args:
        cmd: Gerenciador de comandos do bot
    """
    for module in command_modules:
        if hasattr(module, 'setup'):
            module.setup(cmd)
            print(f"Comandos carregados: {module.__name__}")

# Exporta funções e classes importantes
__all__ = [
    "load_all_commands",
    "command_modules"
]