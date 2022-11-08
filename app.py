from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(100))
    email = db.Column(db.Text(100))
    phone = db.Column(db.Integer)

'''
with app.app_context():
    db.drop_all()
    db.create_all()
'''

@app.get('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.post('/update')
def update():
    employee = Employee.query.get(request.form.get('id'))
    employee.name = request.form.get('name')
    employee.email = request.form.get('email')
    employee.phone = request.form.get('phone')

    db.session.add(employee)
    db.session.commit()
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.post('/insert')
def insert():
    employee = Employee(name=request.form.get('name'), email=request.form.get('email'), phone=request.form.get('phone'))
    db.session.add(employee)
    db.session.commit()
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/delete/<eid>')
def delete_employee(eid):
    db.session.delete(Employee.query.get(eid))
    db.session.commit()
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)