from flask import Flask, render_template, Response, request
from helper import gen_frames
from pytube import YouTube
import os, traceback
from moviepy.editor import *

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('game.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/download', methods=['GET', 'POST'])
def download():
        if request.method == 'POST':
            try:
                print("Downloading video")
                if os.path.exists("./Video/vid.mp4"):
                    os.remove("./Video/vid.mp4")
                YouTube(request.form['url']).streams.get_highest_resolution().download(output_path='./Video', filename='vid.mp4')
                print("Converting to audio")
                video = VideoFileClip(r'./Video/vid.mp4')
                if os.path.exists("./Audio/song.mp3"):
                    os.remove("./Audio/song.mp3")
                video.audio.write_audiofile(r"./Audio/song.mp3")
                print("Complete")
                return render_template('game.html', success="Success")
            except:
                print("Oops, something went wrong. Try again.")
                print(traceback.format_exc())
                return render_template('game.html', error="Something went wrong.")
        elif request.method == 'GET':
            return render_template('game.html')

if __name__ == "__main__":
    app.run()
