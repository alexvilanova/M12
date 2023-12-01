from flask import current_app
from flask_login import current_user
from flask_principal import identity_loaded, identity_changed, ActionNeed, RoleNeed, Permission, Identity, AnonymousIdentity
from enum import Enum

class Role(str, Enum):
    wanner    = "wanner"
    moderator = "moderator"
    admin     = "admin"

class Action(str, Enum):
    products_list     = "list products"
    products_create   = "create products"
    products_read     = "view products"
    products_update   = "edit products"
    products_delete   = "delete products"
    # products_moderate = "moderate products"
    categories_list     = "list categories"
    categories_create   = "create categories"
    categories_read     = "view categories"
    categories_update   = "edit categories"
    categories_delete   = "delete categories"
    statuses_list     = "list statuses"
    statuses_create   = "create statuses"
    statuses_read     = "view statuses"
    statuses_update   = "edit statuses"
    statuses_delete   = "delete statuses"

# Wanners poden visualitzar i crear productes
# Wanners poden editar i eliminar els seus productes
# Moderators poden visualitzar i moderar productes
# Admins poden fer de tot
_permissions = {
    Role.wanner: [
        Action.products_list,
        Action.products_create,
        Action.products_read,
        Action.products_update,
        Action.products_delete
    ],
    Role.moderator: [
        Action.products_list,
        Action.products_read,
        # Action.products_moderate
        Action.products_delete # si s'implementa la moderació es treu aquesta línia
    ],
    Role.admin: [
        Action.products_list,
        Action.products_read,
        Action.products_update,
        Action.products_delete,
        # Action.products_moderate,
        Action.categories_list,
        Action.categories_create,
        Action.categories_read,
        Action.categories_update,
        Action.categories_delete,
        Action.statuses_list,
        Action.statuses_create,
        Action.statuses_read,
        Action.statuses_update,
        Action.statuses_delete,
    ],
}

def load_identity_permissions(identity):
    # Afegir rol
    role = identity.user.role
    identity.provides.add(RoleNeed(role))
    # Afegir permisos
    if (_permissions[role]):
        for action in _permissions[role]:
            identity.provides.add(ActionNeed(action))

###########################
# Mètodes Flask-Principal #
###########################

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    # current_user podria ser anonim!
    if hasattr(identity.user, 'role'):
        load_identity_permissions(identity)

def notify_identity_changed():
    # current_user podria ser anonim!
    if hasattr(current_user, 'email'):
        identity = Identity(current_user.email)
    else:
        identity = AnonymousIdentity()
        
    identity_changed.send(current_app._get_current_object(), identity = identity)

##################
# Routes helpers #
##################

# Usage example: 
# @role_required(Role.admin)
def role_required(*roles):
    needs = [RoleNeed(role) for role in roles]
    return Permission(*needs).require(http_exception=403)

# Usage example: 
# @perm_required(Action.products_create)
def perm_required(action):
    return Permission(ActionNeed(action)).require(http_exception=403)
