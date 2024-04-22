from flask_wtf import FlaskForm
import wtforms
import wtforms.validators

class Login(FlaskForm):
    username  = wtforms.StringField(validators=wtforms.validators.DataRequired)
    password = wtforms.PasswordField(validators=wtforms.validators.DataRequired)
    submit = wtforms.SubmitField()