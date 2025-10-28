# Arquivo: pagamentos/pagamento_pix.py
from .pagamento import Pagamento
from utilidades.qrcode_service import QRCodeService # IMPORTAÇÃO EXTERNA (Dependência)

class PagamentoPix(Pagamento):
    """Implementação Polimórfica 2."""
    def __init__(self, valor=0.0, chave_pix=""):
        super().__init__(valor)
        self.chave_pix = chave_pix

    def processar(self):
        """Implementação: Usa o QRCodeService (Demonstra DEPENDÊNCIA)."""
        servico = QRCodeService() 
        codigo_pix = servico.gerar_qrcode(f"Valor:{self.valor}|Chave:{self.chave_pix}")
        
        print(f"   Processando R$ {self.valor:.2f} via PIX.")
        print(f"   -> **DEPENDÊNCIA**: QR Code gerado: {codigo_pix}")