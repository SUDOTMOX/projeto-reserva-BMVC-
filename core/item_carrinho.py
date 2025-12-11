class ItemCarrinho:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = int(quantidade)

    def calcular_subtotal(self):
        return self.produto.preco * self.quantidade
    
    def subtotal(self):
        return self.calcular_subtotal()

    def to_json(self):
        return {
            'produto_id': str(self.produto.id),
            'quantidade': self.quantidade
        }