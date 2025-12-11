import unittest
import sys
import os

# Ajusta o caminho para o Python encontrar a pasta 'core'
# Isso garante que funcione mesmo se você rodar de dentro da pasta tests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.models.produtos import ProdutoFisico
from core.models.usuarios import Cliente
from core.models.vendas import Carrinho, ItemCarrinho

class TestModels(unittest.TestCase):

    def setUp(self):
        """
        Executado antes de CADA teste.
        Cria objetos 'falsos' na memória para testar isoladamente.
        """
        self.cliente = Cliente("Teste User", "000", "Rua Teste", "123")
        # Produto: Preço 100.0, Peso 2.0
        self.produto = ProdutoFisico("1", "Notebook", 100.0, "Desc", 2.0, "10x10")

    def test_calculo_frete(self):
        """
        Verifica a lógica de Polimorfismo do frete.
        Fórmula no código: 15.0 + (peso * 2.5)
        Conta: 15.0 + (2.0 * 2.5) = 15 + 5 = 20.0
        """
        esperado = 20.0
        resultado = self.produto.calcular_frete()
        self.assertEqual(resultado, esperado, "O cálculo do frete está incorreto!")

    def test_subtotal_item(self):
        """Verifica se o cálculo (Preço x Quantidade) funciona."""
        # 2 notebooks de 100.0 = 200.0
        item = ItemCarrinho(self.produto, 2)
        self.assertEqual(item.subtotal(), 200.0)

    def test_total_carrinho(self):
        """Verifica a soma total do carrinho com múltiplos itens."""
        carrinho = Carrinho(self.cliente)
        
        # Adiciona 1 Notebook (100.0)
        carrinho.adicionar_item(ItemCarrinho(self.produto, 1))
        
        # Cria outro produto de 50.0
        mouse = ProdutoFisico("2", "Mouse", 50.0, "Desc", 0.5, "5x5")
        # Adiciona 2 Mouses (50.0 cada = 100.0)
        carrinho.adicionar_item(ItemCarrinho(mouse, 2))

        # Total esperado: 100 + 100 = 200.0
        self.assertEqual(carrinho.calcular_total(), 200.0)

if __name__ == '__main__':
    unittest.main()