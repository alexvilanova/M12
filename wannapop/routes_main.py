from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from .forms import ProfileForm
from . import db_manager as db, mail_manager
import secrets

# Blueprint
main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/')
def init():
    if current_user.is_authenticated:
        return redirect(url_for('products_bp.product_list'))
    else:
        return redirect(url_for("auth_bp.login"))
    
@main_bp.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        something_change = False
        new_email = form.email.data
        new_name = form.name.data
        new_password = form.password.data

        if new_email != current_user.email:
            something_change = True
            current_user.email = new_email
            current_user.verified = False
            current_user.email_token = secrets.token_urlsafe(20)

        if new_name != current_user.name:
            something_change = True
            current_user.name = new_name

        if new_password: # not empty
            something_change = True
            current_user.password = new_password

        if not something_change:
            flash("Cap canvi", "success")
        else:
            # guardo els canvis a la bbdd
            db.session.commit()

            if not current_user.verified:
                # envio l'email!
                mail_manager.send_register_email(current_user.name, current_user.email, current_user.email_token)

                # logout
                logout_user()
                flash("Revisa el teu correu per verificar-lo", "success")
                return redirect(url_for("auth_bp.login"))

            flash("Perfil actualitzat correctament", "success")
            
        return redirect(url_for('main_bp.profile'))
    else:
        form.name.data = current_user.name
        form.email.data = current_user.email    

        return render_template('profile.html', form = form)

@main_bp.app_errorhandler(403)
def forbidden_access(e):
  return render_template('403.html',message=e), 403

@main_bp.app_errorhandler(404)
def not_allowed(e):
  return render_template('404.html',message=e), 404