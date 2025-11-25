# Arquivo: core/models/vendas.py
from datetime import datetime

class ItemCarrinho:
    """Representa um item dentro do carrinho (Composição)."""
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self):
        return self.produto.preco * self.quantidade

    def to_json(self):
        return {
            'produto_id': self.produto.id,
            'quantidade': self.quantidade
        }

class Carrinho:
    """O Carrinho de Compras."""
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = [] # Lista de ItemCarrinho
        self.status = "ABERTO" # ou PROCESSADO
        self.data_criacao = datetime.now().strftime("%d/%m/%Y")

    def adicionar_item(self, item):
        # Verifica se item já existe para apenas somar quantidade
        for i in self.itens:
            if i.produto.id == item.produto.id:
                i.quantidade += item.quantidade
                return
        self.itens.append(item)

    def calcular_total(self):
        return sum([item.subtotal() for item in self.itens])

    def finalizar_compra(self, metodo_pagamento):
        # Aqui você poderia integrar com a lógica de pagamento
        self.status = "PROCESSADO"
        return True

    def to_json(self):
        return {
            'cliente_id': self.cliente.cpf, # Usamos CPF ou ID como ref
            'status': self.status,
            'data_criacao': self.data_criacao,
            'itens': [i.to_json() for i in self.itens]
        }
    
    @staticmethod
    def from_json(data, cliente_obj, produtos_db):
        """Reconstrói o carrinho (Complexo pois precisa ligar produtos)."""
        carrinho = Carrinho(cliente_obj)
        carrinho.status = data.get('status', 'ABERTO')
        carrinho.data_criacao = data.get('data_criacao', '')
        
        # Reconstrói os itens
        for item_data in data.get('itens', []):
            prod = produtos_db.get(item_data['produto_id'])
            if prod:
                novo_item = ItemCarrinho(prod, item_data['quantidade'])
                carrinho.itens.append(novo_item)
                
        return carrinho