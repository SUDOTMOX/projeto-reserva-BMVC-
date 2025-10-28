# Arquivo: core/carrinho.py (Corrigido para garantir o método adicionar_item)

from .cliente import Cliente
from .item_carrinho import ItemCarrinho
from pagamentos.pagamento import Pagamento 

class Carrinho:
    """Demonstra ASSOCIAÇÃO (Cliente) e COMPOSIÇÃO (ItemCarrinho)."""
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.itens = []      # Coleção que demonstra COMPOSIÇÃO
        self.status = "ABERTO"
        # O método adicionar_item DEVE estar aqui dentro da classe:
    
    def adicionar_item(self, item: ItemCarrinho):
        """Método de Composição: anexa ItemCarrinho."""
        self.itens.append(item)

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def finalizar_compra(self, forma_pagamento: Pagamento):
        # ... (Lógica de pagamento omitida, mas a estrutura está correta)
        pass

    # --- MÉTODOS DE SERIALIZAÇÃO JSON ---
    def to_json(self):
        # ... (serialização do Carrinho para JSON)
        pass

    @staticmethod
    def from_json(data, cliente_ref, produtos_db):
        # ... (reconstrução do Carrinho)
        pass