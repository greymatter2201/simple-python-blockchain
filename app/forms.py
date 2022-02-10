from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

# DataRequired validatitor checcks that the field is not submitted empty
class transactionForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    recipient = StringField("Recipient", validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    transfer = SubmitField("Transfer")

class genForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    generate = SubmitField("Generate")

class balanceForm(FlaskForm):
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Submit")
