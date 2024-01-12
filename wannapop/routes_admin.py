from flask import Blueprint, render_template, abort, redirect, url_for, flash, current_app
from flask_login import current_user
from .models import User
from .helper_role import Role, role_required
from . import db_manager as db
from .forms import ConfirmForm, BlockedUserForm, BanProductForm
from .models import User, BlockedUser, Product, BannedProduct

# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = db.session.query(User).all()
    blocked_users = [user.user_id for user in db.session.query(BlockedUser).all()]
    return render_template('admin/users_list.html', users=users, blocked_users = blocked_users)

@admin_bp.route('/admin/users/block', methods=['GET', 'POST'])
@role_required(Role.admin)
def block_user():
    form = BlockedUserForm()

    # Obtén todos los usuarios para llenar la lista desplegable
    users = User.query.filter(User.id.notin_(BlockedUser.query.with_entities(BlockedUser.user_id))).all()

    # Llena la lista desplegable con el nombre de usuario y su correo electrónico
    form.user_id.choices = [(user.id, f'{user.name} - ({user.email})') for user in users]

    if form.validate_on_submit():
        new_blockeduser = BlockedUser()
        new_blockeduser.admin_id = current_user.id
        form.populate_obj(new_blockeduser)

        # insert!
        db.session.add(new_blockeduser)
        db.session.commit()
        flash(f"[{new_blockeduser.user_id}] Usuari bloquejat", "success")
        return redirect(url_for('admin_bp.admin_users'))
    return render_template('admin/block_user.html', form=form)

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods = ['POST', 'GET'])
@role_required(Role.admin)
def unblock_user(user_id):
        user = db.session.query(BlockedUser).filter(BlockedUser.user_id == user_id).one_or_none()
        
        db.session.delete(user)
        db.session.commit()

        flash(f"[{user.user_id}] Usuari desbloquejat", "success")
        return redirect(url_for('admin_bp.admin_users'))

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=["GET", "POST"])
@role_required(Role.moderator)
def ban_product(product_id):
    result = db.session.query(Product, BannedProduct).outerjoin(BannedProduct).filter(Product.id == product_id).one_or_none()
    if not result:
        abort(404)
    
    (product, banned) = result

    if banned:
        flash("Producte ja prohibit", "error")
        return redirect(url_for('products_bp.product_list'))

    form = BanProductForm()
    if form.validate_on_submit():
        new_banned = BannedProduct();
        # carregar dades de la URL
        new_banned.product_id = product.id
        # carregar dades del formulari
        form.populate_obj(new_banned)
        # insert!
        db.session.add(new_banned)
        db.session.commit()
        # retornar al llistat
        flash("Producte prohibit", "success")
        return redirect(url_for('products_bp.product_list'))

    return render_template('admin/products/ban.html', product=product, form=form)

@admin_bp.route('/admin/products/<int:product_id>/unban', methods=["GET", "POST"])
@role_required(Role.moderator)
def unban_product(product_id):
    result = db.session.query(Product, BannedProduct).outerjoin(BannedProduct).filter(Product.id == product_id).one_or_none()
    if not result:
        abort(404)
    
    (product, banned) = result
    
    if not banned:
        flash("Producte no prohibit", "error")
        return redirect(url_for('products_bp.product_list'))
    
    form = ConfirmForm()
    if form.validate_on_submit():
        db.session.delete(banned)
        db.session.commit()
        flash("Producte permès", "success")
        return redirect(url_for('products_bp.product_list'))

    return render_template('admin/products/unban.html', product=product, form=form)

