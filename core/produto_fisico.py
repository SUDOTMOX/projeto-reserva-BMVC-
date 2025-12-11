from .produto import Produto
from .avaliacao import Avaliacao 
class ProdutoFisico(Produto):
    def __init__(self, nome, preco, peso, imagem_url, categoria="Físico"):
        super().__init__(nome, preco, categoria)
        self.peso = peso
        self.imagem_url = imagem_url 
        self.avaliacoes = [] 

    def calcular_frete(self):
        return 10.0 + (self.peso * 0.5) 
    
    def adicionar_avaliacao(self, avaliacao: Avaliacao):
        self.avaliacoes.append(avaliacao)

    def calcular_media_avaliacoes(self):
        if not self.avaliacoes:
            return 0
        total = sum(a.nota for a in self.avaliacoes)
        return total / len(self.avaliacoes)

    def to_json(self):
        data = super().to_json()
        data['peso'] = self.peso
        data['imagem_url'] = self.imagem_url
        data['avaliacoes'] = [a.to_json() for a in self.avaliacoes]
        return data
        
    @staticmethod
    def from_json(data):
        prod = ProdutoFisico(
            data['nome'], 
            data['preco'], 
            data['peso'], 
            data['imagem_url'], 
            data['categoria']
        )
        if 'avaliacoes' in data:
            for av_data in data['avaliacoes']:
                try:
                    prod.adicionar_avaliacao(Avaliacao.from_json(av_data))
                except:
                    pass 
        return prod