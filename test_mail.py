from flask import Flask, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'mail.remmittance.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'developer@remmittance.com'
app.config['MAIL_PASSWORD'] = 'Shami@2020'

@app.route('/')
def index():
    return jsonify({"status": "success", "message": "Welcome to the Flask Mail Test App!"})

@app.route('/send')
def send():
    try:
        msg = Message("Test Email", recipients=["rugema61@gmail.com"])
        msg.body = "This is a test email from Flask Mail."
        mail.send(msg)
        return jsonify({"status": "success", "message": "Email sent successfully!"})
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error sending email: {str(e)}")
        return jsonify({"status": "error", "message": "Failed to send email."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

