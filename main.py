from flask import Flask, render_template, request
from flask_restx import Api
from app.config import Config
from app.database import db
from app.models import Employee


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application


def configure_app(application: Flask):
    db.init_app(application)

app_config = Config()
app = create_app(app_config)
configure_app(app)

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
    app.run()

