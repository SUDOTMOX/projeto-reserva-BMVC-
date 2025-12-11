from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from .utils import QRCodeService  

class Pagamento(ABC):
   
    def __init__(self, valor):
        self.valor = valor
        self.data_pagamento = datetime.now()
        self.status = "PENDENTE"

    @abstractmethod
    def processar(self):
       
        pass
    
    def to_json(self):
       
        return {
            'tipo': self.__class__.__name__,
            'valor': self.valor,
            'status': self.status,
            'data': self.data_pagamento.strftime("%Y-%m-%d %H:%M:%S")
        }


class PagamentoPix(Pagamento):
    def __init__(self, valor, chave_pix):
        super().__init__(valor)
        self.chave_pix = chave_pix
        self.dados_qrcode = None

    def processar(self):
        print(f"[LOG] Processando PIX de R${self.valor:.2f} para chave {self.chave_pix}...")
        
        self.dados_qrcode = QRCodeService.gerar_qrcode(f"{self.chave_pix}-{self.valor}")
        self.status = "APROVADO"
        return True
    
    def to_json(self):
        data = super().to_json()
        data['chave_pix'] = self.chave_pix
        data['qr_info'] = self.dados_qrcode
        return data


class PagamentoCartao(Pagamento):
    def __init__(self, valor, num_cartao, parcelas=1):
        super().__init__(valor)
        self.num_cartao = num_cartao 
        self.parcelas = parcelas

    def processar(self):
        print(f"[LOG] Processando Cartão {self.num_cartao} em {self.parcelas}x...")
        
        if self.parcelas > 12:
            self.status = "RECUSADO"
            return False
            
        self.status = "APROVADO"
        return True
    
    def to_json(self):
        data = super().to_json()
        data['parcelas'] = self.parcelas
        data['cartao_final'] = self.num_cartao[-4:] 
        return data


class PagamentoBoleto(Pagamento):
    def processar(self):
        print(f"[LOG] Gerando Boleto de R${self.valor:.2f}...")
        
        self.vencimento = self.data_pagamento + timedelta(days=3)
        self.codigo_barras = "34191.79001 01043.510047 91020.150008 1 899900000" + str(int(self.valor))
        
        self.status = "AGUARDANDO_PAGAMENTO"
        return True

    def to_json(self):
        data = super().to_json()
        data['codigo_barras'] = getattr(self, 'codigo_barras', '')
        return data