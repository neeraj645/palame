# app/__init__.py

from flask import Flask, send_from_directory
from flask_mail import Mail
from config import Config
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
mail = Mail(app)
jwt = JWTManager(app)
CORS(app)

# Register Blueprints
from .auth.routes import auth_bp
from .product.routes import product_bp
from .category.routes import category_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(category_bp, url_prefix='/category')



@app.route('/images/product/<filename>')
def product_image(filename):
    # Adjust the path to the static folder relative to the __init__.py file
    return send_from_directory(os.path.join(app.root_path, '../static/images/product'), filename)
