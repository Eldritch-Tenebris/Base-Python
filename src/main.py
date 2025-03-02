import sys
import os
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path para importações corretas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carrega variáveis de ambiente
load_dotenv()

# Importações do projeto
from bot.client import BotClient
from bot.config import Config
from src.utils.database import init_db

def main():
    """
    Função principal que inicializa e executa o bot.
    
    Processo:
    1. Carrega a configuração do arquivo settings.json
    2. Inicializa o banco de dados MongoDB
    3. Cria a instância do bot com a configuração
    4. Inicia o bot usando o token do Discord
    """
    try:
        # Inicializa o banco de dados
        print("Inicializando banco de dados...")
        init_db()
        
        # Carrega configurações
        print("Carregando configurações...")
        config = Config()
        
        # Cria e inicia o bot
        print("Iniciando o bot Discord...")
        bot = BotClient(config)
        bot.run()
    except Exception as e:
        print(f"Erro ao iniciar o bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()