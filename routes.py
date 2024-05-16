from blockchain import Blockchain
from block import Block
from models import User
from flask import Flask, jsonify, request, render_template



def register_routes(app, db):

    blockchain = Blockchain()

    counter = 0
    
    @app.route('/')
    def home():
        return render_template('loginPage.html')
    
    @app.route('/homepage')
    def homepage():
        
        username = request.args.get('name')
        user = User.query.filter_by(username=username).first()

        return render_template('homePage.html', name=username, balance=user.balance)

    @app.route('/signin', methods=['POST'])
    def login():
        
        username = request.form.get('username').strip()

        password = request.form.get('password').strip()

        if not username or not password:
                return render_template('loginPage.html', invalid=True ,error="Username and password fields cannot empty")


        user = User.query.filter_by(username=username).first()

        if not user:
            return render_template('loginPage.html', invalid=True, error="User not found")
        
        if user.password == password:
            return render_template('homePage.html', name=user.username, balance=user.balance)
        else:
            return render_template('loginPage.html', invalid=True ,error="Password was incorrect")


    @app.route('/register', methods=['POST'])
    def register():

        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        if not username or not password:
                return render_template('loginPage.html', invalid=True ,error="Username and password fields cannot empty")

        user = User.query.filter_by(username=username).first()

        if user:
            return render_template('loginPage.html', invalid = True, error="Username already exists")
        

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template("homepage.html", name=username, balance=user.balance)

    @app.route('/make/transaction')
    def make_transaction():
        username = request.args.get('name')

        user = User.query.filter_by(username=username).first()
        return render_template('make_transaction.html', name = user.username, balance=user.balance)

    @app.route('/view/blockchain')
    def view_blockchain():
        blockchain_data = [block.to_dict() for block in blockchain.chain]
        return jsonify(blockchain_data)



    @app.route('/transactions/new', methods=['POST'])
    def new_transaction():
        username = request.args.get('name')  
        recipient_name = request.form.get('recipient')  
        amount_str = request.form.get('amount')  

        if not (username and recipient_name and amount_str):
            return render_template('make_transaction.html', invalid=True, error="All fields must be filled out.", name=sender.username, balance=sender.balance)

        try:
            amount = int(amount_str)
        except ValueError:
            return render_template('make_transaction.html', invalid=True, error="Invalid amount entered.", name=sender.username, balance=sender.balance)

        if amount <= 0:
            return render_template('make_transaction.html', invalid=True, error="Invalid amount entered.", name=sender.username, balance=sender.balance)

        sender = User.query.filter_by(username=username).first()
        recipient = User.query.filter_by(username=recipient_name.strip()).first()

        if not sender:
            return render_template('make_transaction.html', invalid=True, error="Sender not found in system.", name=sender.username, balance=sender.balance)

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


 

