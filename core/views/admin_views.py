<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for, session
import database
from core.produto_fisico import ProdutoFisico

admin_bp = Blueprint('admin', __name__)

def verificar_admin():
    """
    Função auxiliar para proteger as rotas.
    Retorna True se for admin logado, False caso contrário.
    """
=======

from flask import Blueprint, render_template, request, redirect, url_for, session
import database
from core.models.produtos import ProdutoFisico

admin_bp = Blueprint('admin', __name__)
DB = database.carregar_dados_json()

def verificar_admin():
>>>>>>> a5dc457 (docker do projeto pronto)
    if not session.get('logged_in') or not session.get('is_admin'):
        return False
    return True

@admin_bp.route('/admin')
def dashboard():
<<<<<<< HEAD
    """
    Painel Principal do Admin (READ do CRUD).
    """
    if not verificar_admin():
        return redirect(url_for('loja.index'))
        
    DB = database.carregar_dados_json()
=======
    if not verificar_admin():
        return redirect(url_for('loja.index'))
        
>>>>>>> a5dc457 (docker do projeto pronto)
    return render_template(
        'admin/dashboard.html',
        produtos=DB['produtos'].items(),
        clientes=DB['clientes'].items()
    )

@admin_bp.route('/admin/produto/<pid>', methods=['GET', 'POST'])
def editar_produto(pid):
<<<<<<< HEAD
    """
    Rota Híbrida: Criação (CREATE) e Edição (UPDATE).
    """
    if not verificar_admin():
        return redirect(url_for('loja.index'))

    DB = database.carregar_dados_json()
    produto = None
    
    # Se não for novo, tenta buscar o produto existente
=======
    if not verificar_admin():
        return redirect(url_for('loja.index'))

    produto = None
>>>>>>> a5dc457 (docker do projeto pronto)
    if pid != 'novo':
        produto = DB['produtos'].get(pid)

    if request.method == 'POST':
<<<<<<< HEAD
        # Captura os dados do formulário
=======
>>>>>>> a5dc457 (docker do projeto pronto)
        nome = request.form.get('nome')
        preco = float(request.form.get('preco'))
        peso = float(request.form.get('peso'))
        categoria = request.form.get('categoria')
        imagem_url = request.form.get('imagem_url')

<<<<<<< HEAD
        # Lógica de CRIAÇÃO (CREATE)
        if pid == 'novo':
            # Gera um ID novo baseado no maior ID existente
            p_ids = [int(k) for k in DB['produtos'].keys()]
            new_id = str(max(p_ids) + 1) if p_ids else "101"
            
            # Cria o objeto usando argumentos nomeados (CORREÇÃO DE BUG)
            novo_produto = ProdutoFisico(
                nome=nome,
                preco=preco,
                peso=peso,
                imagem_url=imagem_url,
                categoria=categoria
            )
            # Injeta o ID manualmente no objeto (CRUCIAL PARA O CARRINHO)
            novo_produto.id = new_id 
            
            DB['produtos'][new_id] = novo_produto
            
        # Lógica de ATUALIZAÇÃO (UPDATE)
        elif produto:
=======
        if pid == 'novo':
           
            import random
            novo_id = str(random.randint(200, 999))
            
            novo_produto = ProdutoFisico(novo_id, nome, preco, "Descricao..", peso, "10x10")
            novo_produto.categoria = categoria
            novo_produto.imagem_url = imagem_url
            
            DB['produtos'][novo_id] = novo_produto
        elif produto:
            
>>>>>>> a5dc457 (docker do projeto pronto)
            produto.nome = nome
            produto.preco = preco
            produto.peso = peso
            produto.categoria = categoria
            produto.imagem_url = imagem_url

<<<<<<< HEAD
        # Salva as alterações no JSON
        database.salvar_dados_json(DB)
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/editar_produto.html', produto=produto, pid=pid)

@admin_bp.route('/admin/deletar/produto/<pid>', methods=['POST'])
def deletar_produto(pid):
    """
    Rota de Exclusão (DELETE do CRUD).
    Só aceita POST para evitar exclusões acidentais via link direto.
    """
    if not verificar_admin():
        return redirect(url_for('loja.index'))
    
    DB = database.carregar_dados_json()
    
    if pid in DB['produtos']:
        nome_removido = DB['produtos'][pid].nome
        del DB['produtos'][pid]
        database.salvar_dados_json(DB)
        print(f"[ADMIN] Produto '{nome_removido}' (ID: {pid}) excluído com sucesso.")
    
    return redirect(url_for('admin.dashboard'))
=======
        database.salvar_dados_json(DB)
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/editar_produto.html', produto=produto, pid=pid)
>>>>>>> a5dc457 (docker do projeto pronto)
