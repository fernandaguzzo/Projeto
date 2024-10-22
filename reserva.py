from tinydb import Query

class Reserva:
    def __init__(self, cliente_cpf, pousada_id, diaCheckin, diaCheckout, numeroDePessoas, preco, metodoPagamento, db):
        self.cliente_cpf = cliente_cpf
        self.pousada_id = pousada_id
        self.diaCheckin = diaCheckin
        self.diaCheckout = diaCheckout
        self.numeroDePessoas = numeroDePessoas
        self.preco = preco
        self.metodoPagamento = metodoPagamento
        self.db = db

    def cadastrarReserva(self):
        # Verificar se a pousada está cadastrada
        pousada_existente = self.db.search((Query().idPousada == self.pousada_id) & (Query().tipo == 'pousada'))
        if not pousada_existente:
            return {'message': 'Pousada não cadastrada!'}

        # Verificar se a pousada está disponível
        reservas_existentes = self.db.search((Query().pousada_id == self.pousada_id) & (Query().tipo == 'reserva'))
        for reserva in reservas_existentes:
            # Se as datas da reserva atual estiverem dentro do período de uma reserva existente, a pousada não está disponível
            if not (self.diaCheckout < reserva['diaCheckin'] or self.diaCheckin > reserva['diaCheckout']):
                return {'message': 'A pousada não está disponível nas datas selecionadas!'}

        # Inserir nova reserva no banco de dados
        self.db.insert({
            'tipo': 'reserva',
            'cliente_cpf': self.cliente_cpf,
            'pousada_id': self.pousada_id,
            'diaCheckin': self.diaCheckin,
            'diaCheckout': self.diaCheckout,
            'numeroDePessoas': self.numeroDePessoas,
            'preco': self.preco,
            'metodoPagamento': self.metodoPagamento
        })

        # Atualizar o estado da pousada para indisponível
        self.db.update({'estado': 'indisponível'}, (Query().idPousada == self.pousada_id) & (Query().tipo == 'pousada'))

        return {'reserva_id': self.pousada_id, 'message': 'Reserva cadastrada com sucesso!'}




