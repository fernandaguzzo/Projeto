from tinydb import TinyDB, Query

class Reserva:
    def __init__(self, cliente_cpf, pousada_id, diaCheckin, diaCheckout, numeroDePessoas, preco, metodoPagamento, db=None):
        self.cliente_cpf = cliente_cpf
        self.pousada_id = pousada_id
        self.diaCheckin = diaCheckin
        self.diaCheckout = diaCheckout
        self.numeroDePessoas = numeroDePessoas
        self.preco = preco
        self.metodoPagamento = metodoPagamento
        self.db = db

    def cadastrarReserva(self):
        # Verificar se já existe uma reserva para a mesma pousada no mesmo período
        reservas_existentes = self.db.search(Query().pousada_id == self.pousada_id)

        for reserva in reservas_existentes:
            # Verifica se as datas se sobrepõem
            if (self.diaCheckin < reserva['diaCheckout'] and self.diaCheckout > reserva['diaCheckin']):
                return {'message': 'Já existe uma reserva para este quarto neste período!'}

        # Cadastrar a nova reserva
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

        return {'message': 'Reserva cadastrada com sucesso!'}



