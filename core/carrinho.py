<<<<<<< HEAD
from datetime import datetime
from .item_carrinho import ItemCarrinho

class Carrinho:
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = []
        self.status = "ABERTO"
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def adicionar_item(self, item):
        for i in self.itens:
            if str(i.produto.id) == str(item.produto.id):
                i.quantidade += item.quantidade
                return
        self.itens.append(item)

    def calcular_total(self):
        total = 0.0
        for item in self.itens:
            if hasattr(item, 'calcular_subtotal'):
                total += item.calcular_subtotal()
            elif hasattr(item, 'subtotal'):
                total += item.subtotal()
        return total

    def finalizar_compra(self, forma_pagamento):
        if hasattr(forma_pagamento, 'processar'):
            forma_pagamento.processar()
        self.status = "PROCESSADO"
        return True

    def to_json(self):
        c_id = '1' 
        
        if hasattr(self.cliente, 'cpf'):
            c_id = self.cliente.cpf
        elif isinstance(self.cliente, dict):
            c_id = self.cliente.get('cpf', '1')
        elif isinstance(self.cliente, str):
            c_id = self.cliente

        return {
            'cliente_id': c_id,
=======
# Arquivo: core/carrinho.py
from datetime import datetime
from .cliente import Cliente
from .item_carrinho import ItemCarrinho
from pagamentos.pagamento import Pagamento 

class Carrinho:
    """Demonstra ASSOCIAÇÃO (Cliente) e COMPOSIÇÃO (ItemCarrinho)."""
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.itens = []      # Coleção que demonstra COMPOSIÇÃO
        self.status = "ABERTO"
        self.data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def adicionar_item(self, item: ItemCarrinho):
        """Método de Composição: anexa ItemCarrinho."""
        self.itens.append(item)

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def finalizar_compra(self, forma_pagamento: Pagamento):
        """
        Processa o pagamento usando POLIMORFISMO.
        O objeto 'forma_pagamento' pode ser Pix, Cartão ou Boleto.
        """
        forma_pagamento.processar()
        self.status = "PROCESSADO"

    # --- MÉTODOS DE SERIALIZAÇÃO JSON ---
    def to_json(self):
        """Salva o estado do carrinho."""
        return {
            'cliente_id': '1' if not hasattr(self.cliente, 'cpf') else self.cliente.cpf, # Simplificação para ID
            # Idealmente salvaríamos o ID real, aqui salvamos referência
>>>>>>> a5dc457 (docker do projeto pronto)
            'status': self.status,
            'data_criacao': self.data_criacao,
            'itens': [item.to_json() for item in self.itens]
        }

    @staticmethod
    def from_json(data, cliente_ref, produtos_db):
<<<<<<< HEAD
=======
        """
        Reconstrói o Carrinho.
        Precisa de referências externas (cliente e banco de produtos) para remontar os objetos.
        """
>>>>>>> a5dc457 (docker do projeto pronto)
        carrinho = Carrinho(cliente_ref)
        carrinho.status = data.get('status', 'ABERTO')
        carrinho.data_criacao = data.get('data_criacao', '')
        
        if 'itens' in data:
            for item_data in data['itens']:
                try:
<<<<<<< HEAD
                    pid = str(item_data.get('produto_id'))
                    produto_real = produtos_db.get(pid)
                    
                    if produto_real:
                        qtd = item_data.get('quantidade', 1)
                        novo_item = ItemCarrinho(produto_real, qtd)
                        carrinho.itens.append(novo_item)
                except Exception as e:
                    print(f"Erro ao recriar item do carrinho: {e}")
                    continue
        
=======
                    # ItemCarrinho.from_json precisa do dicionário de produtos para achar o objeto Produto
                    item = ItemCarrinho.from_json(item_data) 
                    # Nota: O ItemCarrinho.from_json original que fizemos buscava o produto dentro do próprio JSON do item.
                    # Se ele precisar buscar no DB geral, a lógica seria diferente. 
                    # Vamos assumir a versão que reconstrói o produto a partir dos dados salvos no item.
                    carrinho.itens.append(item)
                except Exception:
                    pass
>>>>>>> a5dc457 (docker do projeto pronto)
        return carrinho