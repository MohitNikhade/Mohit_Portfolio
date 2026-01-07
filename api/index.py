# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import re
# import os
# import logging

# app = Flask(__name__)
# CORS(app)

# logging.basicConfig(level=logging.INFO)

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USER = os.environ.get('EMAIL_USER_NAME')
# EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# # Email validation regex
# EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# def is_valid_email(email):
#     return re.match(EMAIL_REGEX, email) is not None

# def send_email(name, email, message):
#     try:
#         if not EMAIL_USER or not EMAIL_PASSWORD:
#             logging.error("Email credentials not configured")
#             return False

#         msg = MIMEMultipart()
#         msg['From'] = EMAIL_USER
#         msg['To'] = EMAIL_USER
#         msg['Subject'] = f'Portfolio Contact: {name}'
        
#         # Email body
#         body = f"""
#         New contact form submission:
        
#         Name: {name}
#         Email: {email}
#         Message: {message}
        
#         ---
#         Sent from Mohit Portfolio
#         """
        
#         msg.attach(MIMEText(body, 'plain'))
        
#         server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
#         server.starttls()
#         server.login(EMAIL_USER, EMAIL_PASSWORD)
        
#         text = msg.as_string()
#         server.sendmail(EMAIL_USER, EMAIL_USER, text)
#         server.quit()
        
#         logging.info("Email sent successfully")
#         return True
        
#     except Exception as e:
#         logging.error(f"Error sending email: {str(e)}")
#         return False

# @app.route('/')
# def home():
#     return jsonify({
#         "message": "Mohit Portfolio API", 
#         "status": "running",
#         "version": "1.0"
#     })

# @app.route('/api/contact', methods=['POST', 'OPTIONS'])
# def contact():
#     if request.method == 'OPTIONS':
#         return '', 200
        
#     try:
#         data = request.get_json()
        
#         if not data:
#             return jsonify({
#                 "success": False,
#                 "message": "No data provided"
#             }), 400
        
#         name = data.get('name', '').strip()
#         email = data.get('email', '').strip()
#         message = data.get('message', '').strip()
        
#         # Validate fields
#         if not name or not email or not message:
#             return jsonify({
#                 "success": False,
#                 "message": "All fields are required"
#             }), 400
        
#         if not is_valid_email(email):
#             return jsonify({
#                 "success": False,
#                 "message": "Please provide a valid email address"
#             }), 400
        
#         if send_email(name, email, message):
#             return jsonify({
#                 "success": True,
#                 "message": "Thank you for your message! I'll get back to you soon."
#             }), 200
#         else:
#             return jsonify({
#                 "success": False,
#                 "message": "Failed to send message. Please try again later."
#             }), 500
            
#     except Exception as e:
#         logging.error(f"Error in contact endpoint: {str(e)}")
#         return jsonify({
#             "success": False,
#             "message": "An error occurred. Please try again."
#         }), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({
#         "status": "healthy", 
#         "service": "Mohit Portfolio API"
#     })

# if __name__ == '__main__':
#     app.run(debug=True)









from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import os
import logging

app = Flask(__name__)

# Enable CORS for all routes
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Configure logging
logging.basicConfig(level=logging.INFO)

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Email validation regex
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def is_valid_email(email):
    """Validate email format"""
    return re.match(EMAIL_REGEX, email) is not None

def send_email(name, email, message):
    """Send email using SMTP"""
    try:
        # Validate environment variables
        if not EMAIL_USER or not EMAIL_PASSWORD:
            logging.error("Email credentials not configured")
            return False

        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER
        msg['Subject'] = f'Portfolio Contact: {name}'
        
        # Email body
        body = f"""
        New contact form submission from your portfolio:
        
        Name: {name}
        Email: {email}
        Message: {message}
        
        ---
        Sent from Mohit Portfolio Website
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_USER, EMAIL_USER, text)
        server.quit()
        
        logging.info("Email sent successfully")
        return True
        
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return False

@app.route('/')
def home():
    return jsonify({
        "message": "Mohit Portfolio API", 
        "status": "running",
        "version": "1.0"
    })

@app.route('/api/contact', methods=['POST', 'OPTIONS'])
def contact():
    """Handle contact form submission"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        # Log the request
        logging.info(f"Received contact request from {request.remote_addr}")
        
        data = request.get_json()
        
        if not data:
            logging.error("No data provided in request")
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        # Log received data (without sensitive info)
        logging.info(f"Received contact: {name}, {email}, message_length: {len(message)}")
        
        # Validate fields
        if not name or not email or not message:
            logging.error("Missing required fields")
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400
        
        if not is_valid_email(email):
            logging.error(f"Invalid email format: {email}")
            return jsonify({
                "success": False,
                "message": "Please provide a valid email address"
            }), 400
        
        # Check if email credentials are set
        if not EMAIL_USER or not EMAIL_PASSWORD:
            logging.error("Email credentials not set in environment variables")
            return jsonify({
                "success": False,
                "message": "Server configuration error. Please contact the administrator."
            }), 500
        
        # Send email
        if send_email(name, email, message):
            logging.info("Email sent successfully")
            return jsonify({
                "success": True,
                "message": "Thank you for your message! I'll get back to you soon."
            }), 200
        else:
            logging.error("Failed to send email")
            return jsonify({
                "success": False,
                "message": "Failed to send message. Please try again later or contact me directly at mohitnikhade14@gmail.com"
            }), 500
            
    except Exception as e:
        logging.error(f"Error in contact endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An internal server error occurred. Please try again later."
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "Mohit Portfolio API",
        "email_configured": bool(EMAIL_USER and EMAIL_PASSWORD)
    })

# Vercel requires the app variable to be named 'app'
app = app
