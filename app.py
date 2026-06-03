from flask import Flask, render_template, request
from datetime import datetime, date

# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

app = Flask(__name__)

# =========================
# CONFIG MYSQL
# =========================

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calculadora.db"

# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

# =========================
# MODEL
# =========================


# class Historico(db.Model):

# id = db.Column(db.Integer, primary_key=True)

# tipo = db.Column(db.String(50), nullable=False)

# valores = db.Column(db.String(255), nullable=False)

# resultado = db.Column(db.String(255), nullable=False)

# data = db.Column(db.DateTime, default=datetime.utcnow)

ROTAS_SIGNOS = {
    "Áries": "aries",
    "Touro": "touro",
    "Gêmeos": "gemeos",
    "Câncer": "cancer",
    "Leão": "leao",
    "Virgem": "virgem",
    "Libra": "libra",
    "Escorpião": "escorpiao",
    "Sagitário": "sagitario",
    "Capricórnio": "capricornio",
    "Aquário": "aquario",
    "Peixes": "peixes"
}
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

    resultado = round((valor * percentual) / 100, 2)

    if resultado.is_integer():
        resultado = int(resultado)

    if valor.is_integer():
        valor = int(valor)

    if percentual.is_integer():
        percentual = int(percentual)

    return {"valor": valor, "percentual": percentual, "resultado": resultado}


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


def icone_signo(signo):

    icones = {
        "Áries": "♈",
        "Touro": "♉",
        "Gêmeos": "♊",
        "Câncer": "♋",
        "Leão": "♌",
        "Virgem": "♍",
        "Libra": "♎",
        "Escorpião": "♏",
        "Sagitário": "♐",
        "Capricórnio": "♑",
        "Aquário": "♒",
        "Peixes": "♓",
    }

    return icones.get(signo, "")


# =========================
# CALCULADORA DE IDADE
# =========================


def calcular_idade(data_nascimento):

    nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")

    agora = datetime.now()
    if nascimento > agora:
        return {"erro": "A data de nascimento não pode ser maior que a data atual."}

    diferenca = agora - nascimento

    anos = int(diferenca.days / 365.25)

    meses = int(diferenca.days / 30.44)

    dias = diferenca.days

    horas = int(diferenca.total_seconds() / 3600)

    minutos = int(diferenca.total_seconds() / 60)

    # Próximo aniversário

    hoje = date.today()

    aniversario = date(hoje.year, nascimento.month, nascimento.day)

    if aniversario < hoje:

        aniversario = date(hoje.year + 1, nascimento.month, nascimento.day)

    dias_para_aniversario = (aniversario - hoje).days

    # Dia da semana

    dias_semana = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ]

    dia_semana = dias_semana[nascimento.weekday()]

    # Signo

    dia = nascimento.day
    mes = nascimento.month

    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19):
        signo = "Áries"

    elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20):
        signo = "Touro"

    elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20):
        signo = "Gêmeos"

    elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22):
        signo = "Câncer"

    elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22):
        signo = "Leão"

    elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22):
        signo = "Virgem"

    elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22):
        signo = "Libra"

    elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21):
        signo = "Escorpião"

    elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21):
        signo = "Sagitário"

    elif (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19):
        signo = "Capricórnio"

    elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18):
        signo = "Aquário"

    else:
        signo = "Peixes"

    return {
        "idade": anos,
        "meses_vividos": meses,
        "dias_vividos": dias,
        "horas_vividas": horas,
        "minutos_vividos": minutos,
        "dia_da_semana": dia_semana,
        "signo": f"{icone_signo(signo)} {signo}",
        "rota_signo": ROTAS_SIGNOS[signo],
        "dias_para_aniversario": dias_para_aniversario,
    }


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# descrição signos


@app.route("/signo/<nome>")
def signo(nome):

    return render_template(f"signos/{nome}.html")


# =========================
# HOME
# =========================


@app.route("/")
def home():

    return render_template("index.html")


# =========================
# Sobre a Calculadora


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


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

            res = calculadora_simples(operacao, num1, num2)
            simbolos = {
                "soma": "+",
                "subtracao": "-",
                "multiplicacao": "×",
                "divisao": "÷",
            }

            resultado = {
                "num1": num1,
                "num2": num2,
                "operacao": simbolos.get(operacao, operacao),
                "resultado": (
                    res.get("resultado") if "resultado" in res else res.get("erro")
                ),
            }

            valores = f"{num1} | {num2}"

        # =========================
        # PORCENTAGEM
        # =========================

        elif tipo == "porcentagem":

            valor = float(request.form.get("valor"))

            percentual = float(request.form.get("percentual"))

            res = calculadora_porcentagem(valor, percentual)
            resultado = {
                "valor": valor,
                "percentual": percentual,
                "resultado": (
                    res["resultado"] if "resultado" in res else res.get("erro")
                ),
            }

            valores = f"Value={valor}, " f"Percentual={percentual}%"

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
        # CALCULADORA DE IDADE
        # =========================

        elif tipo == "idade":

            data_nascimento = request.form.get("data_nascimento")

            if not data_nascimento:
                resultado = {"erro": "Informe uma data de nascimento."}
            else:
                resultado = calcular_idade(data_nascimento)

            valores = f"Data de nascimento={data_nascimento}"
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

        # novo_historico = Historico(tipo=tipo, valores=valores, resultado=str(resultado))

        # db.session.add(novo_historico)

        # db.session.commit()

    except Exception as erro:

        resultado = {"erro": str(erro)}

    return render_template("index.html", resultado=resultado, tipo_resultado=tipo)


# =========================
# HISTÓRICO
# =========================


# @app.route("/historico")
# def historico():

# dados = Historico.query.order_by(Historico.data.desc()).all()

# return render_template("historico.html", dados=dados)


# =========================
# CRIAR TABELAS
# =========================

# with app.app_context():
# db.create_all()

# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    app.run(debug=True)
