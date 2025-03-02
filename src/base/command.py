import discord
from discord.ext import commands
import inspect
from typing import Callable, Dict, Any, Optional, Union, List

class CommandBuilder:
    """
    Classe para facilitar a criação de comandos slash.
    """
    def __init__(self, bot):
        self.bot = bot
        
    def create_command(self, 
                      name: str, 
                      description: str = None,
                      callback: Callable = None,
                      options: Optional[Dict[str, Dict[str, Any]]] = None,
                      guild_ids: Optional[List[int]] = None):
        """
        Cria um comando slash de forma simplificada
        
        Args:
            name: Nome do comando
            description: Descrição do comando
            callback: Função que será executada quando o comando for chamado
            options: Opções do comando (parâmetros)
            guild_ids: IDs dos servidores para registrar o comando (None = global)
            
        Returns:
            O comando criado
        """
        description = description or f"Comando {name}"
        
        async def wrapper(interaction: discord.Interaction, **kwargs):
            if callback:
                await callback(interaction, **kwargs)
                
        command = discord.app_commands.Command(
            name=name,
            description=description,
            callback=wrapper
        )
        
        # Configura opções se fornecidas
        if options:
            for option_name, option_data in options.items():
                option_type = option_data.get("type", str)
                option_default = option_data.get("default", None)
                
                # Adiciona descrição para o parâmetro
                if "description" in option_data:
                    command.describe(**{option_name: option_data["description"]})
                    
                # Adiciona choices se fornecidos
                if "choices" in option_data:
                    choices = [
                        discord.app_commands.Choice(name=choice["name"], value=choice["value"])
                        for choice in option_data["choices"]
                    ]
                    option_choices = discord.app_commands.choices(name=option_name, choices=choices)
                    command.parameters[option_name].choices = option_choices
        
        # Adiciona o comando ao bot
        if guild_ids:
            for guild_id in guild_ids:
                self.bot.tree.add_command(command, guild=discord.Object(id=guild_id))
        else:
            self.bot.tree.add_command(command)
            
        return command

# Factory function para criar comandos
def create_command(bot=None):
    """
    Retorna uma instância do CommandBuilder ou um decorador para criar comandos
    
    Args:
        bot: A instância do bot Discord
        
    Returns:
        CommandBuilder ou decorator, dependendo se bot é fornecido
    
    Uso:
        cmd = create_command(bot)
        cmd.create_command(...)
        
        # OU como decorator (em desenvolvimento)
        @create_command
        async def ping(interaction):
            await interaction.response.send_message("Pong!")
    """
    if bot is not None:
        return CommandBuilder(bot)
    else:
        # Se chamado como decorator, retorna a função original
        # Será processado posteriormente pelo register_commands
        def decorator(func):
            func.__command_decorator__ = True
            return func
        return decorator

# Sistema para registrar comandos automaticamente
def register_commands(bot, module):
    """
    Registra todos os comandos marcados com @create_command em um módulo
    
    Args:
        bot: A instância do bot Discord
        module: O módulo onde procurar comandos decorados
    """
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if hasattr(func, "__command_decorator__"):
            # Extrai metadados do comando da função
            cmd_name = getattr(func, "__command_name__", name)
            cmd_description = func.__doc__ or f"Comando {cmd_name}"
            
            # Cria o comando
            cmd_builder = CommandBuilder(bot)
            cmd_builder.create_command(
                name=cmd_name,
                description=cmd_description,
                callback=func
            )