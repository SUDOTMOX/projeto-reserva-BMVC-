# Arquivo: core/views/auth_views.py

from flask import Blueprint, render_template, request, redirect, url_for, session
import database
from core.models.usuarios import Cliente

# Define o Blueprint
auth_bp = Blueprint('auth', __name__)

# Carrega o banco de dados (Simulação JSON)
DB = database.carregar_dados_json()

@auth_bp.route('/auth', methods=['GET', 'POST'])
def login_cadastro():
    """Gerencia tanto o Login quanto o Cadastro de novos usuários."""
    erro = None

    if request.method == 'POST':
        acao = request.form.get('acao')

        # --- LÓGICA DE CADASTRO ---
        if acao == 'cadastro':
            # Criação de Objeto (Instanciação de Cliente)
            novo_cliente = Cliente(
                nome="Novo Cliente", # Simplificado para o exemplo, idealmente viria do form
                cpf="000.000.000-00", 
                endereco="Endereço Padrão",
                senha="123",
                is_admin=False
            )
            
            # Persistência
            novo_id = str(DB['next_ids']['cliente'])
            DB['clientes'][novo_id] = novo_cliente
            DB['next_ids']['cliente'] += 1
            database.salvar_dados_json(DB)
            
            # Login automático após cadastro
            session['logged_in'] = True
            session['user_id'] = novo_id
            session['user_name'] = novo_cliente.nome
            session['is_admin'] = False
            
            return redirect(url_for('auth.perfil')) # Vai para o perfil preencher dados reais

        # --- LÓGICA DE LOGIN ---
        elif acao == 'login':
            cpf_login = request.form.get('cpf_login')
            senha_login = request.form.get('senha_login')
            
            # Busca linear (simples para JSON)
            usuario_encontrado = None
            id_encontrado = None
            
            for uid, cliente in DB['clientes'].items():
                if cliente.cpf == cpf_login and cliente.senha == senha_login:
                    usuario_encontrado = cliente
                    id_encontrado = uid
                    break
            
            if usuario_encontrado:
                session['logged_in'] = True
                session['user_id'] = id_encontrado
                session['user_name'] = usuario_encontrado.nome
                session['is_admin'] = usuario_encontrado.is_admin
                return redirect(url_for('loja.index'))
            else:
                erro = "CPF ou Senha incorretos."

    return render_template('auth/login.html', erro=erro)

@auth_bp.route('/logout')
def logout():
    """Limpa a sessão do usuário."""
    session.clear()
    return redirect(url_for('loja.index'))

@auth_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    """Exibe e edita dados do usuário logado."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro'))
        
    cliente = DB['clientes'].get(user_id)
    
    if request.method == 'POST':
        # Atualiza dados do objeto
        cliente.nome = request.form.get('nome')
        cliente.endereco = request.form.get('endereco')
        nova_senha = request.form.get('senha')
        if nova_senha:
            cliente.senha = nova_senha
            
        database.salvar_dados_json(DB)
        session['user_name'] = cliente.nome # Atualiza sessão
        
    return render_template('auth/perfil.html', cliente=cliente)

@auth_bp.route('/pedidos')
def pedidos():
    """Lista histórico de pedidos (Carrinhos com status PROCESSADO)."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro'))
    
    # Filtra apenas os carrinhos deste usuário que já foram processados
    meus_pedidos = [
        (cid, c) for cid, c in DB['carrinhos'].items()
        if c.cliente_id == user_id and c.status == 'PROCESSADO' # Usando cliente_id salvo no JSON ou objeto
    ]
    
    # Nota: Se o objeto Carrinho não tiver cliente_id direto, usamos a referência:
    # if c.cliente.cpf == DB['clientes'][user_id].cpf ...
    
    return render_template('auth/pedidos.html', pedidos=meus_pedidos)