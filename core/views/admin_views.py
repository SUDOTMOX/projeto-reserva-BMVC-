# Arquivo: core/views/admin_views.py

from flask import Blueprint, render_template, request, redirect, url_for, session
import database
from core.models.produtos import ProdutoFisico

admin_bp = Blueprint('admin', __name__)
DB = database.carregar_dados_json()

def verificar_admin():
    """Helper para proteger rotas."""
    if not session.get('logged_in') or not session.get('is_admin'):
        return False
    return True

@admin_bp.route('/admin')
def dashboard():
    """Painel principal do Admin."""
    if not verificar_admin():
        return redirect(url_for('loja.index'))
        
    return render_template(
        'admin/dashboard.html',
        produtos=DB['produtos'].items(),
        clientes=DB['clientes'].items()
    )

@admin_bp.route('/admin/produto/<pid>', methods=['GET', 'POST'])
def editar_produto(pid):
    """Cria ou Edita um produto (CRUD)."""
    if not verificar_admin():
        return redirect(url_for('loja.index'))

    produto = None
    if pid != 'novo':
        produto = DB['produtos'].get(pid)

    if request.method == 'POST':
        # Captura dados do formulário
        nome = request.form.get('nome')
        preco = float(request.form.get('preco'))
        peso = float(request.form.get('peso'))
        categoria = request.form.get('categoria')
        imagem_url = request.form.get('imagem_url')

        if pid == 'novo':
            # Create
            # Gera um ID simples (ex: timestamp ou sequencial manual para o exemplo)
            # Aqui vamos usar um ID aleatório ou manual para simplificar
            import random
            novo_id = str(random.randint(200, 999))
            
            novo_produto = ProdutoFisico(novo_id, nome, preco, "Descricao..", peso, "10x10")
            novo_produto.categoria = categoria
            novo_produto.imagem_url = imagem_url
            
            DB['produtos'][novo_id] = novo_produto
        elif produto:
            # Update
            produto.nome = nome
            produto.preco = preco
            produto.peso = peso
            produto.categoria = categoria
            produto.imagem_url = imagem_url

        database.salvar_dados_json(DB)
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/editar_produto.html', produto=produto, pid=pid)