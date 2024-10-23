from tinydb import TinyDB, Query

class Pousada:
    def __init__(self, nome, idPousada, estado='disponível', pessoasSuportadas=0, limpeza=True, preco=0.0, db=None):
        self.nome = nome
        self.idPousada = idPousada
        self.estado = estado
        self.pessoasSuportadas = pessoasSuportadas
        self.limpeza = limpeza
        self.preco = preco  # Novo atributo para o preço da diária
        self.db = db

    def cadastrarPousada(self):
        # Verificar se já existe uma pousada com este ID
        pousada_existente = self.db.search(Query().idPousada == self.idPousada)
        
        if pousada_existente:
            return {'message': 'Já existe uma pousada com este ID!'}

        # Cadastra a nova pousada com o preço incluído
        self.db.insert({
            'tipo': 'pousada',
            'nome': self.nome,
            'idPousada': self.idPousada,
            'estado': self.estado,
            'pessoasSuportadas': self.pessoasSuportadas,
            'limpeza': self.limpeza,
            'preco': self.preco  # Adicionando o preço ao registro
        })
        
        return {'message': 'Pousada cadastrada com sucesso!'}



