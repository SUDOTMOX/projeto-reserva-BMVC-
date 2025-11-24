# Arquivo: app_web.py - Servidor Flask (VERSÃO FINAL: CRUD + REMOVER ITEM + MENU)

from flask import Flask, render_template, request, redirect, url_for, session
import database 
from core.cliente import Cliente 
from core.carrinho import Carrinho
from core.item_carrinho import ItemCarrinho
from core.produto_fisico import ProdutoFisico

# Classes de pagamento
from pagamentos.pagamento_pix import PagamentoPix
from pagamentos.pagamento_cartao import PagamentoCartao
from pagamentos.pagamento_boleto import PagamentoBoleto

import os
from pathlib import Path
import sys
from datetime import timedelta 

# --- INICIALIZAÇÃO ---
basedir = Path(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, template_folder=str(basedir / 'templates'))

app.secret_key = 'chave_muito_secreta_para_oo_unb' 
app.permanent_session_lifetime = timedelta(minutes=30)
app.config.update(SESSION_PERMANENT=True)
sys.path.append(str(basedir))

# CARREGA BANCO DE DADOS
DB = database.carregar_dados_json()
Cliente.db_ref = DB['clientes'] 

def get_current_user():
    user_id = session.get('user_id')
    return DB['clientes'].get(user_id) if user_id else None


# ==============================================================================
#  1. CRUD DE PRODUTOS (ADMINISTRAÇÃO)
# ==============================================================================

@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'): return redirect(url_for('index')) 
    return render_template('admin_dashboard.html', 
                           clientes=DB['clientes'].items(),
                           produtos=DB['produtos'].items())

@app.route('/admin/criar', methods=['GET', 'POST'])
def admin_criar_produto():
    if not session.get('is_admin'): return redirect(url_for('index'))

    if request.method == 'POST':
        novo_produto = ProdutoFisico(
            nome=request.form['nome'],
            preco=float(request.form['preco']),
            peso=float(request.form['peso']),
            imagem_url=request.form['imagem_url'],
            categoria=request.form['categoria']
        )
        novo_id = str(DB['next_ids']['produto'])
        DB['produtos'][novo_id] = novo_produto
        DB['next_ids']['produto'] += 1
        database.salvar_dados_json(DB)
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_editar_produto.html', produto=None, pid=None)

@app.route('/admin/editar/<pid>', methods=['GET', 'POST'])
def admin_editar_produto(pid):
    if not session.get('is_admin'): return redirect(url_for('index')) 
    produto = DB['produtos'].get(pid)
    if not produto: return "Produto não encontrado.", 404

    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.preco = float(request.form['preco'])
        produto.categoria = request.form['categoria']
        produto.imagem_url = request.form['imagem_url']
        produto.peso = float(request.form['peso'])
        database.salvar_dados_json(DB)
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin_editar_produto.html', produto=produto, pid=pid)

@app.route('/admin/deletar/<pid>')
def admin_deletar_produto(pid):
    if not session.get('is_admin'): return redirect(url_for('index'))
    if pid in DB['produtos']:
        del DB['produtos'][pid]
        database.salvar_dados_json(DB)
    return redirect(url_for('admin_dashboard'))


# ==============================================================================
#  2. CHECKOUT E PAGAMENTOS
# ==============================================================================

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_web():
    carrinho_keys = [int(k) for k in DB['carrinhos'].keys()]
    carrinho_id = max(carrinho_keys) if carrinho_keys else None
    ultimo_carrinho = DB['carrinhos'].get(str(carrinho_id))
    
    if not ultimo_carrinho or ultimo_carrinho.calcular_total() == 0 or ultimo_carrinho.status == "PROCESSADO":
        return redirect(url_for('index', erro_carrinho="Carrinho vazio ou já processado!"))

    if request.method == 'POST':
        forma_escolhida = request.form.get('pagamento')
        parcelas = request.form.get('parcelas', type=int)
        forma_pagamento = None
        pix_info = None

        if forma_escolhida == 'pix':
            forma_pagamento = PagamentoPix(ultimo_carrinho, "LOJA.UNB@PIX")
            pix_info = {
                'code': "00020126360014BR.GOV.BCB.PIX...",
                'qr_url': f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={ultimo_carrinho.calcular_total()}"
            }
        elif forma_escolhida == 'cartao':
            num_cartao = request.form.get('num_cartao', '**** 4444')
            forma_pagamento = PagamentoCartao(ultimo_carrinho, num_cartao, parcelas=parcelas)
        elif forma_escolhida == 'boleto':
            forma_pagamento = PagamentoBoleto(ultimo_carrinho)
        else:
            return redirect(url_for('index'))

        sucesso = ultimo_carrinho.finalizar_compra(forma_pagamento)
        
        if sucesso:
            database.salvar_dados_json(DB)
            return render_template('confirmacao.html', 
                                   forma=forma_escolhida, 
                                   total=ultimo_carrinho.calcular_total(), 
                                   pix_info=pix_info)
        else:
            return redirect(url_for('index', erro_carrinho="Pagamento Recusado!"))
    
    return render_template('checkout.html', carrinho=ultimo_carrinho)


# ==============================================================================
#  3. GESTÃO DO CARRINHO (REMOVER ITEM / LIMPAR)
# ==============================================================================

