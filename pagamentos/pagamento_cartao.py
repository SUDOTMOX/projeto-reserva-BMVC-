from .pagamento import Pagamento

class PagamentoCartao(Pagamento):
    """
    Implementação Polimórfica 1: Pagamento com Cartão.
    Encapsula a lógica de simulação de autorização de cartão.
    """
    def __init__(self, pedido, num_cartao="", parcelas=1):
        # Passa o objeto Pedido para a classe mãe
        super().__init__(pedido) 
        self.num_cartao = num_cartao
        self.parcelas = parcelas
    
    def processar(self):
        """
        Implementação: Lógica de simulação de autorização.
        Retorna True para sucesso e False para falha.
        """
        # CORREÇÃO: Usa o método .calcular_total() em vez de atributo .valor_total
        valor = self.pedido.calcular_total()
        
        print(f"   Iniciando processamento de R$ {valor:.2f} via Cartão ({self.num_cartao}) em {self.parcelas}x.")
        
        # --- LÓGICA DE SIMULAÇÃO ---
        
        if not self.num_cartao or len(self.num_cartao) < 4:
            print("   ERRO: Número de cartão inválido.")
            return False

        # Regra de mentira:
        # Cartões VISA (começam com '4') aprovam.
        # Qualquer outro recusa.
        
        if self.num_cartao.startswith('4'):
            print("   SIMULAÇÃO: Cartão Visa... APROVADO.")
            # Colaboração de Objetos: O Pagamento atualiza o status do pedido
            self.pedido.status = 'PROCESSADO' 
            return True
            
        elif self.num_cartao.startswith('5'):
            print("   SIMULAÇÃO: Cartão Master... RECUSADO.")
            return False
            
        else:
            print("   SIMULAÇÃO: Cartão desconhecido... ERRO.")
            return False