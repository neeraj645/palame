from flask import jsonify

def error_handler(message, status_code=400):
    """Send a standardized error response."""
    return jsonify({
        "success": False,
        "error": True,
        "message": message
    }), status_code

def success_handler(data, status_code=200):
    """Send a standardized success response."""
    response = {
        "success": True,
        "error": False
    }
    response.update(data)
    return jsonify(response), status_code
