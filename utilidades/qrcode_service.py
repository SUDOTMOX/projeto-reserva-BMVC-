# Arquivo: utilidades/qrcode_service.py

class QRCodeService:
    """Serviço Utilitário para Geração de QR Code (Demonstra Dependência)."""
    def gerar_qrcode(self, dados_pagamento: str):
        return f"QR_CODE_PIX_GERADO_PARA: {dados_pagamento[:30]}..."