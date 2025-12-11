<<<<<<< HEAD

from .pessoa import Pessoa 
class Cliente(Pessoa):
    
    def __init__(self, nome, cpf, endereco, senha=None, is_admin=False):
=======
# Arquivo: core/cliente.py

from .pessoa import Pessoa # Importação relativa correta

class Cliente(Pessoa):
    """
    Classe Concreta.
    Objetivo: Demonstrar HERANÇA (extensão de Pessoa), POLIMORFISMO (apresentar_dados)
              e participar da ASSOCIAÇÃO (com Carrinho). Inclui atributos de Login/ADM.
    """
    def __init__(self, nome, cpf, endereco, senha=None, is_admin=False):
        # Chamada ao construtor da superclasse (Herança)
>>>>>>> a5dc457 (docker do projeto pronto)
        super().__init__(nome, cpf)
        self.endereco = endereco
        self.senha = senha 
        self.is_admin = is_admin 

    def apresentar_dados(self):
<<<<<<< HEAD
       
        dados_base = super().apresentar_dados()
        return f"{dados_base}, Endereço: {self.endereco}"
    

    def to_json(self):
        
=======
        """
        Método Sobrescrito.
        Objetivo: Demonstrar o POLIMORFISMO. Retorna o formato específico do Cliente.
        """
        dados_base = super().apresentar_dados()
        return f"{dados_base}, Endereço: {self.endereco}"
    
    # --- MÉTODOS DE SERIALIZAÇÃO JSON ---

    def to_json(self):
        """
        Serializa o Cliente para JSON.
        Objetivo: Salvar todos os atributos, incluindo os herdados e os de Login/ADM.
        """
>>>>>>> a5dc457 (docker do projeto pronto)
        base_data = super().to_json()
        base_data['endereco'] = self.endereco
        base_data['senha'] = self.senha
        base_data['is_admin'] = self.is_admin
        return base_data

    @staticmethod
    def from_json(data):
<<<<<<< HEAD
        
=======
        """
        Reconstrói a instância de Cliente a partir dos dados JSON.
        Objetivo: Usar .get() para evitar AttributeError em caso de dados antigos ou incompletos.
        """
>>>>>>> a5dc457 (docker do projeto pronto)
        return Cliente(
            data['nome'],
            data['cpf'],
            data.get('endereco'),
            senha=data.get('senha'), 
            is_admin=data.get('is_admin', False) 
        )