import discord
from src.base import create_embed, create_components, create_modal

def setup(cmd):
    """Configura comandos gerais do bot"""
    
    @cmd.create_command(
        name="help",
        description="Mostra os comandos disponíveis"
    )
    async def help_command(interaction):
        # Exibe lista de comandos disponíveis
        await interaction.response.send_message(
            embed=create_embed(
                title="📚 Ajuda",
                description="Aqui estão os comandos disponíveis:",
                fields=[
                    {"name": "/ping", "value": "Verifica a latência do bot"},
                    {"name": "/help", "value": "Mostra esta mensagem de ajuda"},
                    {"name": "/info", "value": "Informações sobre o bot"}
                ],
                color=discord.Color.blue()
            )
        )
    
    @cmd.create_command(
        name="info",
        description="Informações sobre o bot"
    )
    async def info_command(interaction):
        # Exibe informações gerais sobre o bot
        await interaction.response.send_message(
            embed=create_embed(
                title="ℹ️ Informações",
                description="Este bot foi criado usando a base API personalizada.",
                thumbnail=interaction.client.user.display_avatar.url,
                footer={"text": f"Solicitado por {interaction.user.name}"},
                color=discord.Color.blurple()
            ),
            view=create_components([
                discord.ui.Button(
                    label="GitHub",
                    url="https://github.com/seu-usuario/seu-repositorio",
                    style=discord.ButtonStyle.link,
                    emoji="🔗"
                )
            ])
        )
    
    @cmd.create_command(
        name="ping",
        description="Verifica a latência do bot"
    )
    async def ping_command(interaction):
        # Calcula e exibe a latência atual do bot
        latency = round(interaction.client.latency * 1000)
        
        # Define a cor com base na qualidade da latência
        if latency < 100:
            color = discord.Color.green()
            status = "Excelente"
        elif latency < 200:
            color = discord.Color.gold()
            status = "Bom"
        else:
            color = discord.Color.red()
            status = "Ruim"
        
        await interaction.response.send_message(
            embed=create_embed(
                title="🏓 Pong!",
                description=f"**Latência:** {latency}ms ({status})",
                color=color,
                timestamp=True
            )
        )
    
    # Função para processar feedback (definida antes do comando)
    async def process_feedback(interaction, values):
        # Processa o feedback enviado pelo usuário
        rating = values.get("rating", "?")
        comment = values.get("comment", "Nenhum comentário fornecido")
        
        # Validação simples
        try:
            rating_num = int(rating)
            if rating_num < 1 or rating_num > 5:
                raise ValueError("Avaliação deve ser entre 1 e 5")
                
            # Agradece pelo feedback
            await interaction.response.send_message(
                embed=create_embed(
                    title="✅ Feedback Recebido",
                    description="Obrigado por nos ajudar a melhorar!",
                    fields=[
                        {"name": "Avaliação", "value": f"{rating_num}/5 ⭐", "inline": True},
                        {"name": "Comentário", "value": comment}
                    ],
                    color=discord.Color.green()
                ),
                ephemeral=True
            )
            
        except ValueError:
            await interaction.response.send_message(
                "Por favor, forneça uma avaliação válida entre 1 e 5.",
                ephemeral=True
            )
    
    @cmd.create_command(
        name="feedback",
        description="Envia um feedback sobre o bot"
    )
    async def feedback_command(interaction):
        # Cria e envia um modal para o usuário preencher
        modal = create_modal(
            title="Feedback do Bot",
            fields=[
                {
                    "label": "Avaliação (1-5)",
                    "custom_id": "rating",
                    "placeholder": "Digite um número de 1 a 5",
                    "max_length": 1,
                    "required": True
                },
                {
                    "label": "Comentário",
                    "custom_id": "comment",
                    "style": discord.TextStyle.paragraph,
                    "placeholder": "Conte o que achou do bot...",
                    "required": True
                }
            ],
            callback=process_feedback  # Referência à função definida acima
        )
        
        await interaction.response.send_modal(modal)