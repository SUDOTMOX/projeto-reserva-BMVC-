<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for, session
import database
from core.carrinho import Carrinho
from core.item_carrinho import ItemCarrinho
from pagamentos.pagamento_pix import PagamentoPix
from pagamentos.pagamento_cartao import PagamentoCartao
from pagamentos.pagamento_boleto import PagamentoBoleto
from core.extensions import socketio

checkout_bp = Blueprint('checkout', __name__)

def eh_o_mesmo_cliente(carrinho, cliente_logado):
    """
    Função Helper BLINDADA: Compara CPFs aceitando Objeto, Dict ou String.
    """
    cpf_carrinho = None
    
    # 1. Se for Objeto Cliente (tem atributo cpf)
    if hasattr(carrinho.cliente, 'cpf'):
        cpf_carrinho = carrinho.cliente.cpf
    
    # 2. Se for Dicionário (recuperado do JSON cru)
    elif isinstance(carrinho.cliente, dict):
        cpf_carrinho = carrinho.cliente.get('cpf')
        
    # 3. Se for apenas String (o ID/CPF salvo diretamente)
    else:
        cpf_carrinho = str(carrinho.cliente)

    # Compara strings limpas
    return str(cpf_carrinho).strip() == str(cliente_logado.cpf).strip()

@checkout_bp.route('/carrinho/adicionar', methods=['POST'])
def adicionar_item():
    DB = database.carregar_dados_json()
    
=======
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
>>>>>>> a5dc457 (docker do projeto pronto)
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro', erro="Faça login para comprar."))

    produto_id = request.form.get('produto_id')
    quantidade = int(request.form.get('quantidade', 1))
<<<<<<< HEAD
    acao = request.form.get('acao_compra') 
=======
    acao = request.form.get('acao_compra') # 'compra_imediata' ou 'adicionar_carrinho'
>>>>>>> a5dc457 (docker do projeto pronto)
    
    produto = DB['produtos'].get(produto_id)
    cliente = DB['clientes'].get(user_id)
    
    if not produto or not cliente:
        return redirect(url_for('loja.index', erro="Erro de dados."))

<<<<<<< HEAD
    # --- Lógica de Busca ---
=======
    # --- LÓGICA DE GESTÃO DE CARRINHO ---
    # 1. Procura se já existe um carrinho ABERTO para este cliente
>>>>>>> a5dc457 (docker do projeto pronto)
    carrinho_atual = None
    carrinho_id = None
    
    for cid, c in DB['carrinhos'].items():
<<<<<<< HEAD
        # Verifica status de forma segura
        status_safe = getattr(c, 'status', 'FECHADO')
        if isinstance(c, dict): status_safe = c.get('status', 'FECHADO')

        if eh_o_mesmo_cliente(c, cliente) and str(status_safe) == 'ABERTO':
             carrinho_atual = c
             carrinho_id = cid
             break

    if not carrinho_atual:
        carrinho_atual = Carrinho(cliente)
        carrinho_atual.status = 'ABERTO'
=======
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
>>>>>>> a5dc457 (docker do projeto pronto)
        carrinho_id = str(DB['next_ids']['carrinho'])
        DB['carrinhos'][carrinho_id] = carrinho_atual
        DB['next_ids']['carrinho'] += 1

<<<<<<< HEAD
    # Garante que é um objeto Carrinho antes de adicionar
    if not isinstance(carrinho_atual, Carrinho):
         # Se por acaso o DB retornou um dict, precisamos recriar o objeto (caso raro aqui, mas seguro)
         # Nota: Isso depende da implementação do database.py, mas vamos assumir que ele devolve objetos
         pass 

    item = ItemCarrinho(produto, quantidade)
    carrinho_atual.adicionar_item(item)
    
    database.salvar_dados_json(DB)

=======
    # 3. Adiciona o Item (Composição)
    item = ItemCarrinho(produto, quantidade)
    carrinho_atual.adicionar_item(item)
    
    # 4. Salva no banco
    database.salvar_dados_json(DB)

    # 5. Redirecionamento
>>>>>>> a5dc457 (docker do projeto pronto)
    if acao == 'compra_imediata':
        return redirect(url_for('checkout.checkout_page'))
    else:
        return redirect(url_for('loja.index', msg=f"{produto.nome} adicionado ao carrinho!"))

@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
<<<<<<< HEAD
    DB = database.carregar_dados_json()
    
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro'))
    
    cliente = DB['clientes'].get(user_id)
    if not cliente:
        session.clear()
        return redirect(url_for('auth.login_cadastro'))

    carrinho = None
    
    # --- Busca o carrinho do cliente ---
    for c in DB['carrinhos'].values():
        status_safe = getattr(c, 'status', 'FECHADO')
        if isinstance(c, dict): status_safe = c.get('status', 'FECHADO')

        if eh_o_mesmo_cliente(c, cliente) and str(status_safe) == 'ABERTO':
            carrinho = c
            break
            
    # Verifica se achou e se tem itens
    if not carrinho or not carrinho.itens:
        # Debug: Tire o comentário abaixo se ainda der erro para ver no terminal o que está acontecendo
        # print(f"DEBUG: Cliente {cliente.cpf}. Carrinho encontrado: {carrinho}")
        return redirect(url_for('loja.index', erro="Seu carrinho está vazio."))

=======
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
>>>>>>> a5dc457 (docker do projeto pronto)
    if request.method == 'POST':
        tipo_pagamento = request.form.get('pagamento')
        total = carrinho.calcular_total()
        strategy = None
<<<<<<< HEAD
        pix_info = None

        if tipo_pagamento == 'pix':
            strategy = PagamentoPix(total, "UNB.PIX@000")
            pix_info = {
                'code': "0002012636...",
                'qr_url': 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + str(total)
            }
=======

        # Factory simples para escolher a estratégia
        if tipo_pagamento == 'pix':
            strategy = PagamentoPix(total, "chave-aleatoria-pix")
>>>>>>> a5dc457 (docker do projeto pronto)
        elif tipo_pagamento == 'boleto':
            strategy = PagamentoBoleto(total)
        elif tipo_pagamento == 'cartao':
            parcelas = int(request.form.get('parcelas', 1))
<<<<<<< HEAD
            strategy = PagamentoCartao(total, "1234-5678...", parcelas)

        if strategy:
            carrinho.finalizar_compra(strategy)
            database.salvar_dados_json(DB)
            
            socketio.emit('nova_venda', {
                'msg': f'Novo pedido de R$ {total:.2f} realizado!',
                'cliente': carrinho.cliente.nome if hasattr(carrinho.cliente, 'nome') else "Cliente"
            })
            
            return render_template('checkout/confirmacao.html', 
                                   total=total, 
                                   forma=tipo_pagamento, 
                                   pix_info=pix_info)
        else:
            return redirect(url_for('checkout.checkout_page', erro="Pagamento Recusado!"))
=======
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
>>>>>>> a5dc457 (docker do projeto pronto)

    return render_template('checkout/checkout.html', carrinho=carrinho)