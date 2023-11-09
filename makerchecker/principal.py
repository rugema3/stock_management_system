from flask_principal import RoleNeed, Principal, Permission, Identity
from flask import session

# Define role needs
admin_role = RoleNeed("admin")
user_role = RoleNeed("user")

principal = Principal(use_sessions=False)  # Disable sessions to use Principal with Flask-Admin

# Define permissions based on roles
admin_permission = Permission(admin_role)
user_permission = Permission(user_role)

# Create an Identity with roles and add permissions to the roles
identity_admin = Identity("admin")
identity_admin.provides.add(admin_role)
identity_admin.provides.add(user_role)  # Optionally, you can assign multiple roles

identity_user = Identity("user")
identity_user.provides.add(user_role)

# Identity loader function to determine the user's identity based on their role
def load_identity():
    user_role = session.get("user_role")
    if user_role == "admin":
        return identity_admin
    else:
        return identity_user

# Manually assign the identity loader to the app
def assign_identity_loader(app):
    app.before_request(load_identity)

# Initialize Principal and assign identities (roles) to users
def init_principal(app):
    principal.init_app(app)
    assign_identity_loader(app)

