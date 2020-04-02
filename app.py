from flask import Flask, render_template, jsonify, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:L30051992z@localhost:5432/edx_projeto1'
db.init_app(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def index():
    notas = Nota.query.order_by(Nota.pregao.desc()).all()
    return render_template("index.html", notas=notas)


@app.route("/book", methods=["POST"])
def book():
    """Add Trades."""

    # Get form information.
    ativo = request.form.get("ativo")
    nota_id = int(request.form.get("nota_id"))
    qtd = int(request.form.get("qtd"))
    financeiro = float(request.form.get("financeiro"))
    daytrade = request.form.get("daytrade")=='on'

    nota = Nota.query.get(nota_id)

    nota.add_trade(ativo.upper(),qtd,financeiro,daytrade)
    return render_template("success.html")


@app.route("/notas")
def notas():
    """List all flights."""

    notas = Nota.query.all()
    return render_template("flights.html", notas=notas)


@app.route("/nota/<int:nota_id>")
def nota(nota_id):
    """List details about a single flight."""

    # Make sure flight exists.

    nota = Nota.query.get(nota_id)
    if not nota:
        return render_template("error.html", message="No such nota.")

    # Get all passengers.
    trades = nota.trades
    return render_template("flight.html", nota=nota, trades=trades)


@app.route("/api/notas/<int:nota_id>")
def nota_api(nota_id):
    """Return details about a single flight."""

    # Make sure nota exists.
    nota = Nota.query.get(nota_id)
    if not nota:
        return jsonify({"error": "Invalid nota_id"}), 422

    trades_aux = nota.trades
    trades = []
    for trade in trades_aux:
        trades.append(trade.ativo)
    return jsonify({
            "numero": nota.numero,
            "pregao": nota.pregao,
            "financeiro": int(100*nota.valor_operacoes),
            "trades": trades
        })
