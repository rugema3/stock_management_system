from flask import Blueprint, send_file, flash
import subprocess
import os
from decorators.admin_decorators import admin_required
from decorators.authentication_decorators import login_required

backup_route = Blueprint('backup', __name__)

@backup_route.route('/backup', methods=['GET', 'POST'])
@admin_required
def backup():
    """
    Run the database backup script and provide the backup file for download.

    This route triggers the execution of the database backup script, and once
    the backup is complete, it provides the user with the option to download
    the backup file. After the download, a success message is flashed.

    Returns:
        Flask.Response: Flask response object containing the backup file.
    """
    print("Backup route accessed!")
    try:
        # Run the backup script
        subprocess.run(['/home/rugema3/automations/stock_backup.sh'])

        # Compose the path to the backup file
        current_date = subprocess.check_output(['date', '+%d-%m-%Y']).decode().strip()
        database_name = "stock"
        backup_path = "/home/rugema3/db_backups"
        backup_filename = f"{backup_path}/{database_name}-{current_date}.sql.tar.gz"

        # Send the file for download
        response = send_file(backup_filename, as_attachment=True)

        # Flash a success message
        flash('Database backup completed successfully! File downloaded.')

        return response

    except Exception as e:
        # Handle any exceptions and flash an error message
        flash(f'Error: {str(e)}')

    # If an error occurred, you might want to redirect to an error page or another route
    return render_template('error.html')  # Adjust this based on your project structure

