# Arquivo: database.py - Módulo de persistência JSON

import json
import os
import sys

# Garante que as importações internas funcionem
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

# Importa as classes dos pacotes para a reconstrução dos objetos
from core.cliente import Cliente
from core.produto_fisico import ProdutoFisico
from core.carrinho import Carrinho
from core.item_carrinho import ItemCarrinho
from core.produto import Produto 


DB_FILE = 'data.json'

# --- DADOS INICIAIS (JSON Puro) ---
# Adicionado 'imagem_url' e MAIS produtos com categorias diversas
DADOS_INICIAIS = {
    'clientes': {
        '1': {'nome': "João Silva", 'cpf': "000.111.222-33", 'endereco': "Rua Principal", 'senha': '123', 'is_admin': False},
        '99': {'nome': "Admin", 'cpf': "999.999.999-99", 'endereco': 'Sede', 'senha': 'admin', 'is_admin': True} 
    }, 
    'produtos': {
        '101': {'nome': "PC Gamer RTX Pro", 'preco': 8500.00, 'peso': 15.0, 'categoria': 'Eletrônico', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=PC+Gamer'}, 
        '102': {'nome': "Monitor UltraWide LG 34\"", 'preco': 1800.00, 'peso': 7.0, 'categoria': 'Eletrônico', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Monitor'},
        '103': {'nome': "Teclado Mecânico RGB Gamer", 'preco': 550.00, 'peso': 1.5, 'categoria': 'Acessório', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Teclado'},
        '104': {'nome': "Livro 'Duna' - Edição Especial", 'preco': 65.00, 'peso': 0.8, 'categoria': 'Livro', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Livro'},
        '105': {'nome': "Câmera Mirrorless Sony Alpha", 'preco': 4200.00, 'peso': 1.0, 'categoria': 'Eletrônico', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Câmera'},
        '106': {'nome': "Camiseta Algodão Básica Preta", 'preco': 49.90, 'peso': 0.3, 'categoria': 'Vestuário', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Camiseta'},
        '107': {'nome': "Fone Over-Ear Edifier W820NB", 'preco': 380.00, 'peso': 0.4, 'categoria': 'Acessório', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Fone'},
        # MAIS PRODUTOS ADICIONAIS
        '108': {'nome': "Mesa de Escritório Gamer DT3", 'preco': 750.00, 'peso': 25.0, 'categoria': 'Móveis', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Mesa+Gamer'},
        '109': {'nome': "SSD NVMe 1TB Kingston Fury", 'preco': 480.00, 'peso': 0.1, 'categoria': 'Informática', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=SSD+NVMe'},
        '110': {'nome': "Smartwatch Amazfit GTR 3 Pro", 'preco': 620.00, 'peso': 0.1, 'categoria': 'Eletrônico', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Smartwatch'},
        '111': {'nome': "Cadeira Gamer Husky Blizzard", 'preco': 1100.00, 'peso': 22.0, 'categoria': 'Móveis', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Cadeira+Gamer'},
        '112': {'nome': "Webcam Logitech C920", 'preco': 350.00, 'peso': 0.2, 'categoria': 'Acessório', 'imagem_url': 'https://via.placeholder.com/600x400/007bff/FFFFFF?text=Webcam'},
    }, 
    'carrinhos': {}, 
    'next_ids': {'cliente': 100, 'carrinho': 1}
}


def carregar_dados_json():
    """Carrega dados do arquivo JSON e reconstrói os objetos Python."""
    try:
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w') as f:
                json.dump(DADOS_INICIAIS, f, indent=4)
            data = DADOS_INICIAIS
        else:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
        
        produtos_obj = {}
        for pid, d in data.get('produtos', {}).items():
            try:
                # Assume ProdutoFisico para simplificação, mas idealmente teria uma fábrica
                produtos_obj[pid] = ProdutoFisico.from_json(d)
            except KeyError as e:
                print(f"AVISO: Produto ID {pid} com dados incompletos ({e}). Ignorado.")
            except Exception as e:
                 print(f"AVISO: Erro ao carregar Produto ID {pid} ({e}). Ignorado.")

        
        clientes_obj = {cid: Cliente.from_json(d) for cid, d in data.get('clientes', {}).items()}
        
        carrinhos_obj = {}
        for cid, d in data.get('carrinhos', {}).items():
            try:
                cliente_ref = clientes_obj.get(d['cliente_id']) 
                if cliente_ref:
                    carrinho_obj = Carrinho.from_json(d, cliente_ref, produtos_obj)
                    carrinhos_obj[cid] = carrinho_obj
            except Exception:
                continue # Ignora carrinhos corrompidos

        return {
            'clientes': clientes_obj,
            'produtos': produtos_obj,
            'carrinhos': carrinhos_obj,
            'next_ids': data.get('next_ids', {'cliente': 1, 'carrinho': 1})
        }

    except Exception as e:
        print(f"ERRO FATAL DE PERSISTÊNCIA: {e}. Servidor usando dados iniciais.")
        # Retorna a estrutura inicial reconstruída para evitar crash
        produtos_obj = {pid: ProdutoFisico.from_json(d) for pid, d in DADOS_INICIAIS['produtos'].items()}
        clientes_obj = {cid: Cliente.from_json(d) for cid, d in DADOS_INICIAIS['clientes'].items()}
        return {
             'clientes': clientes_obj,
             'produtos': produtos_obj,
             'carrinhos': {},
             'next_ids': DADOS_INICIAIS['next_ids']
        }


def salvar_dados_json(dados):
    """Serializa os objetos Python para JSON e salva no arquivo."""
    
    data_to_save = {
        'clientes': {cid: obj.to_json() for cid, obj in dados['clientes'].items()},
        'produtos': {pid: obj.to_json() for pid, obj in dados['produtos'].items()},
        'carrinhos': {cid: obj.to_json() for cid, obj in dados['carrinhos'].items()},
        'next_ids': dados['next_ids']
    }
    
    with open(DB_FILE, 'w') as f:
        json.dump(data_to_save, f, indent=4)