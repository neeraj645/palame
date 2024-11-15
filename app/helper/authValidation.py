# app/utils.py

import re


    # At least 8 characters, at least 1 uppercase letter, 1 lowercase letter, and 1 number, 1 special character
def validate_password(password):
    pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$')
    return pattern.match(password)


def validate_signup_data(data):

    # Validate name
    data['name'] = data.get("name", "").strip()
    if len(data["name"]) < 2 or len(data["name"]) > 30:
        return False, "Name length should be between 2 - 30 characters."

    # Validate email
    data['email'] = data.get('email', '').strip()
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", data['email']):
        return False, "Invalid email format."

    # Validate phone number
    data['phone'] = data.get("phone", "").strip()
    if not re.match(r"^\+91[0-9]{10}$", data['phone']):
        return False, "Invalid phone number format. Use +91XXXXXXXXXX."

    # Validate password
    data['password'] = data.get('password', '').strip()
    if len(data['password']) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Za-z]", data['password']):
        return False, "Password must contain at least one letter."
    if not re.search(r"[0-9]", data['password']):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", data['password']):
        return False, "Password must contain at least one special character."

    return True, None  # All validations passed