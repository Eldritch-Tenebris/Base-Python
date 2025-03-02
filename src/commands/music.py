import discord
from src.base import create_embed, create_components

def setup(cmd):
    """Configura os comandos de música do bot"""
    
    @cmd.create_command(
        name="play",
        description="Toca uma música a partir de uma URL",
        options=[
            {
                "name": "url",
                "description": "URL da música (YouTube, SoundCloud, etc.)",
                "type": str,
                "required": True
            }
        ]
    )
    async def play_command(interaction, url: str):
        # Verifica canal de voz
        if not interaction.user.voice:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Você precisa estar em um canal de voz para usar este comando!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Resposta imediata para evitar timeout
        await interaction.response.defer()
        
        # Simulação temporária - implementação real requer wavelink ou discord.py[voice]
        await interaction.followup.send(
            embed=create_embed(
                title="🎵 Tocando Música",
                description=f"[Música]({url}) adicionada à fila.",
                thumbnail="https://img.youtube.com/vi/ID_DO_VIDEO/maxresdefault.jpg",
                fields=[
                    {"name": "Canal", "value": interaction.user.voice.channel.name},
                    {"name": "Solicitado por", "value": interaction.user.mention}
                ],
                color=discord.Color.blue()
            ),
            view=create_components([
                {
                    "type": "button",
                    "style": discord.ButtonStyle.secondary,
                    "label": "Pausar",
                    "emoji": "⏸️",
                    "custom_id": "music_pause"
                },
                {
                    "type": "button",
                    "style": discord.ButtonStyle.danger,
                    "label": "Parar",
                    "emoji": "⏹️",
                    "custom_id": "music_stop"
                },
                {
                    "type": "button",
                    "style": discord.ButtonStyle.primary,
                    "label": "Pular",
                    "emoji": "⏭️",
                    "custom_id": "music_skip"
                }
            ])
        )
    
    @cmd.create_command(
        name="stop",
        description="Para a reprodução atual"
    )
    async def stop_command(interaction):
        # Verificações de contexto
        if not interaction.user.voice:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Você precisa estar em um canal de voz!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        if not interaction.guild.voice_client or interaction.guild.voice_client.channel != interaction.user.voice.channel:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="O bot precisa estar no mesmo canal que você!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Simulação temporária de parar música
        await interaction.response.send_message(
            embed=create_embed(
                title="⏹️ Música Parada",
                description="A reprodução foi interrompida.",
                color=discord.Color.red()
            )
        )
    
    @cmd.create_command(
        name="pause",
        description="Pausa a música atual"
    )
    async def pause_command(interaction):
        # Verificações de contexto
        if not interaction.user.voice:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Você precisa estar em um canal de voz!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        if not interaction.guild.voice_client or interaction.guild.voice_client.channel != interaction.user.voice.channel:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="O bot precisa estar no mesmo canal que você!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Simulação temporária de pausar música
        await interaction.response.send_message(
            embed=create_embed(
                title="⏸️ Música Pausada",
                description="A reprodução foi pausada.",
                color=discord.Color.yellow()
            ),
            view=create_components([
                {
                    "type": "button",
                    "style": discord.ButtonStyle.success,
                    "label": "Retomar",
                    "emoji": "▶️",
                    "custom_id": "music_resume"
                }
            ])
        )
    
    @cmd.create_command(
        name="queue",
        description="Mostra a fila de músicas"
    )
    async def queue_command(interaction):
        # Simulação temporária de fila de músicas
        await interaction.response.send_message(
            embed=create_embed(
                title="🎶 Fila de Músicas",
                description="Músicas na fila:",
                fields=[
                    {"name": "1. Tocando agora", "value": "Nome da Música 1 - Autor"},
                    {"name": "2.", "value": "Nome da Música 2 - Autor"},
                    {"name": "3.", "value": "Nome da Música 3 - Autor"}
                ],
                footer={"text": "Página 1/1 • Total: 3 músicas"},
                color=discord.Color.blue()
            ),
            view=create_components([
                {
                    "type": "button",
                    "style": discord.ButtonStyle.secondary,
                    "label": "Anterior",
                    "emoji": "◀️",
                    "custom_id": "queue_prev",
                    "disabled": True
                },
                {
                    "type": "button",
                    "style": discord.ButtonStyle.danger,
                    "label": "Limpar Fila",
                    "emoji": "🗑️",
                    "custom_id": "queue_clear"
                },
                {
                    "type": "button", 
                    "style": discord.ButtonStyle.secondary,
                    "label": "Próxima",
                    "emoji": "▶️",
                    "custom_id": "queue_next",
                    "disabled": True
                }
            ])
        )
    
    @cmd.create_command(
        name="skip",
        description="Pula para a próxima música"
    )
    async def skip_command(interaction):
        # Verificações de contexto
        if not interaction.user.voice:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Você precisa estar em um canal de voz!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        if not interaction.guild.voice_client or interaction.guild.voice_client.channel != interaction.user.voice.channel:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="O bot precisa estar no mesmo canal que você!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Simulação temporária de pular música
        await interaction.response.send_message(
            embed=create_embed(
                title="⏭️ Música Pulada",
                description="Pulando para a próxima música.",
                color=discord.Color.blue()
            )
        )