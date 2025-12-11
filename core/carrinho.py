# Arquivo: core/carrinho.py
from datetime import datetime
from .cliente import Cliente
from .item_carrinho import ItemCarrinho
from pagamentos.pagamento import Pagamento 

class Carrinho:
    """Demonstra ASSOCIAÇÃO (Cliente) e COMPOSIÇÃO (ItemCarrinho)."""
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.itens = []      # Coleção que demonstra COMPOSIÇÃO
        self.status = "ABERTO"
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def adicionar_item(self, item: ItemCarrinho):
        """Método de Composição: anexa ItemCarrinho."""
        self.itens.append(item)

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def finalizar_compra(self, forma_pagamento: Pagamento):
        """
        Processa o pagamento usando POLIMORFISMO.
        O objeto 'forma_pagamento' pode ser Pix, Cartão ou Boleto.
        """
        forma_pagamento.processar()
        self.status = "PROCESSADO"

    # --- MÉTODOS DE SERIALIZAÇÃO JSON ---
    def to_json(self):
        """Salva o estado do carrinho."""
        return {
            'cliente_id': '1' if not hasattr(self.cliente, 'cpf') else self.cliente.cpf, # Simplificação para ID
            # Idealmente salvaríamos o ID real, aqui salvamos referência
            'status': self.status,
            'data_criacao': self.data_criacao,
            'itens': [item.to_json() for item in self.itens]
        }

    @staticmethod
    def from_json(data, cliente_ref, produtos_db):
        """
        Reconstrói o Carrinho.
        Precisa de referências externas (cliente e banco de produtos) para remontar os objetos.
        """
        carrinho = Carrinho(cliente_ref)
        carrinho.status = data.get('status', 'ABERTO')
        carrinho.data_criacao = data.get('data_criacao', '')
        
        if 'itens' in data:
            for item_data in data['itens']:
                try:
                    # ItemCarrinho.from_json precisa do dicionário de produtos para achar o objeto Produto
                    item = ItemCarrinho.from_json(item_data) 
                    # Nota: O ItemCarrinho.from_json original que fizemos buscava o produto dentro do próprio JSON do item.
                    # Se ele precisar buscar no DB geral, a lógica seria diferente. 
                    # Vamos assumir a versão que reconstrói o produto a partir dos dados salvos no item.
                    carrinho.itens.append(item)
                except Exception:
                    pass
        return carrinho