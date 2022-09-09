from app import app
from flask import render_template, flash, send_from_directory, redirect, url_for
from app import app
from app.forms import transactionForm, balanceForm, genForm
from .blockchain import Blockchain

blockchain = Blockchain()

# Route for static items
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.route("/")
@app.route("/home")
def home():
    return render_template('base.html')

@app.route('/transactions')
def transactions():
    chain = blockchain.chain
    return render_template('transactions.html', chain=chain)

@app.route('/transfer', methods=['GET', 'POST'])
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
    return render_template('transfer.html', title="Transactions", form=form)

@app.route('/generate', methods=['GET','POST'])
def generate():
    form = genForm()
    title = "Generate Wallet"
    h1 = "Enter a password for your wallet"
    h2 = "Wallet Created"
    if form.validate_on_submit():
        password = form.password.data
        keys = blockchain.generate_keys(password)
        keys = keys.splitlines()[1].decode()
        flash("\".PEM file\" loaded onto current directory", "generate")
        return render_template("generate.html", keys=keys, form=form, title=title, heading=h2)
    return render_template("generate.html", form=form, title=title, heading=h1)

@app.route('/balance', methods=['GET','POST'])
def balance():
    form = balanceForm()
    try:
        global_balances = blockchain.global_balances
    except KeyError:
        return render_template("balance.html", form=form, title=title, heading=heading)
    title = "Check Balances"
    heading = "Enter a public address"
    if form.validate_on_submit():
        address = form.address.data
        balance = global_balances[address]
        return render_template("balance.html", balance=balance, address=address, form=form, title=title, heading=heading)
    return render_template("balance.html", form=form, title=title, heading=heading)

@app.route('/chain')
def chain():
    title = "Chain"
    heading = "View the Chain"
    chain = blockchain.chain
    return render_template('chain.html', chain=chain, title=title,heading=heading)

