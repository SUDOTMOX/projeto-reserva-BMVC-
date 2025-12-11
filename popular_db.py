import requests
import json
import random
import os

DB_FILE = 'data.json'

def fetch_tech_products():
    """
    Busca produtos reais de tecnologia na FakeStoreAPI.
    """
    url = 'https://fakestoreapi.com/products/category/electronics'
    print(f"--- [API] Buscando Eletrônicos em {url}...")
    try:
        response = requests.get(url)
        data = response.json()
        
        produtos_formatados = []
        for item in data:
            # Filtra apenas o que parece ser tecnologia de verdade
            produtos_formatados.append({
                "nome": item['title'][:50], # Corta nomes muito longos
                "preco": float(item['price']) * 5.5, # Converte USD -> BRL
                "categoria": "Eletrônico",
                "peso": round(random.uniform(0.5, 2.5), 1),
                "imagem_url": item['image'],
                "avaliacoes": []
            })
        return produtos_formatados
    except Exception as e:
        print(f"[ERRO] Falha na API: {e}")
        return []

def get_manual_products():
    """
    Retorna uma lista de Livros e Móveis (Dados Mockados).
    Usamos placeholders de imagem para garantir que não quebrem.
    """
    return [
        # --- LIVROS ---
        {
            "nome": "Código Limpo: Habilidades Práticas",
            "preco": 89.90,
            "categoria": "Livro",
            "peso": 0.5,
            "imagem_url": "https://m.media-amazon.com/images/I/41oKdU9XpCL._SY445_SX342_.jpg",
            "avaliacoes": []
        },
        {
            "nome": "Arquitetura Limpa: O Guia do Artesão",
            "preco": 79.90,
            "categoria": "Livro",
            "peso": 0.6,
            "imagem_url": "https://m.media-amazon.com/images/I/41-sN-mzwKL._SY445_SX342_.jpg",
            "avaliacoes": []
        },
        {
            "nome": "O Senhor dos Anéis: A Sociedade do Anel",
            "preco": 59.90,
            "categoria": "Livro",
            "peso": 1.2,
            "imagem_url": "https://placehold.co/300x450/333/FFF?text=Senhor+dos+Aneis",
            "avaliacoes": []
        },
        {
            "nome": "Harry Potter e a Pedra Filosofal",
            "preco": 45.50,
            "categoria": "Livro",
            "peso": 0.4,
            "imagem_url": "https://placehold.co/300x450/5e3b5e/FFF?text=Harry+Potter",
            "avaliacoes": []
        },

        # --- MÓVEIS ---
        {
            "nome": "Cadeira de Escritório Ergonômica",
            "preco": 650.00,
            "categoria": "Móveis",
            "peso": 12.0,
            "imagem_url": "https://placehold.co/400x400/2c3e50/FFF?text=Cadeira+Ergo",
            "avaliacoes": []
        },
        {
            "nome": "Mesa Gamer Preta 1.20m",
            "preco": 320.00,
            "categoria": "Móveis",
            "peso": 15.5,
            "imagem_url": "https://placehold.co/500x300/000/FFF?text=Mesa+Gamer",
            "avaliacoes": []
        },
        {
            "nome": "Estante de Livros Industrial",
            "preco": 210.00,
            "categoria": "Móveis",
            "peso": 8.0,
            "imagem_url": "https://placehold.co/300x600/8e44ad/FFF?text=Estante",
            "avaliacoes": []
        }
    ]

def main():
    # 1. Carrega o banco atual
    if not os.path.exists(DB_FILE):
        print(f"Arquivo {DB_FILE} não encontrado! Rode o main.py primeiro para criar a estrutura.")
        return

    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db_data = json.load(f)

    # 2. Obtém os produtos novos
    tech_products = fetch_tech_products()
    manual_products = get_manual_products()
    
    todos_novos = tech_products + manual_products

    # 3. Calcula o próximo ID disponível
    if db_data['produtos']:
        ids_existentes = [int(k) for k in db_data['produtos'].keys()]
        next_id = max(ids_existentes) + 1
    else:
        next_id = 101

    # 4. Insere no dicionário
    count = 0
    print("\n--- Inserindo no Banco ---")
    for prod in todos_novos:
        # Verifica se já existe produto com nome igual para evitar duplicatas óbvias
        nomes_existentes = [p['nome'] for p in db_data['produtos'].values()]
        if prod['nome'] in nomes_existentes:
            continue

        db_data['produtos'][str(next_id)] = prod
        print(f" [+] ({prod['categoria']}) {prod['nome']}")
        next_id += 1
        count += 1

    # 5. Salva no arquivo
    if count > 0:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Sucesso! {count} novos itens adicionados ao catálogo.")
    else:
        print("\n⚠ Nenhum item novo adicionado (talvez eles já existam).")

if __name__ == "__main__":
    main()