import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Carrega configurações do ambiente
load_dotenv()

class DatabaseConnection:
    """Conexão singleton com MongoDB"""
    _instance = None
    client = None
    db = None
    
    def __new__(cls):
        """Garante instância única (padrão singleton)"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        """Estabelece conexão com o banco de dados MongoDB"""
        mongo_url = os.getenv("MONGO_URL")
        db_name = os.getenv("DB_NAME", "discord_bot")
        
        if not mongo_url:
            raise ValueError("MONGO_URL não encontrada no arquivo .env")
        
        try:
            # Conecta ao servidor MongoDB
            self.client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            # Verifica conexão
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            print(f"Conectado ao MongoDB: {db_name}")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Falha ao conectar ao MongoDB: {e}")
            raise
    
    def get_db(self):
        """Retorna a instância do banco de dados"""
        return self.db

class DatabaseManager:
    """Gerencia operações do banco de dados"""
    
    def __init__(self):
        self.db_conn = DatabaseConnection()
        self.db = self.db_conn.get_db()
    
    def init_db(self):
        """Inicializa coleções e índices"""
        # Cria índices para consultas otimizadas
        self.db.guilds.create_index("guild_id", unique=True)
        self.db.users.create_index("user_id", unique=True)
        self.db.members.create_index([("guild_id", 1), ("user_id", 1)], unique=True)
        self.db.custom_commands.create_index([("guild_id", 1), ("name", 1)], unique=True)
        print("Índices do MongoDB criados com sucesso!")

    #=================== SERVIDORES ===================
    
    def get_guild(self, guild_id):
        """Busca um servidor pelo ID"""
        return self.db.guilds.find_one({"guild_id": guild_id})
    
    def create_guild(self, guild_id, guild_name, **kwargs):
        """Cria documento para um novo servidor"""
        guild_data = {
            "guild_id": guild_id,
            "name": guild_name,
            "prefix": "!",
            "welcome_channel_id": None,
            "welcome_message": None,
            "log_channel_id": None,
            "music_channel_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Campos personalizados adicionais
        guild_data.update(kwargs)
        
        try:
            self.db.guilds.insert_one(guild_data)
            return guild_data
        except Exception as e:
            print(f"Erro ao criar servidor: {e}")
            return None
    
    def get_or_create_guild(self, guild_id, guild_name):
        """Busca ou cria um servidor"""
        guild = self.get_guild(guild_id)
        if not guild:
            guild = self.create_guild(guild_id, guild_name)
        return guild
        
    def update_guild(self, guild_id, **settings):
        """Atualiza as configurações de um servidor"""
        settings["updated_at"] = datetime.utcnow()
        
        result = self.db.guilds.update_one(
            {"guild_id": guild_id},
            {"$set": settings}
        )
        
        return result.modified_count > 0

    #=================== OPERAÇÕES DE MEMBRO ===================
    
    def get_member(self, guild_id, user_id):
        """Obtém dados de um membro em um servidor"""
        return self.db.members.find_one({
            "guild_id": guild_id,
            "user_id": user_id
        })
    
    def create_member(self, guild_id, user_id):
        """Cria um novo documento de membro"""
        member_data = {
            "guild_id": guild_id,
            "user_id": user_id,
            "xp": 0,
            "level": 0,
            "messages_count": 0,
            "last_message_time": datetime.utcnow(),
            "joined_at": datetime.utcnow()
        }
        
        try:
            self.db.members.insert_one(member_data)
            return member_data
        except Exception as e:
            print(f"Erro ao criar membro: {e}")
            return None
    
    def get_or_create_member(self, guild_id, user_id):
        """Obtém um membro ou cria se não existir"""
        member = self.get_member(guild_id, user_id)
        if not member:
            member = self.create_member(guild_id, user_id)
        return member
    
    def add_xp(self, guild_id, user_id, xp_amount=1):
        """
        Adiciona XP a um membro e atualiza seu nível
        
        Returns:
            (new_level, leveled_up)
        """
        # Primeiro obtém o membro atual para verificar seu nível
        member = self.get_member(guild_id, user_id)
        old_level = 0
        
        if member:
            old_level = member.get("level", 0)
        
        # Atualiza o membro (ou cria se não existir)
        result = self.db.members.find_one_and_update(
            {"guild_id": guild_id, "user_id": user_id},
            {
                "$inc": {"xp": xp_amount, "messages_count": 1},
                "$set": {"last_message_time": datetime.utcnow()},
                "$setOnInsert": {"level": 0, "joined_at": datetime.utcnow()}
            },
            upsert=True,
            return_document=True  # Retorna o documento após a atualização
        )
        
        # Calcula o novo nível
        current_xp = result["xp"]
        new_level = int(current_xp / 100)  # 100 XP por nível
        
        # Se o nível mudou, atualiza o documento
        if new_level > old_level:
            self.db.members.update_one(
                {"guild_id": guild_id, "user_id": user_id},
                {"$set": {"level": new_level}}
            )
            return new_level, True  # Retorna o novo nível e indica que subiu de nível
        
        return new_level, False  # Retorna o nível atual e indica que não subiu de nível
    
    #=================== COMANDOS PERSONALIZADOS ===================
    
    def get_custom_commands(self, guild_id):
        """Obtém todos os comandos personalizados de um servidor"""
        return list(self.db.custom_commands.find({"guild_id": guild_id}))
    
    def get_custom_command(self, guild_id, command_name):
        """Obtém um comando personalizado específico"""
        return self.db.custom_commands.find_one({
            "guild_id": guild_id,
            "name": command_name.lower()
        })
    
    def create_custom_command(self, guild_id, command_name, response, created_by):
        """Cria um comando personalizado"""
        command_data = {
            "guild_id": guild_id,
            "name": command_name.lower(),
            "response": response,
            "created_by": created_by,
            "uses": 0,
            "created_at": datetime.utcnow()
        }
        
        try:
            self.db.custom_commands.insert_one(command_data)
            return True
        except Exception as e:
            print(f"Erro ao criar comando personalizado: {e}")
            return False
    
    def use_custom_command(self, guild_id, command_name):
        """
        Incrementa o contador de usos de um comando personalizado
        
        Returns:
            O documento do comando ou None se não existir
        """
        command = self.db.custom_commands.find_one_and_update(
            {"guild_id": guild_id, "name": command_name.lower()},
            {"$inc": {"uses": 1}},
            return_document=True
        )
        return command
    
    #=================== PLAYLISTS ===================
    
    def create_playlist(self, guild_id, name, created_by):
        """Cria uma nova playlist"""
        playlist_data = {
            "guild_id": guild_id,
            "name": name,
            "created_by": created_by,
            "songs": [],
            "created_at": datetime.utcnow()
        }
        
        try:
            result = self.db.playlists.insert_one(playlist_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Erro ao criar playlist: {e}")
            return None
    
    def get_playlists(self, guild_id):
        """Obtém todas as playlists de um servidor"""
        return list(self.db.playlists.find({"guild_id": guild_id}))
    
    def get_playlist(self, playlist_id):
        """Obtém uma playlist específica"""
        try:
            return self.db.playlists.find_one({"_id": ObjectId(playlist_id)})
        except:
            return None
    
    def add_song_to_playlist(self, playlist_id, title, url, added_by):
        """Adiciona uma música a uma playlist"""
        song = {
            "title": title,
            "url": url,
            "added_by": added_by,
            "added_at": datetime.utcnow()
        }
        
        try:
            result = self.db.playlists.update_one(
                {"_id": ObjectId(playlist_id)},
                {"$push": {"songs": song}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao adicionar música: {e}")
            return False


# Instância global para facilitar o uso
db_manager = DatabaseManager()

# Para inicialização rápida
def init_db():
    """Inicializa o banco de dados"""
    db_manager.init_db()

# Métodos de conveniência para acesso rápido
def get_guild(guild_id):
    return db_manager.get_guild(guild_id)

def get_member(guild_id, user_id):
    return db_manager.get_member(guild_id, user_id)

def add_xp(guild_id, user_id, xp_amount=1):
    return db_manager.add_xp(guild_id, user_id, xp_amount)

# Para testes diretos
if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso!")
    # Você pode adicionar comandos de teste aqui