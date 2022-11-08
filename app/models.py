from app.database import db


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(100))
    email = db.Column(db.Text(100))
    phone = db.Column(db.Integer)
