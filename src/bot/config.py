import os
import yaml
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    def __init__(self, config_path=None):
        """
        Inicializa a configuração do bot
        
        Args:
            config_path (str, opcional): Caminho para o arquivo de configuração
        """
        if config_path is None:
            # Caminho padrão para o arquivo de configuração
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base_path, "config", "settings.yml")
        
        self.config_path = config_path
        self._load_config()
        
        # Adiciona variáveis de ambiente à configuração
        self._add_env_vars()
    
    def _load_config(self):
        """Carrega as configurações do arquivo YAML"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
            else:
                self.config = {}
                print(f"Aviso: Arquivo de configuração não encontrado em {self.config_path}")
        except Exception as e:
            self.config = {}
            print(f"Erro ao carregar configurações: {e}")
    
    def _add_env_vars(self):
        """Adiciona variáveis de ambiente importantes à configuração"""
        env_vars = {
            "token": os.getenv("DISCORD_TOKEN"),
            "owner_id": os.getenv("OWNER_ID"),
            "guild_id": os.getenv("GUILD_ID"),
            "music_channel_id": os.getenv("MUSIC_CHANNEL_ID"),
            "log_channel_id": os.getenv("LOG_CHANNEL_ID"),
            "mongo_url": os.getenv("MONGO_URL"),
            "db_name": os.getenv("DB_NAME")
        }
        
        # Adiciona apenas as variáveis que existem
        for key, value in env_vars.items():
            if value is not None:
                self.config[key] = value
    
    def get(self, key, default=None):
        """
        Obtém um valor da configuração
        
        Args:
            key (str): Chave da configuração (suporta notação de ponto para acessar estruturas aninhadas)
            default: Valor padrão caso a chave não exista
            
        Returns:
            O valor da configuração ou o valor padrão
        """
        # Suporte para notação de ponto (ex: recursos.musica.habilitado)
        if "." in key:
            parts = key.split(".")
            value = self.config
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return default
            return value
        
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        Define um valor na configuração
        
        Args:
            key (str): Chave da configuração
            value: Valor a ser definido
        """
        self.config[key] = value
        self.save_config()

    def save_config(self):
        """Salva as configurações no arquivo YAML"""
        # Não salva informações sensíveis no arquivo
        sensitive_keys = ["token", "owner_id", "guild_id", "mongo_url"]
        save_config = {k: v for k, v in self.config.items() if k not in sensitive_keys}
        
        # Garante que o diretório de configuração existe
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(save_config, f, default_flow_style=False, sort_keys=False)