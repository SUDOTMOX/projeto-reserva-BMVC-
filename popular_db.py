import requests
import json
import random
import os

DB_FILE = 'data.json'

<<<<<<< HEAD
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
=======
# MUDANÇA 1: Buscamos APENAS eletrônicos na API
API_URL = 'https://fakestoreapi.com/products/category/electronics'

def fetch_new_products():
    """Busca novos produtos da API."""
    print(f"Buscando produtos TECH em: {API_URL}...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status() 
        return response.json()
    except Exception as e:
        print(f"ERRO ao buscar produtos: {e}")
        return None

def format_product(api_product, new_id):
    """Converte o formato da API para o formato do nosso DB."""
    
    # MUDANÇA 2: Como a API só retorna "electronics", vamos variar 
    # as categorias manualmente para sua loja ficar bonita no filtro.
    categorias_tech = ["Eletrônico", "Informática", "Acessório", "Gamer"]
    categoria_escolhida = random.choice(categorias_tech)

    # Truque para dar nomes mais "Tech" baseados no título original
    nome = api_product['title']
    if "WD" in nome or "SSD" in nome or "Drive" in nome:
        categoria_escolhida = "Informática"
    elif "Monitor" in nome:
        categoria_escolhida = "Eletrônico"
    
    return {
        "nome": nome[:60], # Limita o tamanho do nome
        "preco": float(api_product['price']) * 5.5, # Converte USD para BRL (aprox)
        "categoria": categoria_escolhida,
        "peso": round(random.uniform(0.2, 3.0), 1),
        "imagem_url": api_product['image'],
        "avaliacoes": []
    }

def main():
    # 1. Verifica se o arquivo existe
    if not os.path.exists(DB_FILE):
        print("Arquivo data.json não encontrado! Rode o app_web.py primeiro para criar a estrutura.")
        return

    # 2. Carrega o DB atual
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 3. Busca produtos TECH
    new_products_api = fetch_new_products()
    if not new_products_api:
        return

    # 4. Limpa produtos antigos (OPCIONAL: Se quiser só tech, descomente a linha abaixo)
    # data['produtos'] = {} 

    # Descobre o próximo ID disponível
    if data['produtos']:
        ids_existentes = [int(k) for k in data['produtos'].keys()]
        next_id = max(ids_existentes) + 1
    else:
        next_id = 101
    
    count = 0
    # Vamos duplicar a lista da API para ter mais produtos (a API só retorna uns 6 eletrônicos)
    # Isso fará sua loja parecer cheia com 12 produtos
    lista_dobrada = new_products_api + new_products_api 

    for product in lista_dobrada:
        formatted = format_product(product, next_id)
        # Adiciona uma pequena variação no preço para o duplicado não ser idêntico
        if count >= len(new_products_api): 
            formatted['preco'] += 50.00 
            formatted['nome'] = formatted['nome'] + " (Edição Especial)"

        data['produtos'][str(next_id)] = formatted
        print(f"Adicionado Tech: {formatted['nome']}")
        next_id += 1
        count += 1

    # 5. Salva
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\nSUCESSO! {count} produtos TECH adicionados ao catálogo.")
>>>>>>> a5dc457 (docker do projeto pronto)

if __name__ == "__main__":
    main()