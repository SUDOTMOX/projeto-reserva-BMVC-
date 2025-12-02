# Arquivo: pagamentos/pagamento_boleto.py
from .pagamento import Pagamento

class PagamentoBoleto(Pagamento):
<<<<<<< HEAD
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
=======
    """Implementação Polimórfica 3."""
    def __init__(self, valor=0.0):
        super().__init__(valor)
    
    def processar(self):
        """Implementação: Lógica de geração de boleto."""
        print(f"   Boleto de R$ {self.valor:.2f} gerado com código de barras.")
>>>>>>> 23b8098d47510088389386ce7bf5abf320cf4207
