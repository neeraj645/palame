from datetime import datetime
from flask import Blueprint, request
from app import app 
from app.helper.handler import error_handler, success_handler 
from app.helper.productValidation import  product_validation
from app.helper.productHelper import save_images ,build_updated_fields, handle_image_upload
from app.helper.quertSet_to_JSON import  JSON_convert
from mongoengine import NotUniqueError, ValidationError
from app.schemas import Product

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']


product_bp = Blueprint('product', __name__)




@product_bp.route("/add", methods=["POST"])
def add_product():
    data = {
        "name": request.form.get("name"),
        "description": request.form.get("description"),
        "details": request.form.get("details"),
        "sizes": request.form.getlist("sizes"),
        "quantities": request.form.getlist("quantities"),
        "size_fit": request.form.get("size_fit"),
        "category_id": request.form.get("category_id"),
    }
    
    # Transform sizes and quantities into a list of dictionaries
    data["sizes"] = [{"size": size, "quantity": int(quantity)} for size, quantity in zip(data["sizes"], data["quantities"])]
    data.pop("quantities")

    # Validate required fields
    is_valid, error_message = product_validation(data)
    if not is_valid:
        return error_handler(error_message, 400)

    # Check if images are included in the request
    if "images" not in request.files:
        return error_handler("No images provided", 400)

    images = request.files.getlist("images")
    uploaded_images, error = save_images(images, UPLOAD_FOLDER)  # Use the helper function

    if error:
        return error_handler(f"Failed to save images: {error}", 500)

    data["images"] = uploaded_images

    # Insert product entry into MongoDB
    try:
        category_val = Product(**data)
        category_val.save()
        return success_handler({"message": "Product created successfully."})
    except NotUniqueError:
        return error_handler("Product already exists.", 400)
    except ValidationError as e:
        return error_handler(f"Invalid data format: {str(e)}", 400)
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)
   ###########################################################




@product_bp.route("/list", methods=["GET"])
def all_products():
    try:
        # Fetch all products from the database
        products = Product.objects()

        product_list = JSON_convert(products)

        return success_handler({"products": product_list})
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)




# Update Product API route
@product_bp.route("/update", methods=["PUT"])
def update_product():
    try:
        # Fetch the product ID from the request
        product_id = request.form.get("id")
        
        # Find the product by ID
        product = Product.objects(id=product_id).first()
        if not product:
            return error_handler("Product not found.", 404)
        
        # Prepare the updated fields
        updated_fields = build_updated_fields(request.form)
        
        # Handle image upload and add to updated fields
        if "images" in request.files:
            uploaded_images, error = handle_image_upload(request.files)
            if error:
                return error_handler(error, 500)
            updated_fields["images"] = uploaded_images

        # Update the product in the database
        Product.objects(id=product_id).update_one(**updated_fields, set__updated_at=datetime.utcnow())

        return success_handler({"message": "Product updated successfully."})
    except ValueError as e:
        return error_handler(str(e), 400)
    except NotUniqueError:
        return error_handler("A product with that name already exists.", 400)
    except ValidationError as e:
        return error_handler(f"Invalid data format: {str(e)}", 400)
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)




@product_bp.route('/delete', methods=['DELETE'])
def delete_product():
    try:
        id = request.json.get("id")
        product = Product.objects(id=id).first()
        
        if not product:
            return error_handler("Product not found.", 404)

        product.delete()
        return success_handler({"message": "Product deleted successfully."})
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)
