# Arquivo: pagamentos/pagamento_boleto.py
from .pagamento import Pagamento

class PagamentoBoleto(Pagamento):
    """
    Implementação Polimórfica 3: Boleto Bancário.
    """
    def __init__(self, pedido):
        # O construtor agora deve aceitar 'pedido' para seguir o padrão das outras classes
        super().__init__(pedido)
    
    def processar(self):
        """Implementação: Lógica de geração de boleto."""
        # Usa o método calcular_total() do carrinho (pedido)
        valor = self.pedido.calcular_total()
        
        print(f"   [BOLETO] Gerando boleto de R$ {valor:.2f} com código de barras...")
        
        # Atualiza o status do pedido
        self.pedido.status = 'PROCESSADO'
        return True