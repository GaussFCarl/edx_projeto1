import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Flight(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    passengers = db.relationship("Passenger", backref="flight", lazy=True)

    def add_passenger(self, name):
        p = Passenger(name=name, flight_id=self.id)
        db.session.add(p)
        db.session.commit()


class Passenger(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)


class Nota(db.Model):
    __tablename__ = "notas"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    pregao= db.Column(db.Date, nullable=False)
    data_liquidacao = db.Column(db.Date, nullable=False)
    custo_xp = db.Column(db.Numeric(10, 2), default = 0.00)
    custo_outro = db.Column(db.Numeric(10, 2), default = 0.00)
    valor_operacoes = db.Column(db.Numeric(10, 2), nullable=False)
    trades = db.relationship("Trade", backref="nota", lazy=True)

    def add_trade(self, ativo,qtd,financeiro,daytrade):
        t = Trade(ativo=ativo, nota_id=self.id,qtd=qtd,financeiro=financeiro,daytrade=daytrade)
        db.session.add(t)
        db.session.commit()

class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True)
    nota_id = db.Column(db.Integer, db.ForeignKey("notas.id"), nullable=False)
    ativo = db.Column(db.String(10), nullable=False)
    qtd = db.Column(db.Integer, nullable=False)
    financeiro = db.Column(db.Numeric(10, 2), nullable=False)
    daytrade = db.Column(db.Boolean, default = False , nullable=False)


