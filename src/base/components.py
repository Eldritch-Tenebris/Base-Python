import discord
from typing import List, Optional, Union, Dict, Any, Callable

class ComponentBuilder:
    """
    Classe para facilitar a criação de componentes de interface (botões, selects).
    """
    def __init__(self, timeout: Optional[float] = 180.0):
        self.view = discord.ui.View(timeout=timeout)
        
    def add_button(self, 
                   label: str, 
                   custom_id: Optional[str] = None,
                   style: discord.ButtonStyle = discord.ButtonStyle.primary,
                   callback: Optional[Callable] = None,
                   disabled: bool = False,
                   emoji: Optional[Union[str, discord.Emoji]] = None,
                   url: Optional[str] = None,
                   row: Optional[int] = None):
        """
        Adiciona um botão à view
        
        Args:
            label: Texto do botão
            custom_id: ID personalizado para o botão
            style: Estilo do botão
            callback: Função a ser chamada quando o botão for clicado
            disabled: Se o botão está desabilitado
            emoji: Emoji para mostrar no botão
            url: URL para botões de link (style=ButtonStyle.link)
            row: Linha onde o botão será exibido (0-4)
        """
        if url:
            button = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label=label,
                url=url,
                emoji=emoji,
                disabled=disabled,
                row=row
            )
        else:
            button = discord.ui.Button(
                style=style,
                label=label,
                custom_id=custom_id or f"button_{label.lower().replace(' ', '_')}",
                emoji=emoji,
                disabled=disabled,
                row=row
            )
        
        if callback:
            async def wrapper(interaction):
                await callback(interaction)
                
            button.callback = wrapper
            
        self.view.add_item(button)
        return self
    
    def add_select(self, 
                  placeholder: str,
                  custom_id: Optional[str] = None,
                  options: List[Dict[str, Any]] = None,
                  callback: Optional[Callable] = None,
                  min_values: int = 1,
                  max_values: int = 1,
                  disabled: bool = False,
                  row: Optional[int] = None):
        """
        Adiciona um menu de seleção à view
        
        Args:
            placeholder: Texto exibido quando nada está selecionado
            custom_id: ID personalizado para o select
            options: Lista de opções para o select
            callback: Função a ser chamada quando uma opção for selecionada
            min_values: Número mínimo de valores selecionáveis
            max_values: Número máximo de valores selecionáveis
            disabled: Se o select está desabilitado
            row: Linha onde o select será exibido (0-4)
        """
        select = discord.ui.Select(
            placeholder=placeholder,
            custom_id=custom_id or f"select_{placeholder.lower().replace(' ', '_')}",
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
            row=row
        )
        
        if options:
            for option in options:
                select.add_option(
                    label=option["label"],
                    value=option.get("value", option["label"]),
                    description=option.get("description"),
                    emoji=option.get("emoji"),
                    default=option.get("default", False)
                )
            
        if callback:
            async def wrapper(interaction):
                await callback(interaction, select.values)
                
            select.callback = wrapper
            
        self.view.add_item(select)
        return self
    
    def build(self) -> discord.ui.View:
        """Retorna a view construída"""
        return self.view