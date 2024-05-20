from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from blockchain import Blockchain
import os
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userStorage.db'
app.secret_key = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

blockchain = Blockchain()

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Integer, default=500)
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

        
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
     return redirect('signinOrRegister')


@app.route('/signinOrRegister', methods=['POST', 'GET'])
def signupOrRegister():
    formLogin = LoginForm()
    formRegister = RegisterForm()

    if formLogin.validate_on_submit() and 'submit' in request.form and request.form['submit'] == 'login':
        user = User.query.filter_by(username=formLogin.username.data.lower().strip()).first()
        if user:
            if bcrypt.check_password_hash(user.password, formLogin.password.data.strip()):
                login_user(user)
                return redirect(url_for('homepage'))
            else:
                return render_template('loginPage.html', formLogin=formLogin, formRegister=formRegister, invalid=True, msg="Incorrect Password.")
        else:
            return render_template('loginPage.html', formLogin=formLogin, formRegister=formRegister, invalid=True, msg="User Not Found.")

    if formRegister.validate_on_submit() and 'submit' in request.form and request.form['submit'] == 'register':
        existing_user = User.query.filter_by(username=formRegister.username.data.lower().strip()).first()
        if existing_user:
            return render_template('loginPage.html', formLogin=formLogin, formRegister=formRegister, invalid=True, msg="Account with that username already exists.")
        
        hashed_password = bcrypt.generate_password_hash(formRegister.password.data.strip()).decode('utf-8')
        new_user = User(username=formRegister.username.data.lower().strip(), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('homepage'))

    return render_template('loginPage.html', formLogin=formLogin, formRegister=formRegister)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('signinOrRegister')

@app.route('/homepage', methods=['POST', "GET"])
@login_required
def homepage():
     return render_template('homePage.html', name=current_user.username, balance=current_user.balance)

@app.route('/make/transaction', methods=['POST', "GET"])
@login_required
def make_transaction():

     return render_template('make_transaction.html', name = current_user.username, balance=current_user.balance)

@app.route('/view/blockchain', methods=['POST', "GET"])
@login_required
def view_blockchain():
     blockchain_data = [block.to_dict() for block in blockchain.chain]
     return render_template('blockchainHistory.html', blockchain=blockchain_data)



@app.route('/transactions/new', methods=['POST', "GET"])
@login_required
def new_transaction():

     sender = current_user
     recipient_name = request.form.get('recipient').strip().lower()
     amount_str = request.form.get('amount').strip() 

          

     if not (recipient_name and amount_str):
          return render_template('make_transaction.html', invalid=True, error="All fields must be filled out.", name=sender.username, balance=sender.balance)

     if sender.username == recipient_name:
          return render_template('make_transaction.html', invalid=True, error="Sender and Recipient cannot be the same.", name=sender.username, balance=sender.balance)

     try:
          amount = int(amount_str)
     except ValueError:
          return render_template('make_transaction.html', invalid=True, error="Invalid amount entered.", name=sender.username, balance=sender.balance)

     if amount <= 0:
          return render_template('make_transaction.html', invalid=True, error="Invalid amount entered.", name=sender.username, balance=sender.balance)

     recipient = User.query.filter_by(username=recipient_name.strip()).first()

     if not recipient:
          return render_template('make_transaction.html', invalid=True, error="Recipient not found in system.", name=sender.username, balance=sender.balance)

     if sender.balance < amount:
          return render_template('make_transaction.html', invalid=True, error="Not enough balance available in account.", name=sender.username, balance=sender.balance)

     sender.balance -= amount
     recipient.balance += amount

     blockchain.add_transaction(sender.username, recipient.username, amount)

     
     blockchain.add_block()

     db.session.commit()  

     return render_template('make_transaction.html', success=True, msg="Transaction successful.", name=sender.username, balance=sender.balance)


if __name__ == "__main__":
     app.run(debug=True)