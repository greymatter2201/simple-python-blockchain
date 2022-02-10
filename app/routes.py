from flask import render_template, redirect, url_for, flash, jsonify, request
from app import app
from app.forms import transactionForm, balanceForm, genForm
from .blockchain import Blockchain


blockchain = Blockchain()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

@app.route('/transactions', methods=['GET', 'POST'])
def transfer():
    form = transactionForm()
    if form.validate_on_submit():
        password, recipient, amount = form.password.data, form.recipient.data, form.amount.data

        if not blockchain.new_transactions(password, recipient, amount):
            flash("Wrong password?", "errors")
            return redirect(url_for('transfer'))

        blockchain.mine()
        flash("Transferred!", "transactions")
        return redirect(url_for('transfer'))
    return render_template('form.html', title="Transactions", form=form)

@app.route('/chain', methods=['GET'])
def chain():
    chain = blockchain.chain
    return render_template('chain.html', chain=chain)

@app.route('/generate', methods=["GET", "POST"])
def generate():
    form = genForm()
    if form.validate_on_submit():
        password = form.password.data
        keys = blockchain.generate_keys(password)
        keys = keys.splitlines()[1].decode()
        flash("\".PEM file\" loaded onto current directory", "generate")
        return render_template("generate.html", keys=keys, form=form)
    return render_template("generate.html", form=form)

@app.route('/balance', methods=["GET", "POST"])
def balance():
    form = balanceForm()
    global_balances = blockchain.global_balances
    if form.validate_on_submit():
        address = form.address.data
        balance = global_balances[address]
        return render_template("balance.html", balance=balance, address=address, form=form)
    return render_template("balance.html", form=form)
