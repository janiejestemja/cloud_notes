import os

from flask import Blueprint, current_app, flash, jsonify, render_template, request, redirect, send_file, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

imagefiles = Blueprint("imagefiles", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@imagefiles.route("/filesystem/<int:user_id>/img/<filename>")
@login_required
def serve_user_image(user_id, filename):
    # Only allow access to the currently logged-in user's images
    if user_id != current_user.id:
        abort(403)  # Forbidden

    user_img_folder = os.path.join(current_app.root_path, "filesystem", str(user_id), "img")
    file_path = os.path.join(user_img_folder, filename)

    if not os.path.exists(file_path):
        abort(404)  # File not found

    return send_file(file_path)

@imagefiles.route("/imagefiles", methods=["GET", "POST"])
@login_required
def images():
    user_dir = os.path.join(current_app.root_path, "filesystem", str(current_user.id), "img")
    os.makedirs(user_dir, exist_ok=True)  # Ensure the directory exists
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file part.", category="error")
            return redirect(request.url)

        file = request.files["image"]

        if file.filename == "":
            flash("No selected file.", category="error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Calculate current folder size
            folder_size = sum(os.path.getsize(os.path.join(user_dir, f)) for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f)))

            # Maximum allowed storage in bytes (5MB)
            max_storage = 5 * 1024 * 1024

            # Get size of uploaded file
            file.seek(0, os.SEEK_END)  # Move cursor to the end of the file
            file_size = file.tell()    # Get current cursor position
            file.seek(0)               # Reset cursor to the beginning of the file

            # print(file_size)

            if folder_size + file_size > max_storage:
                flash("Storage limit exceeded. Please delete some files.", category="error")
                return redirect(request.url)

            # Save the image file
            file.save(os.path.join(user_dir, filename))
            flash("Image uploaded successfully.", category="success")
            # Optionally, store file path or metadata in the database
        else:
            flash("Invalid file type. Only images are allowed.", category="error")

        return redirect(request.url)

    # Get list of files in the user's img folder
    image_files = os.listdir(user_dir)
    image_files = [(img, f"/filesystem/{current_user.id}/img/{img}") for img in image_files]

    return render_template("imagefiles.html", user=current_user, images=image_files)

@imagefiles.route("/delete-image", methods=["POST"])
@login_required
def delete_image():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    user_img_folder = os.path.join(current_app.root_path, "filesystem", str(current_user.id), "img")
    file_path = os.path.join(user_img_folder, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # Secure deletion - make sure the file is inside the user's directory
    if os.path.commonpath([file_path, user_img_folder]) != user_img_folder:
        return jsonify({"error": "Invalid file path"}), 403

    os.remove(file_path)
    flash("Imagefile deleted.", category="success")
    return jsonify({"success": True}), 200
