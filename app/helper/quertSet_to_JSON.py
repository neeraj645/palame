

def JSON_convert(products):
    base_url = "http:localhost:5000/images/product/"
    product_list = []
    for product in products:
        product_data = {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "details": product.details,
            "sizes": product.sizes,
            "size_fit": product.size_fit,
            "category_id": str(product.category_id),
            "images": [{"image_url": base_url + img["image_url"]}  for img in product.images],
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
        
        product_list.append(product_data)
    return product_list