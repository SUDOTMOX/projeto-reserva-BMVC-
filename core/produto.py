# Arquivo: core/produto.py
from abc import ABC, abstractmethod

class Produto(ABC):
   
    def __init__(self, nome, preco, categoria):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria
    
    @abstractmethod
    def calcular_frete(self):
        pass
    
    def to_json(self):
        return {'nome': self.nome, 'preco': self.preco, 'categoria': self.categoria}