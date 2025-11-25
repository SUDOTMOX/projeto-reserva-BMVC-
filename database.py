import json
import os
from pathlib import Path

# --- IMPORTAÇÕES DAS CLASSES (MODELS) ---
from core.models.usuarios import Cliente
from core.models.produtos import ProdutoFisico
from core.models.vendas import Carrinho, ItemCarrinho

# --- CONFIGURAÇÃO DO ARQUIVO ---
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / 'data.json'

# --- DADOS INICIAIS (SEED) ---
DADOS_INICIAIS = {
    'clientes': {},
    'produtos': {},
    'carrinhos': {},
    'next_ids': {'cliente': 1, 'carrinho': 1}
}

def carregar_dados_json():
    """
    Lê o arquivo JSON e converte em Dicionários de Objetos Python.
    """
    
    # 1. Tenta abrir o arquivo JSON
    if not os.path.exists(DB_FILE):
        print("Arquivo data.json não encontrado. Criando novo...")
        salvar_arquivo_bruto(DADOS_INICIAIS)
        dados_brutos = DADOS_INICIAIS
    else:
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                dados_brutos = json.load(f)
        except json.JSONDecodeError:
            print("ERRO: data.json corrompido. Usando dados vazios.")
            dados_brutos = DADOS_INICIAIS

    # 2. Carregar PRODUTOS
    produtos_obj = {}
    if 'produtos' in dados_brutos:
        for pid, dados in dados_brutos['produtos'].items():
            try:
                prod = ProdutoFisico(
                    id=pid,
                    nome=dados.get('nome', 'Produto Sem Nome'),
                    preco=float(dados.get('preco', 0.0)),
                    descricao=dados.get('descricao', ''),
                    peso=float(dados.get('peso', 0.0)),
                    dimensoes=dados.get('dimensoes', '0x0x0'),
                    categoria=dados.get('categoria', 'Geral')
                )
                prod.imagem_url = dados.get('imagem_url', '')
                produtos_obj[pid] = prod
            except Exception as e:
                print(f"Erro ao carregar produto {pid}: {e}")

    # 3. Carregar CLIENTES
    clientes_obj = {}
    if 'clientes' in dados_brutos:
        for cid, dados in dados_brutos['clientes'].items():
            try:
                cli = Cliente(
                    nome=dados.get('nome', 'Cliente'),
                    cpf=dados.get('cpf', '000'),
                    endereco=dados.get('endereco', ''),
                    senha=dados.get('senha', '123'),
                    is_admin=dados.get('is_admin', False)
                )
                clientes_obj[cid] = cli
            except Exception as e:
                print(f"Erro ao carregar cliente {cid}: {e}")

    # 4. Carregar CARRINHOS (Com proteção contra NULL)
    carrinhos_obj = {}
    if 'carrinhos' in dados_brutos:
        for cid, dados in dados_brutos['carrinhos'].items():
            
            # [CORREÇÃO CRÍTICA] Se o carrinho for null (vazio), pula ele
            if not dados:
                continue

            try:
                # Busca o objeto cliente dono deste carrinho
                cliente_ref = clientes_obj.get(dados.get('cliente_id'))
                
                if cliente_ref:
                    # Usa o método estático from_json da classe Carrinho
                    carrinho = Carrinho.from_json(dados, cliente_ref, produtos_obj)
                    carrinhos_obj[cid] = carrinho
            except Exception as e:
                print(f"Erro ao reconstruir carrinho {cid}: {e}")

    return {
        'clientes': clientes_obj,
        'produtos': produtos_obj,
        'carrinhos': carrinhos_obj,
        'next_ids': dados_brutos.get('next_ids', {'cliente': 1, 'carrinho': 1})
    }


def salvar_dados_json(dados_memoria):
    """
    Recebe os objetos Python da memória, converte para dicionários e salva no JSON.
    """
    
    dict_salvar = {
        'clientes': {},
        'produtos': {},
        'carrinhos': {},
        'next_ids': dados_memoria['next_ids']
    }

    # Serializa Clientes
    for cid, obj in dados_memoria['clientes'].items():
        dict_salvar['clientes'][cid] = obj.to_json()

    # Serializa Produtos
    for pid, obj in dados_memoria['produtos'].items():
        dict_salvar['produtos'][pid] = obj.to_json()

    # Serializa Carrinhos
    for cid, obj in dados_memoria['carrinhos'].items():
        if obj and hasattr(obj, 'to_json'):
            dict_salvar['carrinhos'][cid] = obj.to_json()

    salvar_arquivo_bruto(dict_salvar)


def salvar_arquivo_bruto(dados_dict):
    """Função auxiliar apenas para escrever no disco com utf-8."""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados_dict, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERRO CRÍTICO AO SALVAR DB: {e}")