# Arquivo: core/produto.py
from abc import ABC, abstractmethod

class Produto(ABC):
<<<<<<< HEAD
   
=======
    """
    Classe Abstrata Base. 
    Objetivo: Definir a estrutura básica para HERANÇA e o método polimórfico.
    """
>>>>>>> a5dc457 (docker do projeto pronto)
    def __init__(self, nome, preco, categoria):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria
    
    @abstractmethod
    def calcular_frete(self):
<<<<<<< HEAD
=======
        """Método para Polimorfismo: Frete é diferente para Físico vs. Digital."""
>>>>>>> a5dc457 (docker do projeto pronto)
        pass
    
    def to_json(self):
        return {'nome': self.nome, 'preco': self.preco, 'categoria': self.categoria}