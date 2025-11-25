# Arquivo: core/models/produtos.py
from abc import ABC, abstractmethod

class Produto(ABC):
    """Classe Base Abstrata para Produtos."""
    def __init__(self, id, nome, preco, descricao, categoria="Geral"):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria
        self.imagem_url = "" # Atributo opcional

    @abstractmethod
    def calcular_frete(self):
        pass

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome, 
            'preco': self.preco, 
            'descricao': self.descricao,
            'categoria': self.categoria,
            'imagem_url': self.imagem_url
        }

class ProdutoFisico(Produto):
    """Produto Tangível com peso e dimensões."""
    def __init__(self, id, nome, preco, descricao, peso, dimensoes, categoria="Físico"):
        super().__init__(id, nome, preco, descricao, categoria)
        self.peso = peso
        self.dimensoes = dimensoes

    def calcular_frete(self):
        """Frete baseado no peso (Polimorfismo)."""
        return 15.0 + (self.peso * 2.5)

    def to_json(self):
        data = super().to_json()
        data['peso'] = self.peso
        data['dimensoes'] = self.dimensoes
        return data

class Avaliacao:
    """Classe simples para avaliações (opcional)."""
    def __init__(self, cliente_nome, nota, comentario):
        self.cliente_nome = cliente_nome
        self.nota = nota
        self.comentario = comentario