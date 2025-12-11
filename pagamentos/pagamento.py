# Arquivo: pagamentos/pagamento.py
from abc import ABC, abstractmethod

class Pagamento(ABC):
   
    def __init__(self, valor=0.0):
        self.valor = valor

    @abstractmethod
    def processar(self):
        pass
    
    def to_json(self):
        return {'valor': self.valor, 'tipo': self.__class__.__name__}