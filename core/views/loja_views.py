from flask import Blueprint, render_template, request
import database

loja_bp = Blueprint('loja', __name__)
DB = database.carregar_dados_json()

@loja_bp.route('/')
def index():
    """Página inicial (Vitrine)."""
    return render_template(
        'index.html',
        produtos=DB['produtos'].items()
    )

@loja_bp.route('/produto/<pid>')
def detalhe_produto(pid):
    """Exibe detalhes de um produto específico."""
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
    """Busca Avançada com múltiplos filtros (Restaurado do Original)."""
    
    # 1. Captura os parâmetros da URL
    termo = request.args.get('termo', '').lower()
    categoria = request.args.get('categoria', '')
    preco_max = request.args.get('preco_max')
    avaliacao_min = request.args.get('avaliacao_min')
    
    resultados = []

    # 2. Aplica os filtros
    for pid, prod in DB['produtos'].items():
        match = True
        
        # Filtro por Nome
        if termo and termo not in prod.nome.lower():
            match = False
        
        # Filtro por Categoria
        if categoria and categoria != prod.categoria:
            match = False
            
        # Filtro por Preço Máximo
        if preco_max:
            try:
                if prod.preco > float(preco_max):
                    match = False
            except ValueError:
                pass # Ignora se o usuário digitou algo errado
        
        # Filtro por Avaliação (Simulado, já que Avaliação não está no JSON de produto)
        # Se quiser implementar real, precisaria salvar nota média no produto
        
        if match:
            resultados.append((pid, prod))
    
    # Pega categorias únicas para preencher o <select>
    todas_categorias = sorted(list(set(p.categoria for p in DB['produtos'].values())))

    return render_template(
        'busca.html',
        produtos=resultados,
        categorias=todas_categorias,
        termo=termo,
        categoria_selecionada=categoria
    )