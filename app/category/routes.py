from flask import Blueprint, request
from app.schemas import Category
from datetime import datetime
from app.helper.handler import error_handler, success_handler
from mongoengine import NotUniqueError, ValidationError

category_bp = Blueprint('category', __name__)

# Create Category
@category_bp.route('/create', methods=['POST'])
def create_category():
    try:
        data = request.get_json()
        name = data.get('name')

        if not name:
            return error_handler("Category name is required.", 400)
        
        # Save category
        category_val = Category(name=name)
        category_val.save()
        
        return success_handler({"message": "Category created successfully."})
    except NotUniqueError:
        return error_handler("Category already exists.", 400)
    except ValidationError as e:
        return error_handler(f"Invalid data format: {str(e)}", 400)
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)



# Read Categories
@category_bp.route('/list', methods=['GET'])
def read_categories():
    try:
        categories = Category.objects()
        category_list = [{"id": str(cat.id), "name": cat.name} for cat in categories]
        return success_handler({"categories": category_list})
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)



# Update Category
@category_bp.route('/update', methods=['PUT'])
def update_category():
    try:
        data = request.get_json()
        category_id =  data.get('id')
        new_name = data.get('new_name')
    
        # print(category_id, new_name)
        if not new_name:
            return error_handler("New category name is required.", 400)

        category = Category.objects(id=category_id).first()

        if not category:
            return error_handler("Category not found.", 404)

        print("hu")
        Category.objects(id=category_id).update(set__name=new_name,set__updated_at=datetime.utcnow())


        return success_handler({"message": "Category updated successfully."})
    except NotUniqueError:
        return error_handler("A category with that name already exists.", 400)
    except ValidationError as e:
        return error_handler(f"Invalid data format: {str(e)}", 400)
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)



# Delete Category
@category_bp.route('/delete', methods=['DELETE'])
def delete_category():
    try:
        id = request.get_json().get("id")
        category = Category.objects(id=id).first()
        if not category:
            return error_handler("Category not found.", 404)

        category.delete()
        return success_handler({"message": "Category deleted successfully."})
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)
