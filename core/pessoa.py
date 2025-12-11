<<<<<<< HEAD

class Pessoa:
=======
# Arquivo: core/pessoa.py

class Pessoa:
    """Classe Abstrata Base para HERANÇA."""
>>>>>>> a5dc457 (docker do projeto pronto)
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
    
    def to_json(self):
        return {'nome': self.nome, 'cpf': self.cpf}