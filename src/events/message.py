import discord
from discord.ext import commands
from src.utils import logger, add_xp, get_custom_command

class MessageEventHandler:
    """Manipula eventos relacionados a mensagens no Discord"""
    
    def __init__(self, bot):
        """
        Inicializa o manipulador de eventos
        
        Args:
            bot: Instância do bot Discord
        """
        self.bot = bot
        self.log = logger.get_logger('events.message')
        self.log.info('Manipulador de mensagens inicializado')
        
        # Cache para comandos personalizados (reduz consultas ao banco)
        self.custom_commands_cache = {}
    
    async def on_message(self, message):
        """
        Processa cada mensagem enviada em servidores
        
        Args:
            message: Objeto de mensagem do Discord
        """
        # Ignora mensagens do próprio bot
        if message.author.bot:
            return
            
        # Ignora mensagens privadas (DM)
        if not message.guild:
            return
            
        # Adiciona XP ao usuário (sistema de níveis)
        guild_id = message.guild.id
        user_id = message.author.id
        
        # Registra mensagem e adiciona XP
        new_level, leveled_up = add_xp(guild_id, user_id)
        
        # Notifica quando o usuário subir de nível
        if leveled_up:
            await message.channel.send(
                f"🎉 Parabéns, {message.author.mention}! Você alcançou o **nível {new_level}**!"
            )
            self.log.info(f"Usuário {user_id} subiu para o nível {new_level} no servidor {guild_id}")
        
        # Processa comandos personalizados
        if message.content.startswith('!'):
            cmd_name = message.content.split()[0][1:].lower()
            await self._handle_custom_command(message, cmd_name)
    
    async def _handle_custom_command(self, message, cmd_name):
        """
        Processa comandos personalizados
        
        Args:
            message: Objeto de mensagem do Discord
            cmd_name: Nome do comando (sem o prefixo)
        """
        guild_id = message.guild.id
        
        # Verifica o cache primeiro
        guild_commands = self.custom_commands_cache.get(guild_id, {})
        command = guild_commands.get(cmd_name)
        
        # Se não estiver no cache, consulta o banco
        if not command:
            command = get_custom_command(guild_id, cmd_name)
            
            # Atualiza o cache se o comando existir
            if command:
                if guild_id not in self.custom_commands_cache:
                    self.custom_commands_cache[guild_id] = {}
                self.custom_commands_cache[guild_id][cmd_name] = command
        
        # Executa o comando, se existir
        if command:
            await message.channel.send(command['response'])
            self.log.debug(f"Comando personalizado '{cmd_name}' executado no servidor {guild_id}")

def setup(bot):
    """
    Registra o manipulador de eventos no bot
    
    Args:
        bot: Instância do bot Discord
    """
    handler = MessageEventHandler(bot)
    bot.add_listener(handler.on_message, 'on_message')