import discord
from discord import app_commands
from src.base import create_embed, create_components

def setup(cmd):
    """Configura comandos administrativos do bot"""
    
    @cmd.create_command(
        name="kick",
        description="Expulsa um membro do servidor",
        options=[
            {
                "name": "membro",
                "description": "O membro a ser expulso",
                "type": discord.Member,
                "required": True
            },
            {
                "name": "motivo",
                "description": "Motivo da expulsão",
                "type": str,
                "required": False
            }
        ],
        permissions=discord.Permissions(kick_members=True)
    )
    async def kick_command(interaction, membro: discord.Member, motivo: str = "Nenhum motivo informado"):
        # Verifica permissões do bot
        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Não tenho permissão para expulsar membros!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Verifica hierarquia de cargos
        if membro.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Você não pode expulsar alguém com cargo igual ou superior ao seu!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Executa a expulsão
        try:
            await membro.kick(reason=f"{motivo} - Por: {interaction.user}")
            
            # Notifica sobre o sucesso
            await interaction.response.send_message(
                embed=create_embed(
                    title="👢 Membro Expulso",
                    description=f"{membro.mention} foi expulso do servidor.",
                    fields=[
                        {"name": "Motivo", "value": motivo},
                        {"name": "Por", "value": interaction.user.mention}
                    ],
                    color=discord.Color.orange(),
                    timestamp=True
                )
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Não foi possível expulsar o membro. Verifique as permissões.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description=f"Ocorreu um erro: {str(e)}",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
    
    @cmd.create_command(
        name="ban",
        description="Bane um membro do servidor",
        options=[
            {
                "name": "membro",
                "description": "O membro a ser banido",
                "type": discord.Member,
                "required": True
            },
            {
                "name": "motivo",
                "description": "Motivo do banimento",
                "type": str,
                "required": False
            },
            {
                "name": "dias",
                "description": "Dias de mensagens a serem excluídas (0-7)",
                "type": int,
                "required": False
            }
        ],
        permissions=discord.Permissions(ban_members=True)
    )
    async def ban_command(interaction, membro: discord.Member, motivo: str = "Nenhum motivo informado", dias: int = 1):
        # Valida o período de exclusão de mensagens
        dias = max(0, min(dias, 7))
        
        # Verifica permissões do bot
        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Não tenho permissão para banir membros!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Verifica hierarquia de cargos
        if membro.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="Você não pode banir alguém com cargo igual ou superior ao seu!",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Funções para manipular os botões de confirmação
        async def confirm_ban(button_interaction):
            if button_interaction.user.id != interaction.user.id:
                await button_interaction.response.send_message("Apenas quem iniciou o comando pode confirmar.", ephemeral=True)
                return
                
            try:
                await membro.ban(reason=f"{motivo} - Por: {interaction.user}", delete_message_days=dias)
                
                await button_interaction.response.edit_message(
                    embed=create_embed(
                        title="🔨 Membro Banido",
                        description=f"{membro.mention} foi banido do servidor.",
                        fields=[
                            {"name": "Motivo", "value": motivo},
                            {"name": "Por", "value": interaction.user.mention},
                            {"name": "Dias de mensagens excluídas", "value": str(dias)}
                        ],
                        color=discord.Color.red(),
                        timestamp=True
                    ),
                    view=None
                )
            except Exception as e:
                await button_interaction.response.send_message(
                    embed=create_embed(
                        title="❌ Erro",
                        description=f"Ocorreu um erro: {str(e)}",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
        
        async def cancel_ban(button_interaction):
            if button_interaction.user.id != interaction.user.id:
                await button_interaction.response.send_message("Apenas quem iniciou o comando pode cancelar.", ephemeral=True)
                return
                
            await button_interaction.response.edit_message(
                embed=create_embed(
                    title="🚫 Banimento Cancelado",
                    description=f"O banimento de {membro.mention} foi cancelado.",
                    color=discord.Color.green()
                ),
                view=None
            )
            
        # Interface de confirmação
        confirmation_view = create_components([
            {
                "type": "button",
                "style": discord.ButtonStyle.danger,
                "label": "Confirmar",
                "emoji": "✅",
                "callback": confirm_ban
            },
            {
                "type": "button",
                "style": discord.ButtonStyle.secondary,
                "label": "Cancelar",
                "emoji": "❌",
                "callback": cancel_ban
            }
        ])
        
        await interaction.response.send_message(
            embed=create_embed(
                title="⚠️ Confirmação de Banimento",
                description=f"Você está prestes a banir {membro.mention} do servidor.",
                fields=[
                    {"name": "Motivo", "value": motivo},
                    {"name": "Dias de mensagens que serão excluídas", "value": str(dias)}
                ],
                color=discord.Color.yellow()
            ),
            view=confirmation_view
        )
        
    @cmd.create_command(
        name="clear",
        description="Limpa mensagens do chat",
        options=[
            {
                "name": "quantidade",
                "description": "Número de mensagens para apagar (1-100)",
                "type": int,
                "required": True
            },
            {
                "name": "usuario",
                "description": "Apagar apenas mensagens deste usuário",
                "type": discord.Member,
                "required": False
            }
        ],
        permissions=discord.Permissions(manage_messages=True)
    )
    async def clear_command(interaction, quantidade: int, usuario: discord.Member = None):
        # Valida a quantidade
        if quantidade < 1 or quantidade > 100:
            await interaction.response.send_message(
                embed=create_embed(
                    title="❌ Erro",
                    description="A quantidade deve estar entre 1 e 100 mensagens.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
            
        # Responde imediatamente para evitar timeout
        await interaction.response.defer(ephemeral=True)
        
        # Filtro de mensagens personalizado
        def message_filter(message):
            if usuario:
                return message.author.id == usuario.id
            return True
            
        # Executa a limpeza
        try:
            deleted = await interaction.channel.purge(
                limit=quantidade,
                check=message_filter,
                bulk=True
            )
            
            # Notifica sobre o resultado
            user_text = f" de {usuario.mention}" if usuario else ""
            await interaction.followup.send(
                embed=create_embed(
                    title="🧹 Chat Limpo",
                    description=f"Foram apagadas {len(deleted)} mensagens{user_text}.",
                    color=discord.Color.blue()
                ),
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                embed=create_embed(
                    title="❌ Erro",
                    description=f"Ocorreu um erro ao limpar as mensagens: {str(e)}",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )