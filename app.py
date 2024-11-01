from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from reserva import Reserva
from pousada import Pousada  

app = Flask(__name__)
db = TinyDB('db.json')


@app.route('/')
def formulario_reserva():
    return render_template('formulario_reserva.html')

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


@app.route('/listar_reservas', methods=['GET'])
def listar_reservas():
    reservas = db.search(Query().tipo == 'reserva')  
    return render_template('listar_reservas.html', reservas=reservas)


@app.route('/cadastrar_pousada', methods=['GET', 'POST'])
def cadastrar_pousada():
    if request.method == 'POST':
        nome = request.form.get('nome')
        id_pousada = request.form.get('idPousada')
        pessoas_suportadas = request.form.get('pessoasSuportadas')
        estado = request.form.get('estado')
        preco = request.form.get('preco') 

       
        if not preco or preco.strip() == "":
            return render_template('formulario_pousada.html', error="O campo preço é obrigatório.")
        
        try:
            preco = float(preco) 
        except ValueError:
            return render_template('formulario_pousada.html', error="Preço inválido. Insira um número válido.")

        pousada = Pousada(
            nome=nome,
            idPousada=int(id_pousada),
            estado=estado,
            pessoasSuportadas=int(pessoas_suportadas),
            preco=preco, 
            db=db
        )

        resultado = pousada.cadastrarPousada()
        if 'message' in resultado:
            if resultado['message'] == 'Pousada cadastrada com sucesso!':
                return redirect(url_for('listar_pousadas'))
            else:
                return render_template('formulario_pousada.html', error=resultado['message'])

    return render_template('formulario_pousada.html')

@app.route('/listar_pousadas', methods=['GET'])
def listar_pousadas():
    pousadas = db.search(Query().tipo == 'pousada')  
    return render_template('listar_pousadas.html', pousadas=pousadas)


@app.route('/buscar_pousada', methods=['GET'])
def buscar_pousada():
    pousada_id = request.args.get('pousada_id')
    
  
    pousada_encontrada = db.search(Query().idPousada == int(pousada_id))
    
   
    if pousada_encontrada:
        reservas = db.search(Query().pousada_id == int(pousada_id))
        pousada_encontrada = pousada_encontrada[0]  
    else:
        reservas = []  
        pousada_encontrada = None

    return render_template('listar_reservas.html', reservas=reservas, pousada_encontrada=pousada_encontrada)


@app.route('/buscar_pousada_preco', methods=['GET'])
def buscar_pousada_preco():
    pousada_id = request.args.get('pousada_id')
    
    
    pousada_encontrada = db.search(Query().idPousada == int(pousada_id))
    
    if pousada_encontrada:
        pousada = pousada_encontrada[0]
        return {
            'success': True,
            'nome': pousada['nome'],
            'preco': pousada['preco']  
        }
    else:
        return {'success': False}, 404

if __name__ == '__main__':
    app.run(debug=True)





