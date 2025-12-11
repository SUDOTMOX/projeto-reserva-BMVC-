from flask import Blueprint, render_template, request, redirect, url_for, session
import database
from core.cliente import Cliente

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth', methods=['GET', 'POST'])
def login_cadastro():
    DB = database.carregar_dados_json()
    erro = request.args.get('erro')

    if request.method == 'POST':
        acao = request.form.get('acao')

        if acao == 'cadastro':
            nome = request.form.get('nome_cadastro') or "Cliente Novo"
            cpf = request.form.get('cpf_cadastro') or "000.000.000-00"
            email = request.form.get('email_cadastro') or "email@teste.com"
            senha = request.form.get('senha_cadastro') or "123"
            
            for c in DB['clientes'].values():
                if c.cpf == cpf:
                     return render_template('auth/login.html', erro="CPF já cadastrado!")

            novo_cliente = Cliente(
                nome=nome,
                cpf=cpf,
                endereco="Atualize seu endereço",
                senha=senha,
                is_admin=False
            )
            
            novo_id = str(DB['next_ids']['cliente'])
            DB['clientes'][novo_id] = novo_cliente
            DB['next_ids']['cliente'] += 1
            database.salvar_dados_json(DB)
            
            session['logged_in'] = True
            session['user_id'] = novo_id
            session['user_name'] = novo_cliente.nome
            session['is_admin'] = False
            
            return redirect(url_for('auth.perfil'))

        elif acao == 'login':
            cpf_login = request.form.get('cpf_login')
            senha_login = request.form.get('senha_login')
            
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
    session.clear()
    return redirect(url_for('loja.index'))

@auth_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    DB = database.carregar_dados_json()
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro'))
        
    cliente = DB['clientes'].get(user_id)
    if not cliente:
        session.clear()
        return redirect(url_for('auth.login_cadastro'))
    
    if request.method == 'POST':
        cliente.nome = request.form.get('nome')
        cliente.endereco = request.form.get('endereco')
        nova_senha = request.form.get('senha')
        if nova_senha:
            cliente.senha = nova_senha
            
        database.salvar_dados_json(DB)
        session['user_name'] = cliente.nome
        
    return render_template('auth/perfil.html', cliente=cliente)

@auth_bp.route('/pedidos')
def pedidos():
    DB = database.carregar_dados_json()
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro'))
    
    cliente = DB['clientes'].get(user_id)
    
    meus_pedidos = [
        (cid, c) for cid, c in DB['carrinhos'].items()
        if c.cliente.cpf == cliente.cpf and c.status == 'PROCESSADO'
    ]
    
    return render_template('auth/pedidos.html', pedidos=meus_pedidos, cliente=cliente)