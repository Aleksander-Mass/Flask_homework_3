from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import CSRFProtect
from models import db, User
from forms import RegisterForm
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
app.config['SECRET_KEY'] = b"2f32616c75fb81841fed095095851ba931082b35dd21b9a8ceaaa136c51e8595"
csrf = CSRFProtect(app)
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register/", methods=["GET", "POST"])
def login():
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        user = User()
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.email = request.form['email']
        user.password = generate_password_hash(request.form['password'])

        db.session.add(user)
        db.session.commit()
        return render_template('success.html')

    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)