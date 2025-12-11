import random

class QRCodeService:
<<<<<<< HEAD
    
    @staticmethod
    def gerar_qrcode(dados):
=======
    """
    Simula um serviço externo de geração de QR Codes.
    No mundo real, isso conectaria a uma API de banco.
    """
    @staticmethod
    def gerar_qrcode(dados):
        # Simula a criação de um hash único
>>>>>>> a5dc457 (docker do projeto pronto)
        hash_mock = f"{hash(dados)}{random.randint(1000, 9999)}"
        
        return {
            "qr_url": "https://via.placeholder.com/200x200.png?text=QR+Code+Pix",
            "code": f"00020126580014BR.GOV.BCB.PIX0136{hash_mock}5204000053039865802BR5913TechNovaStore6008Brasilia62070503***6304"
        }