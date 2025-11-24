# Arquivo: core/produto_fisico.py
from .produto import Produto

class ProdutoFisico(Produto):
    """Demonstra HERANÇA de Produto e POLIMORFISMO (Frete)."""
    def __init__(self, nome, preco, peso, imagem_url, categoria="Físico"):
        super().__init__(nome, preco, categoria)
        self.peso = peso
        self.imagem_url = imagem_url # NOVO ATRIBUTO

    def calcular_frete(self):
        """Implementação Polimórfica 1: Frete baseado no peso."""
        return 10.0 + (self.peso * 0.5) 

    def to_json(self):
        """Serializa o Produto, incluindo a URL da imagem."""
        data = super().to_json()
        data['peso'] = self.peso
        data['imagem_url'] = self.imagem_url
        return data
        
    @staticmethod
    def from_json(data):
        """Reconstrói a instância do ProdutoFisico."""
        return ProdutoFisico(
            data['nome'], 
            data['preco'], 
            data['peso'], 
            data['imagem_url'], 
            data['categoria']
        )