import discord
import asyncio
from typing import Union, List, Optional, Dict, Any, Callable
import re
import json
import os

def parse_time(time_str: str) -> int:
    """
    Converte uma string de tempo (1d, 2h, 30m, etc.) para segundos
    
    Args:
        time_str: String de tempo para converter
        
    Returns:
        Tempo em segundos
    """
    time_str = time_str.lower()
    seconds = 0
    
    # Regex para extrair números e unidades
    pattern = r'(\d+)([dhms])'
    matches = re.findall(pattern, time_str)
    
    for value, unit in matches:
        value = int(value)
        if unit == 'd':
            seconds += value * 86400  # dias para segundos
        elif unit == 'h':
            seconds += value * 3600   # horas para segundos
        elif unit == 'm':
            seconds += value * 60     # minutos para segundos
        elif unit == 's':
            seconds += value          # segundos
            
    return seconds

async def confirm_action(interaction: discord.Interaction, 
                        title: str, 
                        description: str,
                        timeout: int = 60) -> bool:
    """
    Solicita confirmação do usuário para uma ação
    
    Args:
        interaction: Interação do Discord
        title: Título da mensagem de confirmação
        description: Descrição da mensagem de confirmação
        timeout: Tempo em segundos para expirar a confirmação
        
    Returns:
        True se confirmado, False se cancelado ou expirado
    """
    from .embeds import EmbedBuilder
    from .components import ComponentBuilder
    
    # Criar embed de confirmação
    embed = EmbedBuilder(
        title=title,
        description=description,
        color=discord.Color.yellow()
    ).build()
    
    # Criar botões
    view = ComponentBuilder().add_button(
        label="Confirmar",
        custom_id="confirm",
        style=discord.ButtonStyle.success,
        emoji="✅"
    ).add_button(
        label="Cancelar",
        custom_id="cancel",
        style=discord.ButtonStyle.danger,
        emoji="❌"
    ).build()
    
    # Variável para armazenar o resultado
    result = {"confirmed": False}
    
    # Callbacks dos botões
    async def confirm_callback(button_interaction):
        if button_interaction.user.id != interaction.user.id:
            await button_interaction.response.send_message("Você não pode usar este botão.", ephemeral=True)
            return
        
        result["confirmed"] = True
        for child in view.children:
            child.disabled = True
        
        await button_interaction.response.edit_message(view=view)
        view.stop()
    
    async def cancel_callback(button_interaction):
        if button_interaction.user.id != interaction.user.id:
            await button_interaction.response.send_message("Você não pode usar este botão.", ephemeral=True)
            return
        
        for child in view.children:
            child.disabled = True
        
        await button_interaction.response.edit_message(view=view)
        view.stop()
    
    # Atribuir callbacks
    view.children[0].callback = confirm_callback
    view.children[1].callback = cancel_callback
    
    # Enviar mensagem com embed e botões
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    # Esperar pela interação ou timeout
    try:
        await view.wait()
    except asyncio.TimeoutError:
        for child in view.children:
            child.disabled = True
        await interaction.edit_original_response(view=view)
    
    return result["confirmed"]

def load_config(path: str) -> Dict[str, Any]:
    """
    Carrega um arquivo de configuração JSON
    
    Args:
        path: Caminho para o arquivo JSON
        
    Returns:
        Dados do arquivo JSON como dicionário
    """
    if not os.path.exists(path):
        return {}
        
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
        
def save_config(path: str, data: Dict[str, Any]) -> None:
    """
    Salva um dicionário em um arquivo JSON
    
    Args:
        path: Caminho para salvar o arquivo JSON
        data: Dados a serem salvos
    """
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
def format_number(number: Union[int, float]) -> str:
    """
    Formata um número com separadores de milhar
    
    Args:
        number: Número para formatar
        
    Returns:
        Número formatado como string
    """
    return f"{number:,}".replace(",", ".")