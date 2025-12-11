# Arquivo: pagamentos/pagamento.py
from abc import ABC, abstractmethod

class Pagamento(ABC):
<<<<<<< HEAD
   
=======
    """
    Interface Abstrata.
    Objetivo: Define o contrato para POLIMORFISMO e é o alvo da DEPENDÊNCIA.
    """
>>>>>>> a5dc457 (docker do projeto pronto)
    def __init__(self, valor=0.0):
        self.valor = valor

    @abstractmethod
    def processar(self):
<<<<<<< HEAD
=======
        """Método abstrato que deve ser implementado de forma polimórfica."""
>>>>>>> a5dc457 (docker do projeto pronto)
        pass
    
    def to_json(self):
        return {'valor': self.valor, 'tipo': self.__class__.__name__}