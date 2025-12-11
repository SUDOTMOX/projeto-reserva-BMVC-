from .pagamento import Pagamento

class PagamentoBoleto(Pagamento):
    def __init__(self, valor=0.0):
        super().__init__(valor)
    
    def processar(self):
        print(f"   Boleto de R$ {self.valor:.2f} gerado com código de barras.")