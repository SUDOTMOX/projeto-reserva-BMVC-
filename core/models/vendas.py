from datetime import datetime

class ItemCarrinho:
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
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = []
        self.status = "ABERTO" # ou PROCESSADO
        self.data_criacao = datetime.now().strftime("%d/%m/%Y")

    def adicionar_item(self, item):
     
        for i in self.itens:
            if i.produto.id == item.produto.id:
                i.quantidade += item.quantidade
                return
        self.itens.append(item)

    def calcular_total(self):
        return sum([item.subtotal() for item in self.itens])

    def finalizar_compra(self, metodo_pagamento):
       
        self.status = "PROCESSADO"
        return True

    def to_json(self):
        return {
            'cliente_id': self.cliente.cpf, 
            'status': self.status,
            'data_criacao': self.data_criacao,
            'itens': [i.to_json() for i in self.itens]
        }
    
    @staticmethod
    def from_json(data, cliente_obj, produtos_db):
       
        carrinho = Carrinho(cliente_obj)
        carrinho.status = data.get('status', 'ABERTO')
        carrinho.data_criacao = data.get('data_criacao', '')
        
       
        for item_data in data.get('itens', []):
            prod = produtos_db.get(item_data['produto_id'])
            if prod:
                novo_item = ItemCarrinho(prod, item_data['quantidade'])
                carrinho.itens.append(novo_item)
                
        return carrinho