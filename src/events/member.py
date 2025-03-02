import discord
from discord import Member
from src.utils import logger, get_guild
from src.base import create_embed

class MemberEventHandler:
    """Manipulador de eventos relacionados a membros do servidor"""
    
    def __init__(self, bot):
        """
        Inicializa o manipulador de eventos de membros
        
        Args:
            bot: Instância do bot Discord
        """
        self.bot = bot
        self.log = logger.get_logger('events.member')
        self.log.info('Manipulador de eventos de membros inicializado')
    
    async def on_member_join(self, member: Member):
        """
        Processa a entrada de um novo membro no servidor
        
        Args:
            member: Objeto Member do Discord
        """
        self.log.info(f"Membro {member.name} (ID: {member.id}) entrou no servidor {member.guild.name}")
        
        # Busca configurações do servidor
        guild_config = get_guild(member.guild.id)
        
        # Verifica se existe canal de boas-vindas configurado
        if guild_config and guild_config.get('welcome_channel_id'):
            welcome_channel = self.bot.get_channel(guild_config['welcome_channel_id'])
            
            if welcome_channel:
                # Monta a mensagem de boas-vindas (personalizada ou padrão)
                welcome_message = guild_config.get('welcome_message')
                if welcome_message:
                    # Substitui placeholders na mensagem
                    welcome_message = welcome_message.replace('{user}', member.mention)
                    welcome_message = welcome_message.replace('{server}', member.guild.name)
                    await welcome_channel.send(welcome_message)
                else:
                    # Mensagem padrão com embed
                    await welcome_channel.send(
                        embed=create_embed(
                            title=f"Bem-vindo(a) a {member.guild.name}!",
                            description=f"Olá {member.mention}, seja bem-vindo(a) ao servidor!\n"
                                       f"Agora somos {len(member.guild.members)} membros!",
                            thumbnail=member.display_avatar.url,
                            color=discord.Color.green()
                        )
                    )
    
    async def on_member_remove(self, member: Member):
        """
        Processa a saída de um membro do servidor
        
        Args:
            member: Objeto Member do Discord
        """
        self.log.info(f"Membro {member.name} (ID: {member.id}) saiu do servidor {member.guild.name}")
        
        # Busca configurações do servidor
        guild_config = get_guild(member.guild.id)
        
        # Verifica se existe canal de log configurado
        if guild_config and guild_config.get('log_channel_id'):
            log_channel = self.bot.get_channel(guild_config['log_channel_id'])
            
            if log_channel:
                # Notifica sobre a saída do membro
                await log_channel.send(
                    embed=create_embed(
                        title="Membro Saiu",
                        description=f"{member.name} saiu do servidor.",
                        fields=[
                            {"name": "ID", "value": str(member.id), "inline": True},
                            {"name": "Entrou em", "value": member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Desconhecido", "inline": True}
                        ],
                        thumbnail=member.display_avatar.url,
                        color=discord.Color.red(),
                        timestamp=True
                    )
                )

def setup(bot):
    """
    Registra os manipuladores de eventos no bot
    
    Args:
        bot: Instância do bot Discord
    """
    handler = MemberEventHandler(bot)
    bot.add_listener(handler.on_member_join, 'on_member_join')
    bot.add_listener(handler.on_member_remove, 'on_member_remove')