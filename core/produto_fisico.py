<<<<<<< HEAD
from .produto import Produto
from .avaliacao import Avaliacao 
class ProdutoFisico(Produto):
=======
# Arquivo: core/produto_fisico.py
from .produto import Produto
from .avaliacao import Avaliacao # Certifique-se de ter este import se usar avaliações

class ProdutoFisico(Produto):
    """Demonstra HERANÇA de Produto e POLIMORFISMO (Frete)."""
>>>>>>> a5dc457 (docker do projeto pronto)
    def __init__(self, nome, preco, peso, imagem_url, categoria="Físico"):
        super().__init__(nome, preco, categoria)
        self.peso = peso
        self.imagem_url = imagem_url 
<<<<<<< HEAD
        self.avaliacoes = [] 

    def calcular_frete(self):
        return 10.0 + (self.peso * 0.5) 
    
    def adicionar_avaliacao(self, avaliacao: Avaliacao):
=======
        self.avaliacoes = [] # Lista para armazenar objetos Avaliacao (Associação)

    def calcular_frete(self):
        """Implementação Polimórfica: Frete baseado no peso."""
        return 10.0 + (self.peso * 0.5) 
    
    def adicionar_avaliacao(self, avaliacao: Avaliacao):
        """Adiciona uma avaliação ao produto."""
>>>>>>> a5dc457 (docker do projeto pronto)
        self.avaliacoes.append(avaliacao)

    def calcular_media_avaliacoes(self):
        if not self.avaliacoes:
            return 0
        total = sum(a.nota for a in self.avaliacoes)
        return total / len(self.avaliacoes)

    def to_json(self):
<<<<<<< HEAD
=======
        """Serializa o Produto, incluindo a URL da imagem e avaliações."""
>>>>>>> a5dc457 (docker do projeto pronto)
        data = super().to_json()
        data['peso'] = self.peso
        data['imagem_url'] = self.imagem_url
        data['avaliacoes'] = [a.to_json() for a in self.avaliacoes]
        return data
        
    @staticmethod
    def from_json(data):
<<<<<<< HEAD
=======
        """Reconstrói a instância do ProdutoFisico."""
>>>>>>> a5dc457 (docker do projeto pronto)
        prod = ProdutoFisico(
            data['nome'], 
            data['preco'], 
            data['peso'], 
            data['imagem_url'], 
            data['categoria']
        )
<<<<<<< HEAD
=======
        # Reconstrói as avaliações se existirem
>>>>>>> a5dc457 (docker do projeto pronto)
        if 'avaliacoes' in data:
            for av_data in data['avaliacoes']:
                try:
                    prod.adicionar_avaliacao(Avaliacao.from_json(av_data))
                except:
<<<<<<< HEAD
                    pass 
=======
                    pass # Ignora avaliações malformadas
>>>>>>> a5dc457 (docker do projeto pronto)
        return prod