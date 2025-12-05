import requests
import json
import random
import os

DB_FILE = 'data.json'

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

if __name__ == "__main__":
    main()