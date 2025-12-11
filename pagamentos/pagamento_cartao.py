# Arquivo: pagamentos/pagamento_cartao.py
from .pagamento import Pagamento

class PagamentoCartao(Pagamento):
<<<<<<< HEAD
=======
    """Implementação Polimórfica 1."""
>>>>>>> a5dc457 (docker do projeto pronto)
    def __init__(self, valor=0.0, num_cartao="", parcelas=1):
        super().__init__(valor)
        self.num_cartao = num_cartao
        self.parcelas = parcelas
    
    def processar(self):
<<<<<<< HEAD
=======
        """Implementação: Lógica de autorização de cartão."""
>>>>>>> a5dc457 (docker do projeto pronto)
        print(f"   Processando R$ {self.valor:.2f} via Cartão em {self.parcelas}x.")