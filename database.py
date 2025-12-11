import json
import os
import sys

# Ajuste de imports para garantir que funcione tanto rodando main.py quanto app_web.py
try:
    from core.cliente import Cliente
    from core.produto_fisico import ProdutoFisico
    from core.carrinho import Carrinho
except ImportError:
    # Fallback caso os caminhos não sejam encontrados diretamente
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from core.cliente import Cliente
    from core.produto_fisico import ProdutoFisico
    from core.carrinho import Carrinho

DB_FILE = 'data.json'

DADOS_INICIAIS = {
    'clientes': {
        '99': {'nome': "Admin", 'cpf': "999.999.999-99", 'endereco': 'Sede', 'senha': 'admin', 'is_admin': True} 
    }, 
    'produtos': {
        '101': {'nome': "Produto Teste", 'preco': 100.00, 'peso': 1.0, 'categoria': 'Geral', 'imagem_url': '', 'avaliacoes': []}, 
    }, 
    'carrinhos': {}, 
    'next_ids': {'cliente': 100, 'carrinho': 1}
}

def carregar_dados_json():
    print("--- [DB] Carregando dados... ---")
    try:
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(DADOS_INICIAIS, f, indent=4)
            data = DADOS_INICIAIS
        else:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # 1. Reconstrói Produtos (COM CORREÇÃO DE ID)
        produtos_obj = {}
        for pid, d in data.get('produtos', {}).items():
            prod = ProdutoFisico.from_json(d)
            prod.id = pid  # <--- CORREÇÃO CRÍTICA: Injeta o ID no objeto para o carrinho funcionar
            produtos_obj[pid] = prod

        # 2. Reconstrói Clientes
        clientes_obj = {}
        for cid, d in data.get('clientes', {}).items():
            clientes_obj[cid] = Cliente.from_json(d)
        
        # 3. Reconstrói Carrinhos (COM PROTEÇÃO)
        carrinhos_obj = {}
        for cid, d in data.get('carrinhos', {}).items():
            cliente_cpf = d.get('cliente_id')
            
            # Tenta achar o cliente comparando strings limpas
            cliente_ref = None
            for c in clientes_obj.values():
                if str(c.cpf).strip() == str(cliente_cpf).strip():
                    cliente_ref = c
                    break
            
            # Se não achar o cliente, cria um temporário para não perder o carrinho
            if not cliente_ref:
                # print(f"[AVISO] Cliente CPF {cliente_cpf} não encontrado. Usando cliente temporário.")
                cliente_ref = Cliente("Cliente Desconhecido", str(cliente_cpf), "Sem Endereço")

            try:
                carrinho_obj = Carrinho.from_json(d, cliente_ref, produtos_obj)
                carrinhos_obj[cid] = carrinho_obj
            except Exception as e:
                print(f"[ERRO] Falha ao reconstruir carrinho {cid}: {e}")
                continue

        return {
            'clientes': clientes_obj,
            'produtos': produtos_obj,
            'carrinhos': carrinhos_obj,
            'next_ids': data.get('next_ids', {'cliente': 100, 'carrinho': 1})
        }

    except Exception as e:
        print(f"[ERRO FATAL] DB falhou: {e}")
        # Retorna estrutura vazia segura em caso de erro fatal
        return {'clientes': {}, 'produtos': {}, 'carrinhos': {}, 'next_ids': {'cliente': 100, 'carrinho': 1}}


def salvar_dados_json(dados):
    try:
        data_to_save = {
            'clientes': {cid: obj.to_json() for cid, obj in dados['clientes'].items()},
            'produtos': {pid: obj.to_json() for pid, obj in dados['produtos'].items()},
            'carrinhos': {cid: obj.to_json() for cid, obj in dados['carrinhos'].items() if obj is not None},
            'next_ids': dados['next_ids']
        }
        
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        # print("--- [DB] Dados salvos com sucesso ---")
            
    except Exception as e:
        print(f"[ERRO] Falha ao salvar: {e}")