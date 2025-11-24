# Arquivo: core/carrinho.py
from .cliente import Cliente
from .item_carrinho import ItemCarrinho

# REMOVIDO: from pagamentos.pagamento import Pagamento  <-- ISSO CAUSAVA O LOOP

class Carrinho:
    """Demonstra ASSOCIAÇÃO (Cliente) e COMPOSIÇÃO (ItemCarrinho)."""
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.itens = []      
        self.status = "ABERTO"
    
    def adicionar_item(self, item: ItemCarrinho):
        self.itens.append(item)

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def finalizar_compra(self, forma_pagamento):
        """
        Recebe o objeto de pagamento.
        Não precisamos importar a classe Pagamento no topo para isso funcionar.
        """
        # O polimorfismo acontece aqui:
        sucesso = forma_pagamento.processar()
        
        if sucesso:
            self.status = "PROCESSADO"
            return True
        return False

    def remover_item(self, indice):
        """Remove um item da lista pelo índice (0, 1, 2...)."""
        if 0 <= indice < len(self.itens):
            self.itens.pop(indice)

    # --- MÉTODOS DE SERIALIZAÇÃO JSON ---
    def to_json(self):
        return {
            'cliente_cpf': self.cliente.cpf,
            'itens': [item.to_json() for item in self.itens],
            'status': self.status
        }
        
    # ... (Mantenha o método from_json como estava) ...
    @staticmethod
    def from_json(data, cliente_ref, produtos_db):
        # ... (reconstrução do Carrinho)
        pass