from flask import Blueprint, render_template, redirect, url_for, flash,current_app
from .models import Product, Category
from flask_login import current_user, login_required
from .forms import ProductForm, DeleteForm, LoginForm, RegistrationForm
from werkzeug.utils import secure_filename
from .helper_role import wanner_permission, admin_permission, moderator_permission, edit_permission, view_permission, create_permission, delete_permission, moderator_permission
from . import db_manager as db
import uuid
import os


# Blueprint
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)

@main_bp.route('/')
def init():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.product_list'))
    else:
        return redirect(url_for("auth_bp.login"))
    return redirect(url_for('main_bp.product_list'))


@main_bp.route('/products/list')
def product_list():
    # select amb join que retorna una llista dwe resultats
    products_with_category = db.session.query(Product, Category).join(Category).order_by(Product.id.asc()).all()

    return render_template('layout.html', products_with_category = products_with_category)

@main_bp.route('/products/create', methods = ['POST', 'GET'])
@login_required
@create_permission.require(http_exception=403)
def product_create(): 

    # select que retorna una llista de resultats
    categories = db.session.query(Category).order_by(Category.id.asc()).all()

    # carrego el formulari amb l'objecte products
    form = ProductForm()
    form.category_id.choices = [(category.id, category.name) for category in categories]

    if form.validate_on_submit(): # si s'ha fet submit al formulari
        new_product = Product()
        new_product.seller_id = current_user.id # en un el futur tindrà l'id de l'usuari autenticat

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

        # Enviar correo electrónico de bienvenida con el enlace de verificació

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        flash("Nou producte creat", "success")
        return redirect(url_for('main_bp.product_list'))
    else: # GET
        return render_template('products/create.html', form = form)

@main_bp.route('/products/read/<int:product_id>')
@login_required
@view_permission.require(http_exception=403)
def product_read(product_id):
    # select amb join i 1 resultat
    (product, category) = db.session.query(Product, Category).join(Category).filter(Product.id == product_id).one()
    
    return render_template('products/read.html', product = product, category = category)

@main_bp.route('/products/update/<int:product_id>',methods = ['POST', 'GET'])
@login_required
@edit_permission.require(http_exception=403)
def product_update(product_id):
    # select amb 1 resultat
    product = db.session.query(Product).filter(Product.id == product_id).one()

    if current_user.id != product.seller_id:
        flash('No tienes permisos para editar este producto.', 'error')
        return redirect(url_for('main_bp.product_read', product_id=product_id))
    
    # select que retorna una llista de resultats
    categories = db.session.query(Category).order_by(Category.id.asc()).all()

    # carrego el formulari amb l'objecte products
    form = ProductForm(obj = product)
    form.category_id.choices = [(category.id, category.name) for category in categories]

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
        return redirect(url_for('main_bp.product_read', product_id = product_id))
    else: # GET
        return render_template('products/update.html', product_id = product_id, form = form)

@main_bp.route('/products/delete/<int:product_id>',methods = ['GET', 'POST'])
@login_required
@delete_permission.require(http_exception=403)
def product_delete(product_id):
    # select amb 1 resultat
    product = db.session.query(Product).filter(Product.id == product_id).one()

    form = DeleteForm()
    if form.validate_on_submit(): # si s'ha fet submit al formulari
        # delete!
        db.session.delete(product)
        db.session.commit()

        flash("Producte esborrat", "success")
        return redirect(url_for('main_bp.product_list'))
    else: # GET
        return render_template('products/delete.html', form = form, product = product)



def __manage_photo_file(photo_file):    
    # si hi ha fitxer
    if photo_file.data:
        filename = photo_file.data.filename.lower()

        # és una foto
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            # M'asseguro que el nom del fitxer és únic per evitar col·lissions
            unique_filename = str(uuid.uuid4())+ "-" + secure_filename(filename)
            photo_file.data.save(current_app.config['UPLOADS_FOLDER'] + unique_filename)
            return unique_filename

    return None
