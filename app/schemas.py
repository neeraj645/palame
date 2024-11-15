from mongoengine import Document, StringField, BooleanField, DateTimeField, connect, DictField,\
    ListField, EmbeddedDocument, EmbeddedDocumentField,   ReferenceField
import datetime
from config import Config
connect(host = Config.MONGO_URI)


class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True)
    password = StringField(required=True)
    status = BooleanField(default=True)
    is_verified = BooleanField(default=False)
    role = StringField(default="user")
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)


class Category(Document):
    name = StringField(required=True, unique=True)
    status = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'category'}
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)
    
    
class Image(EmbeddedDocument):
    image_url = StringField(required=True)

class Product(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    details = StringField(required=True)
    sizes = ListField(DictField(), required=True)
    size_fit = StringField(required=True)
    category_id = ReferenceField('Category', required=True)  # Assuming Category is another Document
    images = ListField(EmbeddedDocumentField(Image), default=[])
    status = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'product'  # MongoDB collection name
    }