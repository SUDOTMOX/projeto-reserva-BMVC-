from flask import Blueprint, render_template, request
import database

loja_bp = Blueprint('loja', __name__)
DB = database.carregar_dados_json()

@loja_bp.route('/')
def index():
    return render_template(
        'index.html',
        produtos=DB['produtos'].items()
    )

@loja_bp.route('/produto/<pid>')
def detalhe_produto(pid):
    produto = DB['produtos'].get(pid)
    
    if not produto:
        return "Produto não encontrado", 404
        
    frete_estimado = produto.calcular_frete()
    
    return render_template(
        'detalhe_produto.html',
        produto=produto,
        pid=pid,
        frete=frete_estimado
    )

@loja_bp.route('/busca')
def busca():
    
    termo = request.args.get('termo', '').lower()
    categoria = request.args.get('categoria', '')
    preco_max = request.args.get('preco_max')
    avaliacao_min = request.args.get('avaliacao_min')
    resultados = []

    for pid, prod in DB['produtos'].items():
        match = True
        if termo and termo not in prod.nome.lower():
            match = False
        if categoria and categoria != prod.categoria:
            match = False   
        if preco_max:
            try:
                if prod.preco > float(preco_max):
                    match = False
            except ValueError:
                pass 
        if match:
            resultados.append((pid, prod))
    todas_categorias = sorted(list(set(p.categoria for p in DB['produtos'].values())))
    return render_template(
        'busca.html',
        produtos=resultados,
        categorias=todas_categorias,
        termo=termo,
        categoria_selecionada=categoria
    )