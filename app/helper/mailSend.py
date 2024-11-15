
import jwt
from app import mail
from flask_mail import Message
from datetime import datetime, timedelta
from flask import current_app as app, url_for

# Create JWT token valid for 1 hour
def send_verification_email(email):
    token = jwt.encode(
        {'email': email, 'exp': datetime.utcnow() + timedelta(hours=1)},
        app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )   
    # Generate verification link
    link = url_for('auth.verify_email', token=token, _external=True)
    
    print("ms")
    # Configure the email message
    msg = Message('Email Verification Link', sender=app.config['MAIL_USERNAME'], recipients=[email])
    
    # Render the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Email Verification</title>
      <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }}
        .header {{ text-align: center; padding: 20px 0; }}
        .header img {{ width: 100px; height: auto; }}
        .content {{ color: #333333; padding: 20px; }}
        .content h1 {{ font-size: 24px; color: #333333; }}
        .content p {{ font-size: 16px; line-height: 1.5; }}
        .button {{ display: inline-block; margin-top: 20px; padding: 10px 20px; color: white; background-color: paleturquoise; text-decoration: none; border-radius: 5px; font-size: 16px; }}
        .footer {{ margin-top: 30px; font-size: 12px; color: #777777; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbLtNtzuld76UTjHTTqRGCV7jyHP8wcgnT8Q&s" alt="Company Logo">
        </div>
        <div class="content">
          <h1>Verify Your Email</h1>
          <p>Hello,</p>
          <p>Thank you for signing up! Please verify your email address by clicking the button below. This link will expire in 1 hour.</p>
          <a href="{link}" class="button">Verify Email</a>
          <p>If you didn’t create an account with us, please ignore this email.</p>
        </div>
        <div class="footer">
          <p>© 2024 Your Company. All rights reserved.</p>
          <p><a href="#">Privacy Policy</a> | <a href="#">Contact Us</a></p>
        </div>
      </div>
    </body>
    </html>
    """
    
    # Set the HTML content to the message
    msg.html = html_content
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return False








# Create JWT token valid for 1 hour
def forget_password_email(email):
    token = jwt.encode(
        {'email': email, 'exp': datetime.utcnow() + timedelta(hours=1)},
        app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )   
    # Generate verification link
    link = url_for('auth.update_password', token=token, _external=True)
    
    # print("ms")
    # Configure the email message
    msg = Message('Update Password Link', sender=app.config['MAIL_USERNAME'], recipients=[email])
    
    # Render the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Update Password</title>
      <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }}
        .header {{ text-align: center; padding: 20px 0; }}
        .header img {{ width: 100px; height: auto; }}
        .content {{ color: #333333; padding: 20px; }}
        .content h1 {{ font-size: 24px; color: #333333; }}
        .content p {{ font-size: 16px; line-height: 1.5; }}
        .button {{ display: inline-block; margin-top: 20px; padding: 10px 20px; color: white; background-color: paleturquoise; text-decoration: none; border-radius: 5px; font-size: 16px; }}
        .footer {{ margin-top: 30px; font-size: 12px; color: #777777; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbLtNtzuld76UTjHTTqRGCV7jyHP8wcgnT8Q&s" alt="Company Logo">
        </div>
        <div class="content">
          <h1>Update Your Password</h1>
          <p>Hello,</p>
          <p>This is your password update link you can change password by clicking the button below. This link will expire in 1 hour.</p>
          <a href="{link}" class="button">Change Password</a>
          <p>If you didn’t want to update your password, please ignore this mail.</p>
        </div>
        <div class="footer">
          <p>© 2024 Your Company. All rights reserved.</p>
          <p><a href="#">Privacy Policy</a> | <a href="#">Contact Us</a></p>
        </div>
      </div>
    </body>
    </html>
    """
    
    # Set the HTML content to the message
    msg.html = html_content
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return False
