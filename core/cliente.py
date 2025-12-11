
from .pessoa import Pessoa 
class Cliente(Pessoa):
    
    def __init__(self, nome, cpf, endereco, senha=None, is_admin=False):
        super().__init__(nome, cpf)
        self.endereco = endereco
        self.senha = senha 
        self.is_admin = is_admin 

    def apresentar_dados(self):
       
        dados_base = super().apresentar_dados()
        return f"{dados_base}, Endereço: {self.endereco}"
    

    def to_json(self):
        
        base_data = super().to_json()
        base_data['endereco'] = self.endereco
        base_data['senha'] = self.senha
        base_data['is_admin'] = self.is_admin
        return base_data

    @staticmethod
    def from_json(data):
        
        return Cliente(
            data['nome'],
            data['cpf'],
            data.get('endereco'),
            senha=data.get('senha'), 
            is_admin=data.get('is_admin', False) 
        )