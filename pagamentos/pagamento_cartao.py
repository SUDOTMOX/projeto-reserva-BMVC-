# Arquivo: pagamentos/pagamento_cartao.py
from .pagamento import Pagamento

class PagamentoCartao(Pagamento):
    """Implementação Polimórfica 1."""
    def __init__(self, valor=0.0, num_cartao=""):
        super().__init__(valor)
        self.num_cartao = num_cartao
    
    def processar(self):
        """Implementação: Lógica de autorização de cartão."""
        print(f"   Processando R$ {self.valor:.2f} via Cartão.")