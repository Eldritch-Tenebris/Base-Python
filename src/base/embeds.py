import discord
from typing import Optional, Union, Dict, Any, List

class EmbedBuilder:
    """
    Classe para facilitar a criação de embeds.
    """
    def __init__(self, 
                title: Optional[str] = None, 
                description: Optional[str] = None,
                color: Optional[Union[discord.Color, int]] = discord.Color.blue(),
                url: Optional[str] = None):
        self.embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            url=url
        )
    
    def add_field(self, name: str, value: Union[str, int], inline: bool = True):
        """Adiciona um campo ao embed"""
        self.embed.add_field(name=name, value=value, inline=inline)
        return self
    
    def set_author(self, name: str, icon_url: Optional[str] = None, url: Optional[str] = None):
        """Define o autor do embed"""
        self.embed.set_author(name=name, icon_url=icon_url, url=url)
        return self
    
    def set_thumbnail(self, url: str):
        """Define a thumbnail do embed"""
        self.embed.set_thumbnail(url=url)
        return self
        
    def set_image(self, url: str):
        """Define a imagem principal do embed"""
        self.embed.set_image(url=url)
        return self
        
    def set_footer(self, text: str, icon_url: Optional[str] = None):
        """Define o rodapé do embed"""
        self.embed.set_footer(text=text, icon_url=icon_url)
        return self
        
    def set_timestamp(self, timestamp=None):
        """Define o timestamp do embed"""
        self.embed.timestamp = timestamp or discord.utils.utcnow()
        return self
        
    def add_fields(self, fields: List[Dict[str, Any]]):
        """Adiciona múltiplos campos ao embed"""
        for field in fields:
            self.add_field(
                name=field["name"],
                value=field["value"],
                inline=field.get("inline", True)
            )
        return self
        
    def build(self) -> discord.Embed:
        """Retorna o embed construído"""
        return self.embed