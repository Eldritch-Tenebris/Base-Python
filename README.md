# 🚀 Documentação da Base API e Bot Python

Este documento explica como utilizar a Base API para criar comandos e funcionalidades para seu bot no Discord, além de fornecer um guia para desenvolvimento de bots utilizando Python com MongoDB.

## 📋 Índice
As informações detalhadas sobre o projeto estão disponíveis na Wiki
- Início Rápido
- Instalação e Configuração
- Base API e Criação de Comandos
- Sistema de Banco de Dados MongoDB
- Embeds e Componentes
- Eventos e Handlers
- Hospedagem e Deployment
- FAQ e Solução de Problemas

---

## 🛠️ Criação de Comandos

### Usando `create_command` como Factory

```python
from base import create_command

class MeuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        cmd = create_command(self.bot)
        
        cmd.create_command(
            name="oi",
            description="Envia uma saudacão",
            callback=self.oi_command
        )
        
        cmd.create_command(
            name="eco",
            description="Repete uma mensagem",
            callback=self.eco_command,
            options={
                "mensagem": {"description": "A mensagem a ser repetida"}
            }
        )
        
    async def oi_command(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Olá, {interaction.user.mention}!")
        
    async def eco_command(self, interaction: discord.Interaction, mensagem: str):
        await interaction.response.send_message(mensagem)
```

### Configuração de Variáveis de Ambiente

Renomeie o arquivo `.env.example` para `.env` e configure as variáveis necessárias.

### ⚙️ Uso

1. **Executando o bot**
   ```bash
   python src/main.py
   ```

2. **Registrando novos comandos**  
   ```python
   import discord
   from discord import app_commands
   from discord.ext import commands

   class Example(commands.Cog):
       def __init__(self, bot):
           self.bot = bot
       
       @app_commands.command(name="exemplo", description="Um comando de exemplo")
       async def exemplo(self, interaction: discord.Interaction):
           await interaction.response.send_message("Funcionou!")

   async def setup(bot):
       await bot.add_cog(Example(bot))
   ```

---

## 🎨 Embeds e Componentes

### Criando Embeds

```python
from base import EmbedBuilder

embed = EmbedBuilder(
    title="Título do Embed",
    description="Descrição detalhada",
    color=discord.Color.blue()
).add_field(
    name="Campo 1",
    value="Valor do campo 1"
).add_field(
    name="Campo 2",
    value="Valor do campo 2"
).set_thumbnail(
    url="https://exemplo.com/imagem.png"
).set_footer(
    text="Rodapé do embed"
).build()
```

### Criando Componentes (Botões e Selects)

```python
from base import ComponentBuilder

view = ComponentBuilder().add_button(
    label="Clique em Mim",
    custom_id="botao_1",
    style=discord.ButtonStyle.primary,
    emoji="👍"
).add_button(
    label="Cancelar",
    custom_id="cancelar",
    style=discord.ButtonStyle.danger
).build()

await interaction.response.send_message("Mensagem com botões", view=view)
```

---

## 📁 Estrutura do Projeto

```
Discord-Python/
├── src/
│   ├── main.py               # Ponto de entrada da aplicação
│   ├── config.py             # Configurações e variáveis do bot
│   ├── database/             # Módulo de conexão com MongoDB
│   ├── cogs/                 # Módulos de comandos
│   ├── events/               # Tratamento de eventos do Discord
│   └── utils/                # Utilidades e funções auxiliares
├── .env                      # Variáveis de ambiente (não versionado)
├── .env.example              # Exemplo de variáveis de ambiente
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

---

## 🔧 Configurações Avançadas

O arquivo `config.py` permite configurar diversos aspectos do bot:

- Cor padrão para embeds
- Timeouts de comandos
- Tipo de atividade do bot
- Configurações de registro de comandos
- Nível de logging

---

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## 📞 Contato

Para dúvidas ou suporte, abra uma issue no repositório do GitHub.

Desenvolvido com ❤️ para facilitar o desenvolvimento de bots Discord em Python.