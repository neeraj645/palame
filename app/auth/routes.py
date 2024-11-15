# app/auth/routes.py

import jwt
from datetime import datetime
from mongoengine import NotUniqueError, ValidationError, DoesNotExist
from app.helper.JWTtoken import generate_jwt_token, decode_jwt_token
from app.schemas import  User
from flask import Blueprint, request, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from app.helper.mailSend import send_verification_email, forget_password_email
from app.helper.handler import error_handler, success_handler
from app.helper.authValidation import  validate_password, validate_signup_data


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # Validate signup data
        is_valid, error_message = validate_signup_data(data)
        if not is_valid:
            return error_handler(error_message, 400)

        # Hash the password
        data["password"] = generate_password_hash(data['password'])

        # Attempt to insert new user
        user = User(**data)
        user.save()

        # Send verification email
        if send_verification_email(data['email']):
            return success_handler({
                'message': 'Signup successful, please check your email for the verification link.',
                'Verification': False
            })
        else:
            return error_handler('Signup successful, but failed to send verification email', 500)

    except NotUniqueError:
        return error_handler("Email or phone number already exists.", 400)
    except ValidationError as e:
        return error_handler(f"Invalid data format: {str(e)}", 400)
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)




# app/auth/routes.py
#login
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Validate login data
        if not data.get('email') or not data.get('password'):
            return error_handler("Email and password are required.", 400)

        # Find user by email
        user = User.objects(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return error_handler("Invalid email or password", 401)

        # Check if email is verified
        if not user.is_verified:
            return error_handler("Please verify your email first.", 403)

        # Generate JWT token
        token = generate_jwt_token({'_id': str(user.id)})

        # print("yooooo")""?
        return success_handler({
            'message': 'Login successful',
            'token': token,
            'role': user.role
        })

    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)
    




@auth_bp.route('/verify-email', methods=['GET'])
def verify_email():
    token = request.args.get('token')

    try:
        # Decode the token to get email
        
        data, error = decode_jwt_token(token)
        # print(error)
        if error:
            return error_handler(error, 400)
        
        # print("email")
        
        email = data['email']
        # Find the user by email
        user = User.objects(email=email).first()
        if not user:
            return error_handler("User not found.", 404)

        # Update the user's verification status
        user.update(set__is_verified=True)

        return success_handler({
            'message': 'Email verified successfully',
            'status': True
        })

    except jwt.ExpiredSignatureError:
        return error_handler("Verification link expired.", 400)
    except jwt.InvalidTokenError:
        return error_handler("Invalid verification link.", 400)
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)






@auth_bp.route('/forget_password', methods=['POST'])
def forget_password():
    try:
        # Extract email from the request data
        email = request.get_json().get("email")

        # Validate email
        if not email:
            return error_handler("Email is required.", 400)

        # Find user by email using MongoEngine
        user = User.objects(email=email).first()
        
        # Check if user exists
        if not user:
            return error_handler(f"{email} is not found.", 404)
        
        # Ensure the email is verified
        if not user.is_verified:
            return error_handler("Please verify this user first.", 403)

        # Send forget password email
        if forget_password_email(email):
            return success_handler({
                'message': 'Password reset link sent successfully. Please check your email to update your password.'
            })
        else:
            return error_handler("Unable to send password reset email.", 500)

    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)






@auth_bp.route('/update_password', methods=['POST'])
def update_password():
    token = request.args.get('token')
    
    try:
        # Decode the token to get email
        data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        current_user = data['email']

        # Extract and validate the new password from request data
        new_password = request.get_json().get('new_password')
        if not new_password:
            return error_handler("New password is required.", 400)
        if not validate_password(new_password):
            return error_handler("Password must be at least 8 characters long and include at least one letter, one number, and one special character.", 400)

        # Hash the new password before storing it
        hashed_password = generate_password_hash(new_password)

        # Update the password in the database
        update_result = User.objects(email=current_user).update_one(set__password=hashed_password,set__updated_at=datetime.utcnow())

        # Check if the password update was successful
        if update_result:
            return success_handler({"message": "Password updated successfully"})
        else:
            return error_handler("Unable to update password.", 400)

    except jwt.ExpiredSignatureError:
        return error_handler("The reset link has expired.", 400)
    except jwt.InvalidTokenError:
        return error_handler("Invalid reset link.", 400)
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)






@auth_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    try:
        user_id = request.get_json().get("user_id")

        # Find the user by ID and Delete
        user = User.objects(id=user_id, is_verified=True).first()
               
        # Check if user exists
        if not user:
            return error_handler("User not found.", 404)

        # Perform delete
        user.delete()

        return success_handler({
            "message": "User deleted successfully"
        }, 200)

    except DoesNotExist:
        return error_handler("User not found.", 404)
    except Exception as e:
        return error_handler(f"An unexpected error occurred: {str(e)}", 500)