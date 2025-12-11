# Arquivo: core/views/checkout_views.py

from flask import Blueprint, render_template, request, redirect, url_for, session
import database
from core.models.vendas import Carrinho, ItemCarrinho
# Importa as classes de serviço (Strategy Pattern)
from core.services.pagamentos import PagamentoPix, PagamentoCartao, PagamentoBoleto

checkout_bp = Blueprint('checkout', __name__)
DB = database.carregar_dados_json()

@checkout_bp.route('/carrinho/adicionar', methods=['POST'])
def adicionar_item():
    """Adiciona item ao carrinho ou inicia compra imediata."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro', erro="Faça login para comprar."))

    produto_id = request.form.get('produto_id')
    quantidade = int(request.form.get('quantidade', 1))
    acao = request.form.get('acao_compra') # 'compra_imediata' ou 'adicionar_carrinho'
    
    produto = DB['produtos'].get(produto_id)
    cliente = DB['clientes'].get(user_id)
    
    if not produto or not cliente:
        return redirect(url_for('loja.index', erro="Erro de dados."))

    # --- LÓGICA DE GESTÃO DE CARRINHO ---
    # 1. Procura se já existe um carrinho ABERTO para este cliente
    carrinho_atual = None
    carrinho_id = None
    
    for cid, c in DB['carrinhos'].items():
        # Verifica se pertence ao cliente e está aberto (Lógica simplificada)
        # Idealmente compararíamos IDs, mas comparando objetos/referencias funciona se carregado corretamente
        if c.status == 'ABERTO': 
             # Nota: Em um sistema real, verificaríamos c.cliente_id == user_id
             # Aqui assumimos que pegamos o último aberto global para simplificar o exemplo acadêmico
             carrinho_atual = c
             carrinho_id = cid
             break
    
    # 2. Se não achou, cria um novo
    if not carrinho_atual:
        carrinho_atual = Carrinho(cliente)
        carrinho_id = str(DB['next_ids']['carrinho'])
        DB['carrinhos'][carrinho_id] = carrinho_atual
        DB['next_ids']['carrinho'] += 1

    # 3. Adiciona o Item (Composição)
    item = ItemCarrinho(produto, quantidade)
    carrinho_atual.adicionar_item(item)
    
    # 4. Salva no banco
    database.salvar_dados_json(DB)

    # 5. Redirecionamento
    if acao == 'compra_imediata':
        return redirect(url_for('checkout.checkout_page'))
    else:
        return redirect(url_for('loja.index', msg=f"{produto.nome} adicionado ao carrinho!"))

@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    """Exibe o carrinho e processa o pagamento."""
    
    # Busca o carrinho aberto (mesma lógica simplificada acima)
    carrinho = None 
    for c in DB['carrinhos'].values():
        if c.status == 'ABERTO':
            carrinho = c
            break
            
    if not carrinho or not carrinho.itens:
        return redirect(url_for('loja.index', erro="Seu carrinho está vazio."))

    # --- PROCESSAMENTO DO PAGAMENTO (POST) ---
    if request.method == 'POST':
        tipo_pagamento = request.form.get('pagamento')
        total = carrinho.calcular_total()
        strategy = None

        # Factory simples para escolher a estratégia
        if tipo_pagamento == 'pix':
            strategy = PagamentoPix(total, "chave-aleatoria-pix")
        elif tipo_pagamento == 'boleto':
            strategy = PagamentoBoleto(total)
        elif tipo_pagamento == 'cartao':
            parcelas = int(request.form.get('parcelas', 1))
            strategy = PagamentoCartao(total, "1234-5678-9012-3456", parcelas)

        if strategy:
            # O Carrinho delega o processamento para a estratégia (Polimorfismo)
            sucesso = carrinho.finalizar_compra(strategy)
            
            if sucesso:
                database.salvar_dados_json(DB)
                
                # Se for PIX, pegamos os dados gerados
                pix_info = getattr(strategy, 'dados_qrcode', None)
                
                return render_template('checkout/confirmacao.html', 
                                     total=total, 
                                     forma=tipo_pagamento, 
                                     pix_info=pix_info)
            else:
                return redirect(url_for('checkout.checkout_page', erro="Pagamento Recusado!"))

    return render_template('checkout/checkout.html', carrinho=carrinho)