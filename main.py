<<<<<<< HEAD

from flask import Flask
from datetime import timedelta
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from core.views.loja_views import loja_bp
from core.views.auth_views import auth_bp
from core.views.checkout_views import checkout_bp
from core.views.admin_views import admin_bp


app = Flask(__name__, 
            template_folder='core/templates', 
            static_folder='core/static')


app.secret_key = 'chave_muito_secreta_projeto_unb'  
app.permanent_session_lifetime = timedelta(minutes=60) 


app.register_blueprint(loja_bp)      
app.register_blueprint(auth_bp)     
app.register_blueprint(checkout_bp) 
app.register_blueprint(admin_bp)     

# 6. Inicialização do Servidor
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 SISTEMA INICIADO: TechNova Store (Arquitetura BMVS)")
    print("📂 Templates carregados de: core/templates")
    print("📂 Banco de Dados: data.json")
    print(f"🔗 Acesse em: http://127.0.0.1:5000")
    print("="*50 + "\n")
    
    app.run(debug=True)
=======
# Arquivo: main.py (Na raiz)
# Este arquivo contém o menu e orquestra a execução das classes.

# Importações de classes dos pacotes
from core.cliente import Cliente
from core.produto_fisico import ProdutoFisico
from core.carrinho import Carrinho
from core.item_carrinho import ItemCarrinho
from pagamentos.pagamento_cartao import PagamentoCartao
from pagamentos.pagamento_pix import PagamentoPix
from pagamentos.pagamento_boleto import PagamentoBoleto

import database # Módulo de persistência (no mesmo nível)

# --- INICIALIZAÇÃO DE DADOS ---
try:
    DB = database.carregar_dados_json()
    clientes_db = DB['clientes']
    produtos_db = DB['produtos']
    carrinhos_db = DB['carrinhos']
    next_ids = DB['next_ids']

    # Referência Global para Serialização Correta (Associação)
    Cliente.db_ref = clientes_db 

except Exception as e:
    print(f"\nERRO CRÍTICO NA INICIALIZAÇÃO: {e}")
    exit(1)


# (Incluir aqui as funções salvar_e_sair, cadastrar_cliente_func, listar_entidades_func, criar_carrinho_func, processar_pagamento_func, e exibir_menu, conforme o padrão anterior)

# --- LOOP PRINCIPAL DO PROGRAMA ---
if __name__ == "__main__":
    # O loop while True deve estar aqui para executar o menu.
    # ...
    pass
>>>>>>> 607f5ec40e532919c5874d28420be5eff9da6bcf
