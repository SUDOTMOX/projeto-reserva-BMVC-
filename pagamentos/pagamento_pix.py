<<<<<<< HEAD
from .pagamento import Pagamento


try:
    from core.services.utils import QRCodeService
except ImportError:
    import sys
    sys.path.append('.') 
    from utils import QRCodeService 

class PagamentoPix(Pagamento):
=======
# Arquivo: pagamentos/pagamento_pix.py
from .pagamento import Pagamento
from utilidades.qrcode_service import QRCodeService 

class PagamentoPix(Pagamento):
    """Implementação Polimórfica 2."""
>>>>>>> a5dc457 (docker do projeto pronto)
    def __init__(self, valor=0.0, chave_pix=""):
        super().__init__(valor)
        self.chave_pix = chave_pix

    def processar(self):
<<<<<<< HEAD
        servico = QRCodeService() 
        codigo_pix = servico.gerar_qrcode(f"Valor:{self.valor}|Chave:{self.chave_pix}")
        
        print(f"   Processando R$ {self.valor:.2f} via PIX.")
=======
        """Implementação: Usa o QRCodeService (Demonstra DEPENDÊNCIA)."""
        servico = QRCodeService() 
        codigo_pix = servico.gerar_qrcode(f"Valor:{self.valor}|Chave:{self.chave_pix}")
        
        print(f"   Processando R$ {self.valor:.2f} via PIX.")
        # print(f"   -> QR Code gerado: {codigo_pix}")
>>>>>>> a5dc457 (docker do projeto pronto)
