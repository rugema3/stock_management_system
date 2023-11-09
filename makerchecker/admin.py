from flask import Blueprint, render_template
from flask_admin import Admin, BaseView, expose
from flask_principal import Permission

admin_bp = Blueprint("makerchecker_admin", __name__)

# Define a Flask-Principal permission
admin_permission = Permission("admin")

class MakerCheckerAdminView(BaseView):
    @expose('/')
    @admin_permission.require(http_exception=403)  # Only admins can access this view
    def index(self):
        return self.render("admin/index.html")

# Initialize Flask-Admin
def init_admin(app):
    admin = Admin(app, name="Maker-Checker Admin", template_mode="bootstrap3")

    # Add your models and views to the admin panel here
    # For example, you can add views to manage users, view logs, and more.

    # Add the MakerCheckerAdminView to the admin panel
    admin.add_view(MakerCheckerAdminView(name="Maker-Checker", endpoint="maker_checker_admin"))
