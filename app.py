from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from reserva import Reserva
from pousada import Pousada  # Certifique-se de que a classe Pousada já está implementada

app = Flask(__name__)
db = TinyDB('db.json')

# Rota para o formulário de reserva
@app.route('/')
def formulario_reserva():
    return render_template('formulario_reserva.html')

# Rota para cadastrar uma reserva
@app.route('/cadastrar_reserva', methods=['POST'])
def cadastrar_reserva():
    nome_cliente = request.form.get('nomeCompleto')
    cpf = request.form.get('cpf')
    pousada_id = request.form.get('pousadaId')
    dia_checkin = request.form.get('diaCheckin')
    dia_checkout = request.form.get('diaCheckout')
    numero_pessoas = request.form.get('quantidade')
    preco = request.form.get('valor')
    metodo_pagamento = request.form.get('metodoPagamento')

    reserva = Reserva(
        cliente_cpf=cpf,
        pousada_id=int(pousada_id),
        diaCheckin=dia_checkin,
        diaCheckout=dia_checkout,
        numeroDePessoas=int(numero_pessoas),
        preco=float(preco),
        metodoPagamento=metodo_pagamento,
        db=db
    )

    resultado = reserva.cadastrarReserva()
    if 'reserva_id' in resultado:
        return redirect(url_for('listar_reservas'))
    else:
        return render_template('formulario_reserva.html', error=resultado['message'])

# Rota para listar reservas
@app.route('/listar_reservas', methods=['GET'])
def listar_reservas():
    reservas = db.search(Query().tipo == 'reserva')  # Busca todas as reservas no banco
    return render_template('listar_reservas.html', reservas=reservas)

# Rota para o formulário de cadastro de pousada
# Rota para o formulário de cadastro de pousada
@app.route('/cadastrar_pousada', methods=['GET', 'POST'])
def cadastrar_pousada():
    if request.method == 'POST':
        nome = request.form.get('nome')
        id_pousada = request.form.get('idPousada')
        pessoas_suportadas = request.form.get('pessoasSuportadas')
        estado = request.form.get('estado')

        pousada = Pousada(
            nome=nome,
            idPousada=int(id_pousada),
            estado=estado,
            pessoasSuportadas=int(pessoas_suportadas),
            db=db
        )

        resultado = pousada.cadastrarPousada()
        if 'message' in resultado:
            if resultado['message'] == 'Pousada cadastrada com sucesso!':
                return redirect(url_for('listar_pousadas'))  # Redireciona para a lista de pousadas
            else:
                return render_template('formulario_pousada.html', error=resultado['message'])

    return render_template('formulario_pousada.html')


# Rota para listar pousadas
@app.route('/listar_pousadas', methods=['GET'])
def listar_pousadas():
    pousadas = db.search(Query().tipo == 'pousada')  # Busca todas as pousadas no banco
    return render_template('listar_pousadas.html', pousadas=pousadas)

# Rota para buscar pousada pelo ID nas reservas
@app.route('/buscar_pousada', methods=['GET'])
def buscar_pousada():
    pousada_id = request.args.get('pousada_id')
    
    # Busca a pousada pelo ID
    pousada_encontrada = db.search(Query().idPousada == int(pousada_id))
    
    # Busca as reservas relacionadas a esta pousada
    if pousada_encontrada:
        reservas = db.search(Query().pousada_id == int(pousada_id))
        pousada_encontrada = pousada_encontrada[0]  # Obtém o primeiro resultado
    else:
        reservas = []  # Se a pousada não for encontrada, não há reservas
        pousada_encontrada = None

    return render_template('listar_reservas.html', reservas=reservas, pousada_encontrada=pousada_encontrada)

if __name__ == '__main__':
    app.run(debug=True)


