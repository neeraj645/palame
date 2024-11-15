import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secretKey")
    
    # MongoDB URI
    MONGO_URI = "mongodb+srv://shanki645:anruovRKFsriEDKM@cluster0.oeika.mongodb.net/palame"

    # JWT configuration
    JWT_SECRET_KEY = "secretkey"

    # Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'neerajkirar645@gmail.com'
    MAIL_PASSWORD = 'yvlzyzwzifprpkoe'
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/images/product')

