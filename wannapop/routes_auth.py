from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import User
from .forms import LoginForm, RegistrationForm
from . import db_manager as db
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ja està autenticat, sortim d'aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = LoginForm()
    if form.validate_on_submit(): # si s'ha enviat el formulari via POST i és correcte
        email = form.email.data
        plain_text_password = form.password.data

        user = load_user(email)
        if user and check_password_hash(user.password, plain_text_password):
            # aquí és crea la cookie
            login_user(user)
            flash("Se ha iniciado sesión correctamente", "success")
            return redirect(url_for("main_bp.init"))

        # si arriba aquí, és que no s'ha autenticat correctament
        flash("Credenciales incorrectas", "error")

        return redirect(url_for("auth_bp.login"))
    
    return render_template('auth/login.html', form = form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data

        # Verifica si el correo ya está en uso
        existing_user = db.session.query(User).filter_by(email=email).first()

        if existing_user:
            flash('El correo ya está en uso', 'error')
            return render_template('auth/register.html', form=form)
        else:
            # Crea el nuevo usuario y almacena con generate_password_hash
            new_user = User(
                name=form.name.data,
                email=email,
                password=generate_password_hash(form.password.data, method='sha256')
                )
            
            # Guarda el nuevo usuario en la base de datos
            db.session.add(new_user)
            db.session.commit()

            flash('Te has registrado con éxito. Por favor, inicia sesión.', 'success')
            return redirect(url_for('auth_bp.login'))

    return render_template('auth/register.html', form=form)

@login_manager.user_loader
def load_user(email):
    if email is not None:
        # select amb 1 resultat o cap
        user_or_none = db.session.query(User).filter(User.email == email).one_or_none()
        return user_or_none
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))