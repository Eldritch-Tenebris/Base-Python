"""
Constantes usadas pelo bot Discord.
Centraliza valores importantes para facilitar a configuração e manutenção.
"""

# IDs de canais e cargos
CHANNEL_ID = 123456789012345678  # Canal principal para anúncios
ADMIN_ROLE_ID = 987654321098765432  # Cargo com permissões administrativas

# Mensagens do sistema
WELCOME_MESSAGE = "Bem-vindo ao servidor!"  # Exibida para novos membros
GOODBYE_MESSAGE = "Até logo! Esperamos vê-lo novamente!"  # Exibida quando membros saem
ERROR_MESSAGE = "Ocorreu um erro. Tente novamente."  # Usada em tratamento de exceções
COMMAND_NOT_FOUND_MESSAGE = "Comando não encontrado. Use !help para ver a lista de comandos."  # Para comandos inválidos

# Limites e configurações
MAX_PLAYLIST_SIZE = 50  # Número máximo de músicas em uma playlist
XP_PER_MESSAGE = 2  # Quantidade de XP ganha por mensagem
XP_COOLDOWN = 60  # Segundos entre ganhos de XP (evita spam)
DEFAULT_PREFIX = "!"  # Prefixo padrão para comandos