from datetime import datetime
from .item_carrinho import ItemCarrinho

class Carrinho:
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = []
        self.status = "ABERTO"
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def adicionar_item(self, item):
        for i in self.itens:
            if str(i.produto.id) == str(item.produto.id):
                i.quantidade += item.quantidade
                return
        self.itens.append(item)

    def calcular_total(self):
        total = 0.0
        for item in self.itens:
            if hasattr(item, 'calcular_subtotal'):
                total += item.calcular_subtotal()
            elif hasattr(item, 'subtotal'):
                total += item.subtotal()
        return total

    def finalizar_compra(self, forma_pagamento):
        if hasattr(forma_pagamento, 'processar'):
            forma_pagamento.processar()
        self.status = "PROCESSADO"
        return True

    def to_json(self):
        c_id = '1' 
        
        if hasattr(self.cliente, 'cpf'):
            c_id = self.cliente.cpf
        elif isinstance(self.cliente, dict):
            c_id = self.cliente.get('cpf', '1')
        elif isinstance(self.cliente, str):
            c_id = self.cliente

        return {
            'cliente_id': c_id,
            'status': self.status,
            'data_criacao': self.data_criacao,
            'itens': [item.to_json() for item in self.itens]
        }

    @staticmethod
    def from_json(data, cliente_ref, produtos_db):
        carrinho = Carrinho(cliente_ref)
        carrinho.status = data.get('status', 'ABERTO')
        carrinho.data_criacao = data.get('data_criacao', '')
        
        if 'itens' in data:
            for item_data in data['itens']:
                try:
                    pid = str(item_data.get('produto_id'))
                    produto_real = produtos_db.get(pid)
                    
                    if produto_real:
                        qtd = item_data.get('quantidade', 1)
                        novo_item = ItemCarrinho(produto_real, qtd)
                        carrinho.itens.append(novo_item)
                except Exception as e:
                    print(f"Erro ao recriar item do carrinho: {e}")
                    continue
        
        return carrinho