@app.route('/carrinho/remover/<int:indice>')
def remover_item_carrinho(indice):
    """NOVA ROTA: Remove um item específico pelo índice."""
    carrinho_keys = [int(k) for k in DB['carrinhos'].keys()]
    carrinho_id = max(carrinho_keys) if carrinho_keys else None
    ultimo_carrinho = DB['carrinhos'].get(str(carrinho_id))
    
    if ultimo_carrinho and ultimo_carrinho.status == 'ABERTO':
        ultimo_carrinho.remover_item(indice)
        database.salvar_dados_json(DB)
        
    return redirect(url_for('checkout_web'))

@app.route('/carrinho/limpar', methods=['POST'])
def limpar_carrinho():
    """Esvazia o carrinho atual criando um novo."""
    # Lógica simplificada: redireciona para index, mas poderia criar novo carrinho aqui
    return redirect(url_for('index'))


# ==============================================================================
#  4. MENU DE USUÁRIO
# ==============================================================================

@app.route('/perfil', methods=['GET', 'POST'])
def perfil_usuario():
    cliente = get_current_user()
    if not cliente: return redirect(url_for('login_cadastro'))
    
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.endereco = request.form['endereco']
        if request.form.get('senha'): cliente.senha = request.form['senha']
        database.salvar_dados_json(DB)
        return redirect(url_for('perfil_usuario', sucesso="Dados Atualizados!"))
        
    return render_template('perfil.html', cliente=cliente, sucesso=request.args.get('sucesso'))

@app.route('/pedidos')
def pedidos_prontos():
    cliente = get_current_user()
    if not cliente: return redirect(url_for('login_cadastro'))
    
    pedidos_lista = [
        (pid, c) for pid, c in DB['carrinhos'].items() 
        if c.status == 'PROCESSADO' and c.cliente.cpf == cliente.cpf
    ]
    
    return render_template('pedidos.html', cliente=cliente, pedidos=pedidos_lista)


# ==============================================================================
#  5. ROTAS GERAIS
# ==============================================================================

@app.route('/')
def index():
    return render_template('index.html',
        is_admin=session.get('is_admin', False),
        user_name=session.get('user_name', 'Visitante'),
        produtos=DB['produtos'].items(),
        erro_carrinho=request.args.get('erro_carrinho') 
    )

@app.route('/carrinho/adicionar_item', methods=['POST'])
def adicionar_item_processa():
    cliente_id = session.get('user_id') 
    if not cliente_id: return redirect(url_for('login_cadastro'))
    
    cliente = DB['clientes'].get(cliente_id)
    prod = DB['produtos'].get(request.form.get('produto_id'))
    qtd = int(request.form.get('quantidade', 1))
    acao = request.form.get('acao_compra')

    carrinho_keys = [int(k) for k in DB['carrinhos'].keys()]
    ultimo_id = str(max(carrinho_keys)) if carrinho_keys else '0'
    carrinho = DB['carrinhos'].get(ultimo_id)

    if not carrinho or carrinho.status != 'ABERTO':
        novo_id = str(int(ultimo_id) + 1) if carrinho_keys else '1'
        carrinho = Carrinho(cliente)
        DB['carrinhos'][novo_id] = carrinho
        DB['next_ids']['carrinho'] = int(novo_id) + 1
        ultimo_id = novo_id

    item = ItemCarrinho(prod, qtd)
    carrinho.adicionar_item(item)
    database.salvar_dados_json(DB)

    if acao == 'compra_imediata':
        return redirect(url_for('checkout_web'))
    return redirect(url_for('index'))

@app.route('/produto/<pid>')
def detalhe_produto(pid):
    produto = DB['produtos'].get(pid)
    if not produto: return "404", 404
    return render_template('detalhe_produto.html', produto=produto, pid=pid, frete=produto.calcular_frete())

@app.route('/busca')
def busca():
    termo = request.args.get('termo', '').lower()
    filtrados = [(pid, p) for pid, p in DB['produtos'].items() if termo in p.nome.lower()]
    return render_template('busca.html', produtos=filtrados, termo=termo)

@app.route('/auth', methods=['GET', 'POST'])
def login_cadastro():
    if request.method == 'POST':
        if request.form.get('acao') == 'cadastro':
            return redirect(url_for('cadastrar_cliente_web'))
        
        cpf = request.form.get('cpf_login')
        senha = request.form.get('senha_login')
        user_entry = next(((k, v) for k, v in DB['clientes'].items() if v.cpf == cpf), None)
        
        if user_entry and user_entry[1].senha == senha:
            session['logged_in'] = True
            session['user_id'] = user_entry[0]
            session['user_name'] = user_entry[1].nome
            session['is_admin'] = user_entry[1].is_admin
            return redirect(url_for('index'))
    return render_template('login_cadastro.html')

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente_web():
    if request.method == 'POST':
        novo = Cliente(
            request.form['nome'], request.form['cpf'], request.form['endereco'], 
            senha=request.form['senha']
        )
        nid = str(DB['next_ids']['cliente'])
        DB['clientes'][nid] = novo
        DB['next_ids']['cliente'] += 1
        database.salvar_dados_json(DB)
        session['logged_in'] = True
        session['user_id'] = nid
        session['user_name'] = novo.nome
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)