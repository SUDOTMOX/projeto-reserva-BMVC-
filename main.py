
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