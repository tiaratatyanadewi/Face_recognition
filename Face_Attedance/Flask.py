import os
from flask import Flask, render_template, Response, jsonify, request
import requests
from flask_socketio import SocketIO
import threading
import socket
from subprocess import Popen

# Import gen_frames from Main.py
from Main import gen_frames

app = Flask(__name__)
socketio = SocketIO(app)

main_started = False

def start_main():
    global main_started
    main_started = True
    print("main.py started")

@socketio.on('start_main')
def handle_start_main():
    global main_started
    if not main_started:
        print("Received request to start main.py")
        start_main()

@app.before_request
def check_start_main():
    global main_started
    if not main_started:
        app.logger.info('Starting main.py in background')
        threading.Thread(target=start_main).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/api/run_script")
def run_script():
    url = request.args.get('url')
    if url:
        response = requests.get(url)
        return jsonify({"data": response.text})
    else:
        return jsonify({"error": "No URL provided"}), 400

# Endpoint to start the Flask server
@app.route("/start_flask_server")
def start_flask_server():
    Popen(['python', 'C:/Users/tiara/OneDrive/Documents/Files/Face_Attendance/Main.py'])  # Start main.py
    return jsonify({"message": "Flask server started"})

@app.route("/start_main_py")
def start_main_py():
    Popen(['python', 'C:/Users/tiara/OneDrive/Documents/Files/Face_Attendance/Main.py'])  # Start Main.py
    return jsonify({"message": "Main.py started"})

def get_ip():
    ip_address = None
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

if __name__ == "__main__":
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
    print(f"Flask app can be accessed at http://{get_ip()}:5000")
