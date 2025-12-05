# Arquivo: core/avaliacao.py

class Avaliacao:
    """Classe de dados simples para ser Associada ao Produto."""
    def __init__(self, cliente_id, nota, comentario):
        self.cliente_id = cliente_id
        self.nota = nota
        self.comentario = comentario
    
    def to_json(self):
        return {'cliente_id': self.cliente_id, 'nota': self.nota, 'comentario': self.comentario}
    
    @staticmethod
    def from_json(data):
        return Avaliacao(data['cliente_id'], data['nota'], data['comentario'])