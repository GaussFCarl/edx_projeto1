from flask import Flask, render_template, jsonify, request
from models import *

app = Flask(__name__)
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:L30051992z@localhost:5432/edx_projeto1'
db.init_app(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def index():
    notas = Nota.query.order_by(Nota.pregao.desc()).all()
    return render_template("index.html", notas=notas)


@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    # Get form information.
    ativo = request.form.get("ativo")
    nota_id = int(request.form.get("nota_id"))
    qtd = int(request.form.get("qtd"))
    financeiro = float(request.form.get("financeiro"))
    daytrade = request.form.get("daytrade")=='on'

    nota = Nota.query.get(nota_id)

    nota.add_trade(ativo.upper(),qtd,financeiro,daytrade)
    return render_template("success.html")


@app.route("/flights")
def flights():
    """List all flights."""

    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)


@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """List details about a single flight."""

    # Make sure flight exists.

    flight = Flight.query.get(flight_id)
    if not flight:
        return render_template("error.html", message="No such flight.")

    # Get all passengers.
    passengers = flight.passengers
    return render_template("flight.html", flight=flight, passengers=passengers)


@app.route("/api/flights/<int:flight_id>")
def flight_api(flight_id):
    """Return details about a single flight."""

    # Make sure flight exists.
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"error": "Invalid flight_id"}), 422

    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
            "origin": flight.origin,
            "destination": flight.destination,
            "duration": flight.duration,
            "passengers": names
        })
