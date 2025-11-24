from flask import Flask, render_template, request, redirect
import redis
from datetime import datetime

app = Flask(__name__)

red = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/') 

def home():
    return render_template('index.html', title='Leo')

@app.route('/enviar', methods=['POST'])


def enviar():

    id = red.incr('id')
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'Pendente'
    

    red.hset(f'tarefa:{id}', 'titulo', titulo)
    red.hset(f'tarefa:{id}', 'descricao', descricao)
    red.hset(f'tarefa:{id}', 'data', dt)
    red.hset(f'tarefa:{id}', 'status', status)
    
    return redirect('/')


@app.route('/buscar', methods=['GET'])
def buscar():
    registro = []

    for chave in red.keys('tarefa:*'):
        dado = red.hgetall(chave)

        dadoDecodificado = {k.decode(): v.decode() for k, v in dado.items()}

        dadoDecodificado['id'] = chave.decode().split(':')[1]
        registro.append(dadoDecodificado)
  
        registro = sorted(registro, key=lambda x: int(x['id']), reverse=True)

    return render_template('index.html', registro=registro)

@app.route('/editar/<id>', methods=['GET'])

def editar(id):
    dado = red.hgetall(f'tarefa:{id}')
    
    dado_decod = {k.decode(): v.decode() for k, v in dado.items()}
    dado_decod['id'] = id
    return render_template('editar.html', dado=dado_decod)


@app.route('/editarDados/<id>', methods=['POST'])

def atualizarDados(id):
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    status = request.form['status']

    red.hset(f'tarefa:{id}', 'titulo', titulo)
    red.hset(f'tarefa:{id}', 'descricao', descricao)
    red.hset(f'tarefa:{id}', 'status', status)

    return redirect('/')

@app.route('/excluir/<id>', methods=['GET'])

def excluir(id):
    red.delete(f'tarefa:{id}')
    return redirect('/')


@app.route('/buscarId', methods=['POST'])

def buscarId():
    id = request.form['id']
    dado = red.hgetall(f'tarefa:{id}')
    
    dado_decod = {k.decode(): v.decode() for k, v in dado.items()}
    dado_decod['id'] = id
    return render_template('index.html', registro=[dado_decod])


if __name__ == '__main__':
    app.run(debug=True)
