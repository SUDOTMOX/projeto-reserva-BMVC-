
class Pessoa:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def to_json(self):
        return {'nome': self.nome, 'cpf': self.cpf}

class Cliente(Pessoa):
    def __init__(self, nome, cpf, endereco, senha=None, is_admin=False):
        super().__init__(nome, cpf)
        self.endereco = endereco
        self.senha = senha
        self.is_admin = is_admin

    def to_json(self):
        data = super().to_json()
        data['endereco'] = self.endereco
        data['senha'] = self.senha
        data['is_admin'] = self.is_admin
        return data

    @staticmethod
    def from_json(data):
        return Cliente(
            nome=data['nome'],
            cpf=data['cpf'],
            endereco=data['endereco'],
            senha=data.get('senha'),
            is_admin=data.get('is_admin', False)
        )