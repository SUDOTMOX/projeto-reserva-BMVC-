import random

class QRCodeService:
    
    @staticmethod
    def gerar_qrcode(dados):
        hash_mock = f"{hash(dados)}{random.randint(1000, 9999)}"
        
        return {
            "qr_url": "https://via.placeholder.com/200x200.png?text=QR+Code+Pix",
            "code": f"00020126580014BR.GOV.BCB.PIX0136{hash_mock}5204000053039865802BR5913TechNovaStore6008Brasilia62070503***6304"
        }