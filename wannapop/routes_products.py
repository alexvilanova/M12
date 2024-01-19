from flask import Blueprint, render_template, redirect, url_for, flash, abort, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import Product, Category, Status, BlockedUser, BannedProduct
from .forms import ProductForm, DeleteForm
from .helper_role import Action, perm_required
from . import db_manager as db
import uuid
import os

# Blueprint
products_bp = Blueprint("products_bp", __name__)

# https://code.tutsplus.com/templating-with-jinja2-in-flask-advanced--cms-25794t
@products_bp.context_processor
def templates_processor():
    return {
        'Action': Action
    }

@products_bp.route('/products/list')
@perm_required(Action.products_list)
def product_list():

    # verifica si el usuario actual esta bloqueado
    user_blocked = BlockedUser.query.filter_by(user_id=current_user.id).first()
    # select amb join que retorna una llista de resultats
    products_with_category = Product.get_all_with_outerjoin()

    return render_template('products/list.html', products_with_category = products_with_category, user_blocked = user_blocked)

@products_bp.route('/products/create', methods = ['POST', 'GET'])
@perm_required(Action.products_create)
def product_create(): 
    blocked_user = BlockedUser.query.filter_by(user_id=current_user.id).first()
    if not blocked_user:
        # selects que retornen una llista de resultats
        
        categories = Category.get_all_with(Category)
        statuses = Status.get_all_with(Status)
        # carrego el formulari amb l'objecte products
        form = ProductForm()
        form.category_id.choices = [(category.id, category.name) for category in categories]
        form.status_id.choices = [(status.id, status.name) for status in statuses]

        if form.validate_on_submit(): # si s'ha fet submit al formulari
            new_product = Product()
            new_product.seller_id = current_user.id

            # dades del formulari a l'objecte product
            form.populate_obj(new_product)

            # si hi ha foto
            filename = __manage_photo_file(form.photo_file)
            if filename:
                new_product.photo = filename
            else:
                new_product.photo = "no_image.png"

            # insert!
            new_product.add()

            # https://en.wikipedia.org/wiki/Post/Redirect/Get
            flash("Nou producte creat", "success")
            return redirect(url_for('products_bp.product_list'))
        else: # GET
            return render_template('products/create.html', form = form)
    else:
        flash("Se te ha restringido la creación de productos", "danger")
        return redirect(url_for('products_bp.product_list'))

@products_bp.route('/products/read/<int:product_id>')
@perm_required(Action.products_read)
def product_read(product_id):
    # select amb join i 1 resultat
    result = Product.get_filtered_by()

    if not result:
        abort(404)

    (product, category, status) = result
    return render_template('products/read.html', product = product, category = category, status = status)

@products_bp.route('/products/update/<int:product_id>',methods = ['POST', 'GET'])
@perm_required(Action.products_update)
def product_update(product_id):
    # select amb 1 resultat
    product = Product.get_filtered_by()
    
    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_update, product):
        abort(403)

    # selects que retornen una llista de resultats
    categories = Category.get_all_with()
    statuses = Status.get_all_with()

    # carrego el formulari amb l'objecte products
    form = ProductForm(obj = product)
    form.category_id.choices = [(category.id, category.name) for category in categories]
    form.status_id.choices = [(status.id, status.name) for status in statuses]

    if form.validate_on_submit(): # si s'ha fet submit al formulari
        # dades del formulari a l'objecte product
        form.populate_obj(product)

        # si hi ha foto
        filename = __manage_photo_file(form.photo_file)
        if filename:
            product.photo = filename

        # update!
        product.add()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        flash("Producte actualitzat", "success")
        return redirect(url_for('products_bp.product_read', product_id = product_id))
    else: # GET
        return render_template('products/update.html', product_id = product_id, form = form)

@products_bp.route('/products/delete/<int:product_id>',methods = ['GET', 'POST'])
@perm_required(Action.products_delete)
def product_delete(product_id):
    # select amb 1 resultat
    product = Product.get_filtered_by(Product)

    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_delete, product):
        abort(403)

    form = DeleteForm()
    if form.validate_on_submit(): # si s'ha fet submit al formulari
        # delete!
        product.remove()

        flash("Producte esborrat", "success")
        return redirect(url_for('products_bp.product_list'))
    else: # GET
        return render_template('products/delete.html', form = form, product = product)

__uploads_folder = os.path.abspath(os.path.dirname(__file__)) + "/static/products/"

def __manage_photo_file(photo_file):
    # si hi ha fitxer
    if photo_file.data:
        filename = photo_file.data.filename.lower()

        # és una foto
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # M'asseguro que el nom del fitxer és únic per evitar col·lissions
            unique_filename = str(uuid.uuid4())+ "-" + secure_filename(filename)
            photo_file.data.save(__uploads_folder + unique_filename)
            return unique_filename

    return None
