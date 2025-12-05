
from flask import Blueprint, render_template, request, redirect, url_for, session
import database
from core.models.usuarios import Cliente

auth_bp = Blueprint('auth', __name__)

DB = database.carregar_dados_json()

@auth_bp.route('/auth', methods=['GET', 'POST'])
def login_cadastro():
    erro = None

    if request.method == 'POST':
        acao = request.form.get('acao')

        if acao == 'cadastro':
            novo_cliente = Cliente(
                nome="Novo Cliente", 
                cpf="000.000.000-00", 
                endereco="Endereço Padrão",
                senha="123",
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
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro'))
        
    cliente = DB['clientes'].get(user_id)
    
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
   
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_cadastro'))
    
   
    meus_pedidos = [
        (cid, c) for cid, c in DB['carrinhos'].items()
        if c.cliente_id == user_id and c.status == 'PROCESSADO' 
    ]
     
    return render_template('auth/pedidos.html', pedidos=meus_pedidos)