from flask import Flask, render_template, request
from simulador import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/simulador1', methods=['POST'])
def calcular_simulador1():
    lambda_ = int(request.form.get('lamb'))
    mi_ = int(request.form.get('mi'))
    simulation_total_time = int(request.form.get('total_time'))
    sample_size = int(request.form.get('sample_size'))
    deterministic = bool(int(request.form.get('deterministic')))
    initial_customers = int(request.form.get('initial_customers'))

    data = rodadas_simulacao(
        lambda_, mi_, simulation_total_time, sample_size, deterministic, initial_customers, simulador_1)

    return data


@app.route('/simulador2', methods=['POST'])
def calcular_simulador2():
    lambda_ = int(request.form.get('lamb'))
    mi_ = int(request.form.get('mi'))
    simulation_total_time = int(request.form.get('total_time'))
    sample_size = int(request.form.get('sample_size'))
    deterministic = bool(int(request.form.get('deterministic')))
    initial_customers = int(request.form.get('initial_customers'))

    data = rodadas_simulacao(
        lambda_, mi_, simulation_total_time, sample_size, deterministic, initial_customers, simulador_2)

    return data


if __name__ == '__main__':
    app.run(debug=True)
