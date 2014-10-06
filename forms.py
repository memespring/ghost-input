from wtforms import Form, validators, TextField, PasswordField

class SigninForm(Form):

    email = TextField('Email address', [validators.Email()])
    password = PasswordField('Password', [validators.Required()])
