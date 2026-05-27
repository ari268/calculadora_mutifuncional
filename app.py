from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# =========================
# CONFIG MYSQL
# =========================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:81218515@localhost/calculadora_web"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# MODEL
# =========================


class Historico(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    tipo = db.Column(db.String(50), nullable=False)

    valores = db.Column(db.String(255), nullable=False)

    resultado = db.Column(db.String(255), nullable=False)

    data = db.Column(db.DateTime, default=datetime.utcnow)


# =========================
# CALCULADORA SIMPLES
# =========================


def calculadora_simples(operacao, num1, num2):

    operacoes = {
        "soma": num1 + num2,
        "subtracao": num1 - num2,
        "multiplicacao": num1 * num2,
    }

    if operacao == "divisao":

        if num2 == 0:
            return {"erro": "Não é possível dividir por zero"}

        return {"resultado": round(num1 / num2, 2)}

    if operacao not in operacoes:

        return {"erro": "Operação inválida"}

    return {"resultado": round(operacoes[operacao], 2)}


# =========================
# PORCENTAGEM
# =========================


def calculadora_porcentagem(valor, percentual):

    resultado = (valor * percentual) / 100

    return {"resultado": round(resultado, 2)}


# =========================
# IMC
# =========================


def calculadora_imc(peso, altura):

    if altura <= 0:

        return {"erro": "Altura inválida"}

    # Se vier em centímetros
    if altura > 3:
        altura = altura / 100

    imc = peso / (altura**2)

    if imc < 18.5:
        classificacao = "Abaixo do peso"

    elif imc < 25:
        classificacao = "Peso normal"

    elif imc < 30:
        classificacao = "Sobrepeso"

    elif imc < 35:
        classificacao = "Obesidade Grau I"

    elif imc < 40:
        classificacao = "Obesidade Grau II"

    else:
        classificacao = "Obesidade Grau III"

    return {
        "imc": round(imc, 2),
        "classificacao": classificacao,
        "altura_convertida": round(altura, 2),
    }


# =========================
# JUROS SIMPLES
# =========================


def calculadora_juros_simples(capital, taxa, tempo, periodo="meses"):

    # Converte anos para meses
    if periodo == "anos":
        tempo = tempo * 12

    juros = capital * ((taxa / 100) * tempo)

    montante = capital + juros

    return {
        "capital": round(capital, 2),
        "taxa": f"{taxa}% ao mês",
        "tempo": f"{tempo} meses",
        "juros": round(juros, 2),
        "montante": round(montante, 2),
    }


# =========================
# JUROS COMPOSTOS
# =========================


def calculadora_juros_compostos(capital, taxa, tempo, periodo="meses"):

    # Converte anos para meses
    if periodo == "anos":
        tempo = tempo * 12

    montante = capital * ((1 + taxa / 100) ** tempo)

    juros = montante - capital

    return {
        "capital": round(capital, 2),
        "taxa": f"{taxa}% ao mês",
        "tempo": f"{tempo} meses",
        "juros": round(juros, 2),
        "montante": round(montante, 2),
    }


# =========================
# HOME
# =========================


@app.route("/")
def home():

    return render_template("index.html")


# =========================
# CALCULAR
# =========================


@app.route("/calcular", methods=["POST"])
def calcular():

    resultado = None

    try:

        tipo = request.form.get("tipo")

        # =========================
        # CALCULADORA SIMPLES
        # =========================

        if tipo == "simples":

            operacao = request.form.get("operacao")

            num1 = float(request.form.get("num1"))

            num2 = float(request.form.get("num2"))

            resultado = calculadora_simples(operacao, num1, num2)

            valores = f"{num1} | {num2}"

        # =========================
        # PORCENTAGEM
        # =========================

        elif tipo == "porcentagem":

            valor = float(request.form.get("valor"))

            percentual = float(request.form.get("percentual"))

            resultado = calculadora_porcentagem(valor, percentual)

            valores = f"Valor={valor}, " f"Percentual={percentual}%"

        # =========================
        # JUROS SIMPLES
        # =========================

        elif tipo == "juros_simples":

            capital = float(request.form.get("capital"))

            taxa = float(request.form.get("taxa"))

            tempo = float(request.form.get("tempo"))

            periodo = request.form.get("periodo")

            resultado = calculadora_juros_simples(capital, taxa, tempo, periodo)

            valores = (
                f"Capital={capital}, " f"Taxa={taxa}%, " f"Tempo={tempo} {periodo}"
            )

        # =========================
        # JUROS COMPOSTOS
        # =========================

        elif tipo == "juros_compostos":

            capital = float(request.form.get("capital"))

            taxa = float(request.form.get("taxa"))

            tempo = float(request.form.get("tempo"))

            periodo = request.form.get("periodo")

            resultado = calculadora_juros_compostos(capital, taxa, tempo, periodo)

            valores = (
                f"Capital={capital}, " f"Taxa={taxa}%, " f"Tempo={tempo} {periodo}"
            )

        # =========================
        # IMC
        # =========================

        elif tipo == "imc":

            peso = float(request.form.get("peso"))

            altura = float(request.form.get("altura"))

            resultado = calculadora_imc(peso, altura)

            valores = f"Peso={peso}kg, " f"Altura={altura}m"

        else:

            resultado = {"erro": "Tipo inválido"}

            valores = "N/A"

        # =========================
        # SALVAR HISTÓRICO
        # =========================

        novo_historico = Historico(tipo=tipo, valores=valores, resultado=str(resultado))

        db.session.add(novo_historico)

        db.session.commit()

    except Exception as erro:

        resultado = {"erro": str(erro)}

    return render_template("index.html", resultado=resultado)


# =========================
# HISTÓRICO
# =========================


@app.route("/historico")
def historico():

    dados = Historico.query.order_by(Historico.data.desc()).all()

    return render_template("historico.html", dados=dados)


# =========================
# CRIAR TABELAS
# =========================

with app.app_context():
    db.create_all()

# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    app.run(debug=True)
