from tinydb import TinyDB, Query

class Pousada:
    def __init__(self, nome, idPousada, estado='disponível', pessoasSuportadas=0, limpeza=True, db=None):
        self.nome = nome
        self.idPousada = idPousada
        self.estado = estado
        self.pessoasSuportadas = pessoasSuportadas
        self.limpeza = limpeza
        self.db = db

    def cadastrarPousada(self):
        # Verificar se já existe uma pousada com este ID
        pousada_existente = self.db.search(Query().idPousada == self.idPousada)
        if pousada_existente:
            return {'message': 'Já existe uma pousada com este ID!'}

        self.db.insert({
            'tipo': 'pousada',
            'nome': self.nome,
            'idPousada': self.idPousada,
            'estado': self.estado,
            'pessoasSuportadas': self.pessoasSuportadas,
            'limpeza': self.limpeza
        })
        return {'message': 'Pousada cadastrada com sucesso!'}

