<<<<<<< HEAD
from .pagamento import Pagamento

class PagamentoBoleto(Pagamento):
=======
# Arquivo: pagamentos/pagamento_boleto.py
from .pagamento import Pagamento

class PagamentoBoleto(Pagamento):
    """Implementação Polimórfica 3."""
>>>>>>> a5dc457 (docker do projeto pronto)
    def __init__(self, valor=0.0):
        super().__init__(valor)
    
    def processar(self):
<<<<<<< HEAD
=======
        """Implementação: Lógica de geração de boleto."""
>>>>>>> a5dc457 (docker do projeto pronto)
        print(f"   Boleto de R$ {self.valor:.2f} gerado com código de barras.")