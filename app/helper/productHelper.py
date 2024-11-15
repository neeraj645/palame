# app/helper/product_helpers.py
import os
import uuid
from bson import ObjectId
from werkzeug.utils import secure_filename
from flask import current_app
from app import app
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

def save_images(images, upload_folder):
    """Save images with unique names and return a list of image URLs."""
    uploaded_images = []

    for image in images:
        # Generate a unique name for each image
        unique_name = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
        image_path = os.path.join(upload_folder, unique_name)

        try:
            # Save image to the specified folder
            image.save(image_path)
            uploaded_images.append({"image_url": unique_name})
        except Exception as e:
            # Log the error and return None if saving fails
            current_app.logger.error(f"Failed to save image {image.filename}: {e}")
            return None, str(e)  # Return None and error message in case of failure

    return uploaded_images, None  # Return the list and None for no error

# Helper function to build updated fields dictionary
def build_updated_fields(data):
    updated_fields = {}
    
    # Simple fields
    simple_fields = ["name", "description", "details", "size_fit"]
    for field in simple_fields:
        if field in data:
            updated_fields[field] = data.get(field)
    
    # Category ID with validation
    if "category_id" in data:
        try:
            updated_fields["category_id"] = ObjectId(data.get("category_id"))
        except Exception:
            raise ValueError("Invalid category ID format.")

    # Sizes field as list of dictionaries
    if "sizes" in data and "quantities" in data:
        sizes = data.getlist("sizes")
        quantities = data.getlist("quantities")
        updated_fields["sizes"] = [{"size": size, "quantity": int(quantity)} for size, quantity in zip(sizes, quantities)]
    
    return updated_fields

# Helper function to handle image upload
def handle_image_upload(files):
    images = files.getlist("images")
    if not images:
        return None, None
    
    uploaded_images, error = save_images(images, UPLOAD_FOLDER)
    if error:
        raise ValueError(f"Failed to save images: {error}")
    
    return uploaded_images, None
