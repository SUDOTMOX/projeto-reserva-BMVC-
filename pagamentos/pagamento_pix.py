from .pagamento import Pagamento
# Se você não tiver o arquivo utilidades/qrcode_service.py, 
# remova a importação e use a lógica comentada abaixo.
from utilidades.qrcode_service import QRCodeService 

class PagamentoPix(Pagamento):
    """Implementação Polimórfica 2."""
    def __init__(self, pedido, chave_pix=""):
        super().__init__(pedido)
        self.chave_pix = chave_pix

    def processar(self):
        """Implementação: Simula geração de QR Code."""
        valor = self.pedido.calcular_total()
        
        # Gera o código (Simulado ou via Serviço)
        servico = QRCodeService()
        dados_pix = f"Valor:{valor}|Chave:{self.chave_pix}"
        codigo_pix = servico.gerar_qrcode(dados_pix)
        
        print(f"   Processando R$ {valor:.2f} via PIX.")
        print(f"   -> QR Code gerado: {codigo_pix}")
        
        # Simula pagamento instantâneo para o projeto
        self.pedido.status = 'PROCESSADO'
        return True