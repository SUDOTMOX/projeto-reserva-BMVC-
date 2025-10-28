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