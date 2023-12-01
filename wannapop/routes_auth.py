from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user
from . import db_manager as db, login_manager, mail_manager
from .forms import LoginForm, RegisterForm, ResendForm
from .helper_role import notify_identity_changed, Role
from .models import User
import secrets

# Blueprint
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ja està autenticat, sortim d'aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = LoginForm()
    if form.validate_on_submit(): # si s'ha enviat el formulari via POST i és correcte
        email = form.email.data
        password = form.password.data

        user = load_user(email)
        if user and user.check_password(password):
            # si no està verificat, no pot entrar
            if not user.verified:
                flash("Revisa el teu email i verifica el teu compte", "error")
                return redirect(url_for("auth_bp.login"))
            
            # aquí és crea la cookie
            login_user(user)
            # aquí s'actualitzen els rols que té l'usuari
            notify_identity_changed()

            return redirect(url_for("main_bp.init"))

        # si arriba aquí, és que no s'ha autenticat correctament
        flash("Error d'usuari i/o contrasenya", "error")
        return redirect(url_for("auth_bp.login"))
    
    return render_template('login.html', form = form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Si ja està autenticat, sortim d'aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = RegisterForm()
    if form.validate_on_submit(): # si s'ha enviat el formulari via POST i és correcte
        new_user = User()
       
        # dades del formulari a l'objecte new_user
        form.populate_obj(new_user)

        # els nous usuaris tenen role 'wanner'
        new_user.role = Role.wanner

        # els nous usuaris han de verificar l'email
        new_user.verified = False
        new_user.email_token = secrets.token_urlsafe(20)

        # insert!
        db.session.add(new_user)
        db.session.commit()

        # envio l'email!
        mail_manager.send_register_email(new_user.name, new_user.email, new_user.email_token)

        flash("Revisa el teu correu per verificar-lo", "success")
        return redirect(url_for("auth_bp.login"))
    
    return render_template('register.html', form = form)

@auth_bp.route("/verify/<name>/<token>")
def verify(name, token):
    user = db.session.query(User).filter(User.name == name).one_or_none()
    if user and user.email_token == token:
        user.verified = True
        user.email_token = None # esborro el token perquè ja no serveix
        db.session.commit()
        flash("Compte verificat correctament", "success")
    else:
        flash("Error de verificació", "error")
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/resend", methods=["GET", "POST"])
def resend():
    # Si ja està autenticat, sortim d'aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = ResendForm()
    if form.validate_on_submit():
        email = form.email.data
        user = db.session.query(User).filter(User.email == email).one_or_none()
        if user:
            if user.verified:
                flash("Aquest compte ja està verificat", "error")
            else:
                mail_manager.send_register_email(user.name, user.email, user.email_token)
                flash("Revisa el teu correu per verificar-lo", "success")
        else:
            flash("Aquest compte no existeix", "error")
        return redirect(url_for("auth_bp.login"))
    else:
        return render_template('resend.html', form = form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("T'has desconnectat correctament", "success")
    return redirect(url_for("auth_bp.login"))

@login_manager.user_loader
def load_user(email):
    if email is not None:
        # Un resultat o None
        return db.session.query(User).filter(User.email == email).one_or_none()
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash("Autentica't o registra't per accedir a aquesta pàgina", "error")
    return redirect(url_for("auth_bp.login"))
