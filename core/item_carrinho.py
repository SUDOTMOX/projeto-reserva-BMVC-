<<<<<<< HEAD
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
=======
# Arquivo: core/item_carrinho.py

from .produto_fisico import ProdutoFisico # Importação deve ser do ProdutoFisico

class ItemCarrinho:
    """Classe Parte na COMPOSIÇÃO."""
    def __init__(self, produto: ProdutoFisico, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade
    
    def calcular_subtotal(self):
        return self.produto.preco * self.quantidade
    

    def to_json(self):
        return {'produto_data': self.produto.to_json(), 'quantidade': self.quantidade}
    
    @staticmethod
    def from_json(data):
        produto_obj = ProdutoFisico.from_json(data['produto_data'])
        return ItemCarrinho(produto_obj, data['quantidade'])
>>>>>>> a5dc457 (docker do projeto pronto)
