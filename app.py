from flask import Flask, request, jsonify
import pywhatkit as kit
import os  # For getting Heroku's PORT environment variable

app = Flask(__name__)

@app.route('/send_order_notification', methods=['POST'])
def send_order_notification():
    data = request.json
    phone_number = data.get('phoneNumber')
    message = data.get('orderDetails')
    
    if phone_number and message:
        # Get the current time and add 2 minutes
        current_time = datetime.now()
        send_time = current_time + timedelta(minutes=2)
        
        # Extract the hour and minute from the calculated time
        hour = send_time.hour
        minute = send_time.minute
        
        # Send message using PyWhatKit
        kit.sendwhatmsg(phone_number, message, hour, minute)  # Send the message 2 minutes from now
        
        return jsonify({"status": "success", "message": f"Message scheduled to {phone_number} at {hour}:{minute}"}), 200
    else:
        return jsonify({"status": "error", "message": "Missing phone number or message"}), 400

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)  # Get the Heroku port or use 5000 for local testing
    app.run(host='0.0.0.0', port=port)  # Bind to all available IPs
