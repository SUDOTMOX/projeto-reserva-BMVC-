# Arquivo: pagamentos/pagamento.py
from abc import ABC, abstractmethod

# NÃO FAÇA import de Carrinho aqui para evitar o ciclo.
# NÃO FAÇA 'from .pagamento import Pagamento' (isso causa o erro da linha 1).

class Pagamento(ABC):
    """
    Interface Abstrata.
    """
    def __init__(self, pedido):
        self.pedido = pedido # O Python aceita o objeto sem precisar importar a classe dele aqui.

    @abstractmethod
    def processar(self):
        pass
    
    def to_json(self):
        # Verifica se o pedido tem o método calcular_total antes de chamar (Duck Typing)
        valor = 0.0
        if hasattr(self.pedido, 'calcular_total'):
            valor = self.pedido.calcular_total()
            
        return {
            'valor': valor, 
            'tipo': self.__class__.__name__
        }