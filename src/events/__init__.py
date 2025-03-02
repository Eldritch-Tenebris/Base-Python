"""
Gerenciamento de eventos do Discord.
Este módulo agrega todos os manipuladores de eventos do bot.
"""

# Importa os manipuladores de eventos
from .member import setup as setup_member_events
from .message import setup as setup_message_events

def setup_all_events(bot):
    """
    Configura todos os manipuladores de eventos para o bot
    
    Args:
        bot: Instância do bot Discord
    """
    # Registra cada grupo de eventos
    setup_member_events(bot)
    setup_message_events(bot)

# Exporta funções relevantes
__all__ = [
    "setup_all_events",
    "setup_member_events",
    "setup_message_events"
]