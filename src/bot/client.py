import discord
from discord import Intents
import os
import sys
import importlib

# Importa a base API
from src.base import create_command, create_embed, create_components

class BotClient:
    def __init__(self, config):
        # Configuração
        self.config = config
        
        # Intents
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        
        # Bot
        self.bot = discord.Bot(intents=intents)
        
        # Command builder da sua base API
        self.cmd = create_command(self.bot)
        
        # Registra eventos
        self.bot.event(self.on_ready)
        
        # Carrega módulos
        self._load_modules()
        
    async def on_ready(self):
        """Evento disparado quando o bot está pronto"""
        print(f'Bot conectado como {self.bot.user.name} ({self.bot.user.id})')
        print('------')
        
        # Define status do bot
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name="/help para comandos"
            )
        )
        
    def _load_modules(self):
        """Carrega todos os módulos de comandos dinamicamente"""
        try:
            # Exemplo de comando básico usando a base API
            @self.cmd.create_command(
                name="ping",
                description="Verifica a latência do bot"
            )
            async def ping_command(interaction):
                await interaction.response.send_message(
                    embed=create_embed(
                        title="🏓 Pong!",
                        description=f"Latência: {round(self.bot.latency * 1000)}ms",
                        color=discord.Color.green()
                    ),
                    view=create_components([
                        discord.ui.Button(
                            label="Atualizar",
                            custom_id="refresh_ping",
                            emoji="🔄",
                            style=discord.ButtonStyle.primary
                        )
                    ])
                )
            
            # Procura por módulos de comando na pasta commands
            commands_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "commands")
            if os.path.exists(commands_dir):
                for filename in os.listdir(commands_dir):
                    if filename.endswith('.py') and not filename.startswith('_'):
                        module_name = f"src.commands.{filename[:-3]}"
                        try:
                            module = importlib.import_module(module_name)
                            if hasattr(module, 'setup'):
                                module.setup(self.cmd)
                                print(f"Módulo carregado: {module_name}")
                        except Exception as e:
                            print(f"Erro ao carregar módulo {module_name}: {e}")
        except Exception as e:
            print(f"Erro ao carregar módulos: {e}")
    
    def run(self):
        """Inicia o bot"""
        token = self.config.get("token")
        if not token or token == "YOUR_BOT_TOKEN":
            token = os.getenv("DISCORD_TOKEN")
            if not token:
                raise ValueError("Token não encontrado nas configurações ou variáveis de ambiente")
        
        self.bot.run(token)