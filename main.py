from flask import Flask, render_template, Response
from helper import gen_frames

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run()
