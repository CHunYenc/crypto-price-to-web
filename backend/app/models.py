# from app.extensions import db

# class FocusSymbol(db.Model):
#     __tablename__ = "focus_symbol"
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     exchange = db.Column(db.String(10), nullable=False, default="None")
#     symbol_A = db.Column(db.String(10), nullable=False)
#     symbol_B = db.Column(db.String(10), nullable=False)
#     db.UniqueConstraint(exchange, symbol_A, symbol_B)

# class CryptoPrice(db.Model):
#     __tablename__ = "crypto_price"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     exchange = db.Column(db.String(10), nullable=False)
#     symbol = db.Column(db.String(10), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.utcnow())

#     def __repr__(self):
#         return f"<id:{id}>"
