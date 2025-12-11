# Arquivo: pagamentos/pagamento_boleto.py
from .pagamento import Pagamento

class PagamentoBoleto(Pagamento):
    """Implementação Polimórfica 3."""
    def __init__(self, valor=0.0):
        super().__init__(valor)
    
    def processar(self):
        """Implementação: Lógica de geração de boleto."""
        print(f"   Boleto de R$ {self.valor:.2f} gerado com código de barras.")