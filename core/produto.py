# Arquivo: core/produto.py
from abc import ABC, abstractmethod

class Produto(ABC):
    """
    Classe Abstrata Base. 
    Objetivo: Definir a estrutura básica para HERANÇA e o método polimórfico.
    """
    def __init__(self, nome, preco, categoria):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria
    
    @abstractmethod
    def calcular_frete(self):
        """Método para Polimorfismo: Frete é diferente para Físico vs. Digital."""
        pass
    
    def to_json(self):
        return {'nome': self.nome, 'preco': self.preco, 'categoria': self.categoria}