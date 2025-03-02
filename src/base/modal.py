import discord
from typing import List, Dict, Any, Callable, Optional

class CustomModal(discord.ui.Modal):
    """Classe personalizada para modais com callback dinâmico"""
    def __init__(self, title: str, callback: Callable, fields: List[Dict[str, Any]]):
        super().__init__(title=title)
        self.callback_func = callback
        
        # Adicionar campos ao modal
        for field in fields:
            text_input = discord.ui.TextInput(
                label=field["label"],
                custom_id=field.get("custom_id", field["label"].lower().replace(" ", "_")),
                style=field.get("style", discord.TextStyle.short),
                placeholder=field.get("placeholder", ""),
                default=field.get("default", ""),
                required=field.get("required", True),
                min_length=field.get("min_length", 1),
                max_length=field.get("max_length", 4000)
            )
            self.add_item(text_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        # Coleta os valores dos campos
        values = {item.custom_id: item.value for item in self.children}
        # Chama o callback com os valores
        await self.callback_func(interaction, values)

class ModalBuilder:
    """Builder para criar modais"""
    def __init__(self, title: str):
        self.title = title
        self.fields = []
        self.callback = None
        
    def add_field(self, 
                 label: str, 
                 custom_id: Optional[str] = None,
                 style: discord.TextStyle = discord.TextStyle.short,
                 placeholder: Optional[str] = None,
                 default: Optional[str] = None,
                 required: bool = True,
                 min_length: int = 1,
                 max_length: int = 4000):
        """Adiciona um campo ao modal"""
        self.fields.append({
            "label": label,
            "custom_id": custom_id or label.lower().replace(" ", "_"),
            "style": style,
            "placeholder": placeholder,
            "default": default,
            "required": required,
            "min_length": min_length,
            "max_length": max_length
        })
        return self
        
    def set_callback(self, callback: Callable):
        """Define o callback a ser chamado quando o modal for enviado"""
        self.callback = callback
        return self
        
    def build(self) -> discord.ui.Modal:
        """Constrói e retorna o modal"""
        if not self.callback:
            raise ValueError("Modal precisa de um callback definido")
        return CustomModal(self.title, self.callback, self.fields)

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
    return CustomModal(title, callback, fields)