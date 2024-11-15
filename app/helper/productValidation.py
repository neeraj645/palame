from flask import jsonify 

def product_validation(data):
    # Validate each field
    if not data['name'] or len(data["name"]) < 3:
        return False,"Product name is required and must be at least 3 characters long."

    if not data["description"] or len(data["description"]) < 10:
        return False, "Product description is required and must be at least 10 characters long."

    if not data["details"] or len(data["details"]) < 5:
        return False,"Product details are required and must be at least 5 characters long."

    if not data['sizes']:
        return False,"At least one size is required, and sizes cannot be empty."

    if not data['size_fit']:
        return False,"Size fit information is required."

    if not data['category_id']:
        return False,"Category ID is required."

    
    # If no errors, return None to indicate successful validation
    # print("jii")
    return True, None