from abc import ABC, abstractmethod
from datetime import datetime, timedelta
<<<<<<< HEAD
from .utils import QRCodeService  

class Pagamento(ABC):
   
=======
from .utils import QRCodeService  # Importação relativa dentro do pacote services

class Pagamento(ABC):
    """
    Classe Abstrata (Strategy Base).
    Define o contrato 'processar' que todas as formas de pagamento devem seguir.
    """
>>>>>>> a5dc457 (docker do projeto pronto)
    def __init__(self, valor):
        self.valor = valor
        self.data_pagamento = datetime.now()
        self.status = "PENDENTE"

    @abstractmethod
    def processar(self):
<<<<<<< HEAD
       
        pass
    
    def to_json(self):
       
=======
        """Método polimórfico: cada filha implementa de um jeito."""
        pass
    
    def to_json(self):
        """Serialização comum a todos os pagamentos."""
>>>>>>> a5dc457 (docker do projeto pronto)
        return {
            'tipo': self.__class__.__name__,
            'valor': self.valor,
            'status': self.status,
            'data': self.data_pagamento.strftime("%Y-%m-%d %H:%M:%S")
        }

<<<<<<< HEAD
=======
# --- IMPLEMENTAÇÕES CONCRETAS (Estratégias) ---
>>>>>>> a5dc457 (docker do projeto pronto)

class PagamentoPix(Pagamento):
    def __init__(self, valor, chave_pix):
        super().__init__(valor)
        self.chave_pix = chave_pix
        self.dados_qrcode = None

    def processar(self):
<<<<<<< HEAD
        print(f"[LOG] Processando PIX de R${self.valor:.2f} para chave {self.chave_pix}...")
        
        self.dados_qrcode = QRCodeService.gerar_qrcode(f"{self.chave_pix}-{self.valor}")
        self.status = "APROVADO"
        return True
    
    def to_json(self):
=======
        """Lógica específica do PIX: Gera QR Code."""
        print(f"[LOG] Processando PIX de R${self.valor:.2f} para chave {self.chave_pix}...")
        
        # Uso de dependência (QRCodeService)
        self.dados_qrcode = QRCodeService.gerar_qrcode(f"{self.chave_pix}-{self.valor}")
        self.status = "APROVADO" # Simulação de aprovação imediata
        return True
    
    def to_json(self):
        """Sobrescrita para incluir dados do QR Code no JSON."""
>>>>>>> a5dc457 (docker do projeto pronto)
        data = super().to_json()
        data['chave_pix'] = self.chave_pix
        data['qr_info'] = self.dados_qrcode
        return data


class PagamentoCartao(Pagamento):
    def __init__(self, valor, num_cartao, parcelas=1):
        super().__init__(valor)
<<<<<<< HEAD
        self.num_cartao = num_cartao 
        self.parcelas = parcelas

    def processar(self):
        print(f"[LOG] Processando Cartão {self.num_cartao} em {self.parcelas}x...")
        
=======
        self.num_cartao = num_cartao # Em produção, nunca salve o cartão real!
        self.parcelas = parcelas

    def processar(self):
        """Lógica específica do Cartão: Valida limite e parcelas."""
        print(f"[LOG] Processando Cartão {self.num_cartao} em {self.parcelas}x...")
        
        # Simula comunicação com gateway (Cielo, Stripe, etc)
>>>>>>> a5dc457 (docker do projeto pronto)
        if self.parcelas > 12:
            self.status = "RECUSADO"
            return False
            
        self.status = "APROVADO"
        return True
    
    def to_json(self):
        data = super().to_json()
        data['parcelas'] = self.parcelas
<<<<<<< HEAD
        data['cartao_final'] = self.num_cartao[-4:] 
=======
        data['cartao_final'] = self.num_cartao[-4:] # Salva só o final por segurança
>>>>>>> a5dc457 (docker do projeto pronto)
        return data


class PagamentoBoleto(Pagamento):
    def processar(self):
<<<<<<< HEAD
=======
        """Lógica específica do Boleto: Gera código de barras e data de vencimento."""
>>>>>>> a5dc457 (docker do projeto pronto)
        print(f"[LOG] Gerando Boleto de R${self.valor:.2f}...")
        
        self.vencimento = self.data_pagamento + timedelta(days=3)
        self.codigo_barras = "34191.79001 01043.510047 91020.150008 1 899900000" + str(int(self.valor))
        
        self.status = "AGUARDANDO_PAGAMENTO"
        return True

    def to_json(self):
        data = super().to_json()
        data['codigo_barras'] = getattr(self, 'codigo_barras', '')
        return data