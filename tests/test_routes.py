import unittest
from unittest.mock import patch
import sys
import os

# Ajusta o caminho para o Python encontrar a pasta 'core' e o 'main.py' na raiz
# Adiciona o diretório pai (..) ao path do sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app # Importa seu servidor Flask
from core.models.usuarios import Cliente

class TestRoutes(unittest.TestCase):

    def setUp(self):
        """Configura o navegador de teste do Flask antes de cada teste."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Desativa proteção CSRF para facilitar testes
        app.secret_key = 'test_key' # Chave necessária para sessão funcionar em testes
        self.client = app.test_client()
        
        # Dados Falsos (Mock) para simular o banco de dados sem ler o arquivo data.json real
        self.mock_db = {
            'clientes': {
                '1': Cliente("Usuario Teste", "123.456.789-00", "Rua X", "senha123", False),
                '99': Cliente("Admin", "999.999.999-99", "Sede", "admin", True)
            },
            'produtos': {},
            'carrinhos': {},
            'next_ids': {'cliente': 2, 'carrinho': 1}
        }

    def test_home_page_status(self):
        """Teste: A página inicial carrega corretamente? (Código 200)"""
        # Patch substitui o banco de dados real pelo nosso mock_db temporário
        with patch('core.views.loja_views.DB', self.mock_db):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            # Verifica se o nome da loja aparece no HTML retornado
            self.assertIn(b'TechNova', response.data)

    def test_login_sucesso(self):
        """Teste: Login com senha correta redireciona e cria sessão?"""
        
        # "Mockamos" o banco de dados dentro da view de Auth
        with patch('core.views.auth_views.DB', self.mock_db):
            # Simula o envio do formulário de login (POST)
            response = self.client.post('/auth', data={
                'acao': 'login',
                'cpf_login': '123.456.789-00',
                'senha_login': 'senha123'
            }, follow_redirects=True)

            # Verifica se a requisição funcionou (200 OK)
            self.assertEqual(response.status_code, 200)
            # Se logou, deve aparecer o nome do usuário no topo da página
            # Nota: b'' significa bytes. O Flask retorna HTML em bytes.
            self.assertIn(b'Usuario Teste', response.data)

    def test_login_falha(self):
        """Teste: Login com senha errada deve mostrar erro."""
        
        with patch('core.views.auth_views.DB', self.mock_db):
            response = self.client.post('/auth', data={
                'acao': 'login',
                'cpf_login': '123.456.789-00',
                'senha_login': 'SENHA_ERRADA'
            }, follow_redirects=True)

            # Verifica se a mensagem de erro apareceu na página
            self.assertIn(b'incorretos', response.data)

    def test_protecao_rota_perfil(self):
        """Teste: Tentar acessar /perfil sem estar logado deve redirecionar."""
        
        with patch('core.views.auth_views.DB', self.mock_db):
            # Tenta acessar direto a rota protegida sem fazer login antes
            response = self.client.get('/perfil', follow_redirects=True)
            
            # Deve ser redirecionado para a tela de login/cadastro
            # Procuramos por um texto que só existe na tela de login
            self.assertIn(b'Acesse sua Conta', response.data)

    def test_logout(self):
        """Teste: O logout limpa a sessão corretamente?"""
        
        with patch('core.views.auth_views.DB', self.mock_db):
            # 1. Força o login na sessão do navegador de teste manualmente
            with self.client.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['logged_in'] = True

            # 2. Clica no botão de sair (acessa a rota /logout)
            response = self.client.get('/logout', follow_redirects=True)
            
            # 3. Verifica se voltou para a vitrine deslogado (botão 'Entrar' aparece)
            self.assertIn(b'Entrar / Cadastrar', response.data)

if __name__ == '__main__':
    unittest.main()