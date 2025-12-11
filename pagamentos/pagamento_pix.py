from .pagamento import Pagamento


try:
    from core.services.utils import QRCodeService
except ImportError:
    import sys
    sys.path.append('.') 
    from utils import QRCodeService 

class PagamentoPix(Pagamento):
    def __init__(self, valor=0.0, chave_pix=""):
        super().__init__(valor)
        self.chave_pix = chave_pix

    def processar(self):
        servico = QRCodeService() 
        codigo_pix = servico.gerar_qrcode(f"Valor:{self.valor}|Chave:{self.chave_pix}")
        
        print(f"   Processando R$ {self.valor:.2f} via PIX.")