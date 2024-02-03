from flask import request, render_template, redirect, url_for, flash, Blueprint, current_app, session
from decorators.admin_decorators import admin_required
from werkzeug.utils import secure_filename
import os
import uuid

update_profile_picture_route = Blueprint('update_profile_picture', __name__)

# Absolute path to the upload folder
UPLOAD_FOLDER = '/home/rugema3/stock_management_system/application/static/img/profile_pics'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@update_profile_picture_route.route('/update_profile_picture', methods=['GET', 'POST'])
@admin_required
def update_profile_picture():
    """
    Handle updating user profile pictures.
    """

    user_id = session.get('id')
    user_department = session.get('department')
    user_role = session.get('role')
    extracted_path = session.get('extracted_path')
    print(f'path: {extracted_path}')
    user_handler = current_app.user_handler

    if request.method == 'POST':
        profile_picture_file = request.files['profile_picture']
        
        if profile_picture_file.filename == '':
            flash('No file selected for uploading.', 'error')
            return redirect(url_for('profile'))

        if profile_picture_file and allowed_file(profile_picture_file.filename):
            # Generate a random part using uuid
            random_part = str(uuid.uuid4())[:4]
           
            # Construct file path
            filename = f"{user_id}_{random_part}_{secure_filename(profile_picture_file.filename)}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            # Save uploaded file
            profile_picture_file.save(filepath)

            if user_handler.update_profile_picture(user_id, filename, filepath):
                # Return success message
                flash('Profile picture uploaded successfully.', 'success')
            else:
                flash('Failed to update profile picture.', 'error')
        else:
            flash('Invalid file format. Allowed formats are jpg, jpeg, png, gif.', 'error')

        return redirect(url_for('admin'))
    else:
        return render_template('upload_profile_picture.html', extracted_path=extracted_path, user_id=user_id, user_department=user_department, user_role=user_role)

