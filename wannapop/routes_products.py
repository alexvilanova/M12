from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import Product, Category, Status
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
    # select amb join que retorna una llista de resultats
    products_with_category = db.session.query(Product, Category).join(Category).order_by(Product.id.asc()).all()
    
    return render_template('products/list.html', products_with_category = products_with_category)

@products_bp.route('/products/create', methods = ['POST', 'GET'])
@perm_required(Action.products_create)
def product_create(): 

    # selects que retornen una llista de resultats
    categories = db.session.query(Category).order_by(Category.id.asc()).all()
    statuses = db.session.query(Status).order_by(Status.id.asc()).all()

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
        db.session.add(new_product)
        db.session.commit()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        flash("Nou producte creat", "success")
        return redirect(url_for('products_bp.product_list'))
    else: # GET
        return render_template('products/create.html', form = form)

@products_bp.route('/products/read/<int:product_id>')
@perm_required(Action.products_read)
def product_read(product_id):
    # select amb join i 1 resultat
    result = db.session.query(Product, Category, Status).join(Category).join(Status).filter(Product.id == product_id).one_or_none()

    if not result:
        abort(404)

    (product, category, status) = result
    return render_template('products/read.html', product = product, category = category, status = status)

@products_bp.route('/products/update/<int:product_id>',methods = ['POST', 'GET'])
@perm_required(Action.products_update)
def product_update(product_id):
    # select amb 1 resultat
    product = db.session.query(Product).filter(Product.id == product_id).one_or_none()
    
    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_update, product):
        abort(403)

    # selects que retornen una llista de resultats
    categories = db.session.query(Category).order_by(Category.id.asc()).all()
    statuses = db.session.query(Status).order_by(Status.id.asc()).all()

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
        db.session.add(product)
        db.session.commit()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        flash("Producte actualitzat", "success")
        return redirect(url_for('products_bp.product_read', product_id = product_id))
    else: # GET
        return render_template('products/update.html', product_id = product_id, form = form)

@products_bp.route('/products/delete/<int:product_id>',methods = ['GET', 'POST'])
@perm_required(Action.products_delete)
def product_delete(product_id):
    # select amb 1 resultat
    product = db.session.query(Product).filter(Product.id == product_id).one_or_none()

    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_delete, product):
        abort(403)

    form = DeleteForm()
    if form.validate_on_submit(): # si s'ha fet submit al formulari
        # delete!
        db.session.delete(product)
        db.session.commit()

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
