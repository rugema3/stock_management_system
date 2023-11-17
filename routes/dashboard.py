from flask import Blueprint, render_template
from app.models.database_manager import Database  

admin_bp = Blueprint('admin', __name__)
db_manager = Database()  # Create an instance of your AdminManager or relevant manager

@admin_bp.route('/pending_items')
def pending_items():
    # Retrieve pending items from the manager
    pending_items = db_manager.get_pending_items()

    # Render a template with the pending items
    return render_template('admin/pending_items.html', pending_items=pending_items)
