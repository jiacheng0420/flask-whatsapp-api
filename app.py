from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# 环境变量方式读取（部署到Render时使用）
ACCOUNT_SID = os.getenv('ACCOUNT_SID', 'YOUR_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN', 'YOUR_AUTH_TOKEN')
FROM_WHATSAPP = os.getenv('FROM_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/api/send', methods=['POST'])
def send_message():
    phone = request.form.get('phone')
    message = request.form.get('message')

    if not phone or not message:
        return jsonify({'success': False, 'error': 'Missing phone or message'}), 400

    try:
        msg = client.messages.create(
            from_=FROM_WHATSAPP,
            body=message,
            to=f'whatsapp:{phone}'
        )
        return jsonify({'success': True, 'sid': msg.sid})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
