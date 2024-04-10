from flask import Flask, request
from file_send import  file_sender
app = Flask(__name__)
UPLOAD_FOLDER = "file_send"
app.config['SERVER_NAME'] = '192.168.0.7:5545'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/<string:channel_id>/', methods=['POST'])
async def upload(channel_id):
    data = request.headers
    auth = data.get('auth')
    try:
        if 'file' not in request.files:
            return 'no file found', 500

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return "files not selected", 500

        uploaded_file.save('file_send/' + uploaded_file.filename)
        send = await file_sender.send_file(channel_id, auth, uploaded_file.filename)
        if(send == 200):
            return "file sent!", 200
        else:
            return "something get wrong", 500

    except:
        return 500
if __name__ == '__main__':
    app.run()