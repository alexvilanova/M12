from flask import Blueprint, current_app
from flask_principal import identity_loaded, identity_changed, ActionNeed, RoleNeed, Permission, Identity, AnonymousIdentity
from flask_login import login_required, current_user
from enum import Enum

# Define custom roles
class Role(str, Enum):
    admin = 'admin'
    moderator = 'moderator'
    wanner = 'wanner'

# Define needs for roles
admin_role_need = RoleNeed(Role.admin)
moderator_role_need = RoleNeed(Role.moderator)
wanner_role_need = RoleNeed(Role.wanner)

# Define permissions based on roles
admin_permission = Permission(admin_role_need)
moderator_permission = Permission(moderator_role_need)
wanner_permission = Permission(wanner_role_need)

# Connect identity_loaded signal to set up roles for the current user
@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'role'):
        if current_user.role == Role.admin:
            identity.provides.add(admin_role_need)
        elif current_user.role == Role.moderator:
            identity.provides.add(moderator_role_need)
        elif current_user.role == Role.wanner:
            identity.provides.add(wanner_role_need)

# # Example routes with role-based permissions
# @main_bp.route('/admin_only')
# @login_required
# @admin_permission.require(http_exception=403)
# def admin_only():
#     return "This page is for admins only."

# @main_bp.route('/moderator_only')
# @login_required
# @moderator_permission.require(http_exception=403)
# def moderator_only():
#     return "This page is for moderators only."

# @main_bp.route('/wanner_only')
# @login_required
# @wanner_permission.require(http_exception=403)
# def wanner_only():
#     return "This page is for wanners only."

# @main_bp.route('/create_product')
# @login_required
# @wanner_permission.require(http_exception=403)
# def create_product():
#     return "This page is for wanners only to create products."
