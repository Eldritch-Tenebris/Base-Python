import discord
from typing import Dict, Any, List, Optional, Union, Callable
from .embeds import EmbedBuilder
from .components import ComponentBuilder
from .modal import create_modal as create_modal_base

def create_embed(title: Optional[str] = None,
                description: Optional[str] = None,
                color: Optional[Union[discord.Color, int]] = discord.Color.blue(),
                fields: Optional[List[Dict[str, Any]]] = None,
                author: Optional[Dict[str, Any]] = None,
                thumbnail: Optional[str] = None,
                image: Optional[str] = None,
                footer: Optional[Dict[str, Any]] = None,
                timestamp: Any = None) -> discord.Embed:
    """
    Função helper para criar embeds de forma rápida
    
    Args:
        title: Título do embed
        description: Descrição do embed
        color: Cor do embed
        fields: Lista de campos (dicionários com name, value, inline)
        author: Dicionário com name, icon_url, url
        thumbnail: URL da thumbnail
        image: URL da imagem
        footer: Dicionário com text, icon_url
        timestamp: Timestamp do embed
        
    Returns:
        O embed construído
    """
    builder = EmbedBuilder(title=title, description=description, color=color)
    
    if fields:
        for field in fields:
            builder.add_field(
                name=field["name"],
                value=field["value"],
                inline=field.get("inline", True)
            )
    
    if author:
        builder.set_author(
            name=author["name"],
            icon_url=author.get("icon_url"),
            url=author.get("url")
        )
    
    if thumbnail:
        builder.set_thumbnail(url=thumbnail)
        
    if image:
        builder.set_image(url=image)
        
    if footer:
        builder.set_footer(text=footer["text"], icon_url=footer.get("icon_url"))
        
    if timestamp is not None:
        builder.set_timestamp(timestamp)
        
    return builder.build()

def create_components(buttons: Optional[List[Dict[str, Any]]] = None,
                     selects: Optional[List[Dict[str, Any]]] = None,
                     timeout: float = 180.0) -> discord.ui.View:
    """
    Função helper para criar componentes rapidamente
    
    Args:
        buttons: Lista de botões (dicionários de configuração)
        selects: Lista de selects (dicionários de configuração)
        timeout: Tempo limite da view
        
    Returns:
        A view construída
    """
    builder = ComponentBuilder(timeout=timeout)
    
    if buttons:
        for button in buttons:
            builder.add_button(
                label=button["label"],
                custom_id=button.get("custom_id"),
                style=button.get("style", discord.ButtonStyle.primary),
                callback=button.get("callback"),
                disabled=button.get("disabled", False),
                emoji=button.get("emoji"),
                url=button.get("url"),
                row=button.get("row")
            )
    
    if selects:
        for select in selects:
            builder.add_select(
                placeholder=select["placeholder"],
                custom_id=select.get("custom_id"),
                options=select.get("options", []),
                callback=select.get("callback"),
                min_values=select.get("min_values", 1),
                max_values=select.get("max_values", 1),
                disabled=select.get("disabled", False),
                row=select.get("row")
            )
            
    return builder.build()

def create_modal(title: str, fields: List[Dict[str, Any]], callback: Callable) -> discord.ui.Modal:
    """
    Função helper para criar modais rapidamente
    
    Args:
        title: Título do modal
        fields: Lista de campos
        callback: Função a ser chamada quando o modal for enviado
        
    Returns:
        O modal configurado
    """
    return create_modal_base(title, fields, callback)