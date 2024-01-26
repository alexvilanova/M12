from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DecimalField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email, Length
import decimal

class LoginForm(FlaskForm):
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        validators=[ DataRequired()]
    )
    submit = SubmitField()

class RegisterForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        validators=[ DataRequired()]
    )
    submit = SubmitField()

class ProfileForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        # no es obligatori canviar-lo
    )
    submit = SubmitField()

class ResendForm(FlaskForm):
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    submit = SubmitField()

class ProductForm(FlaskForm):
    title = StringField(
        validators = [DataRequired()]
    )
    description = StringField(
        validators = [DataRequired()]
    )
    photo_file = FileField()
    price = DecimalField(
        places = 2, 
        rounding = decimal.ROUND_HALF_UP, 
        validators = [DataRequired(), NumberRange(min = 0)]
    )
    category_id = SelectField(
        validators = [InputRequired()]
    )
    status_id = SelectField(
        validators = [InputRequired()]
    )
    submit = SubmitField()

class CategoryForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    slug = StringField(
        validators = [DataRequired()]
    )
    submit = SubmitField()

class StatusForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    slug = StringField(
        validators = [DataRequired()]
    )
    submit = SubmitField()

class BlockedUserForm(FlaskForm):
    user_id = SelectField('User', coerce=int, choices=[], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=255)])

# Formulari generic per esborrar i aprofitar la CSRF Protection
class DeleteForm(FlaskForm):
    submit = SubmitField()

class BanProductForm(FlaskForm):
    reason = StringField(
        validators = [DataRequired()]
    )
    submit = SubmitField()

# Formulari generic per a confirmar una acció
class ConfirmForm(FlaskForm):
    submit = SubmitField()