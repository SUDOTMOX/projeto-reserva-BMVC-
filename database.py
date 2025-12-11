<<<<<<< HEAD
=======
# Arquivo: database.py - Módulo de persistência JSON

>>>>>>> a5dc457 (docker do projeto pronto)
import json
import os
import sys

<<<<<<< HEAD
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
=======
# Garante que as importações internas funcionem
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

# Importa as classes dos pacotes para a reconstrução dos objetos
from core.cliente import Cliente
from core.produto_fisico import ProdutoFisico
from core.carrinho import Carrinho
from core.item_carrinho import ItemCarrinho
# Se tiver outras classes como ProdutoDigital, importe aqui também

DB_FILE = 'data.json'

# --- DADOS INICIAIS (JSON Puro) para caso o arquivo não exista ---
DADOS_INICIAIS = {
    'clientes': {
        '1': {'nome': "João Silva", 'cpf': "000.111.222-33", 'endereco': "Rua Principal", 'senha': '123', 'is_admin': False},
        '99': {'nome': "Admin", 'cpf': "999.999.999-99", 'endereco': 'Sede', 'senha': 'admin', 'is_admin': True} 
    }, 
    'produtos': {
        '101': {'nome': "PC Gamer RTX", 'preco': 8500.00, 'peso': 15.0, 'categoria': 'Eletrônico', 'imagem_url': 'https://via.placeholder.com/300x200', 'avaliacoes': []}, 
>>>>>>> a5dc457 (docker do projeto pronto)
    }, 
    'carrinhos': {}, 
    'next_ids': {'cliente': 100, 'carrinho': 1}
}

def carregar_dados_json():
<<<<<<< HEAD
    print("--- [DB] Carregando dados... ---")
    try:
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w', encoding='utf-8') as f:
=======
    """Carrega dados do arquivo JSON e reconstrói os objetos Python."""
    try:
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w') as f:
>>>>>>> a5dc457 (docker do projeto pronto)
                json.dump(DADOS_INICIAIS, f, indent=4)
            data = DADOS_INICIAIS
        else:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
<<<<<<< HEAD
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
=======
        # 1. Reconstrói Produtos
        produtos_obj = {}
        for pid, d in data.get('produtos', {}).items():
            try:
                # Cria o produto usando o método estático from_json da classe
                produtos_obj[pid] = ProdutoFisico.from_json(d)
            except Exception as e:
                 print(f"AVISO: Erro ao carregar Produto ID {pid} ({e}). Ignorado.")

        # 2. Reconstrói Clientes
        clientes_obj = {cid: Cliente.from_json(d) for cid, d in data.get('clientes', {}).items()}
        
        # 3. Reconstrói Carrinhos (Depende de Clientes e Produtos)
        carrinhos_obj = {}
        for cid, d in data.get('carrinhos', {}).items():
            try:
                cliente_id = d.get('cliente_id') # Ajuste conforme sua estrutura de JSON
                # Se no JSON o carrinho salva o ID do cliente ou o objeto cliente aninhado, ajuste aqui.
                # Assumindo que Carrinho.from_json lida com isso ou esperamos um ID:
                
                # Se o Carrinho.from_json precisa do objeto cliente real:
                cliente_ref = clientes_obj.get(str(cliente_id)) 
                
                # Nota: Dependendo de como seu Carrinho.from_json foi escrito anteriormente,
                # ele pode precisar de (data, cliente_ref, produtos_db).
                # Vamos assumir a assinatura padrão que criamos:
                if cliente_ref:
                    carrinho_obj = Carrinho.from_json(d, cliente_ref, produtos_obj)
                    carrinhos_obj[cid] = carrinho_obj
            except Exception as e:
                # print(f"Erro ao carregar carrinho {cid}: {e}")
                continue 
>>>>>>> a5dc457 (docker do projeto pronto)

        return {
            'clientes': clientes_obj,
            'produtos': produtos_obj,
            'carrinhos': carrinhos_obj,
            'next_ids': data.get('next_ids', {'cliente': 100, 'carrinho': 1})
        }

    except Exception as e:
<<<<<<< HEAD
        print(f"[ERRO FATAL] DB falhou: {e}")
        # Retorna estrutura vazia segura em caso de erro fatal
        return {'clientes': {}, 'produtos': {}, 'carrinhos': {}, 'next_ids': {'cliente': 100, 'carrinho': 1}}


def salvar_dados_json(dados):
=======
        print(f"ERRO FATAL DE PERSISTÊNCIA: {e}. Servidor usando dados iniciais na memória.")
        # Retorna estrutura vazia/inicial para não crashar o app, mas avisa no console
        return {
             'clientes': {},
             'produtos': {},
             'carrinhos': {},
             'next_ids': {'cliente': 100, 'carrinho': 1}
        }


def salvar_dados_json(dados):
    """Serializa os objetos Python para JSON e salva no arquivo."""
>>>>>>> a5dc457 (docker do projeto pronto)
    try:
        data_to_save = {
            'clientes': {cid: obj.to_json() for cid, obj in dados['clientes'].items()},
            'produtos': {pid: obj.to_json() for pid, obj in dados['produtos'].items()},
            'carrinhos': {cid: obj.to_json() for cid, obj in dados['carrinhos'].items() if obj is not None},
            'next_ids': dados['next_ids']
        }
        
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
<<<<<<< HEAD
        # print("--- [DB] Dados salvos com sucesso ---")
            
    except Exception as e:
        print(f"[ERRO] Falha ao salvar: {e}")
=======
            
    except Exception as e:
        print(f"ERRO CRÍTICO AO SALVAR: {e}")
>>>>>>> a5dc457 (docker do projeto pronto)
