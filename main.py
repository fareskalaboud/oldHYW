from flask import Flask, render_template, Response, request
from helper import gen_frames
from pytube import YouTube
import os
import traceback
from moviepy.editor import *
from youtubesearchpython import VideosSearch
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def hello():
    return render_template('game.html')


@app.route("/ar/how-it-works")
def howitoworks_ar():
    return render_template('ar-how-it-works.html')


@app.route("/en/how-it-works")
def howitworks_en():
    return render_template('en-how-it-works.html')


@app.route("/ar/select")
def select_game_type_ar():
    return render_template('ar-select-game.html')


@app.route("/en/select")
def select_game_type_en():
    return render_template('en-select-game.html')


@app.route("/en/rec/select")
@app.route("/en/ai/select")
def select_song_en():
    return render_template('en-select-song.html')


@app.route("/ar/rec/select")
@app.route("/ar/ai/select")
def select_song_ar():
    return render_template('ar-select-song.html')


@app.route("/en/rec/select/search", methods=['GET', 'POST'])
@app.route("/en/ai/select/search", methods=['GET', 'POST'])
def load_search_en():
    if request.method == 'POST':
        try:
            videosSearch = VideosSearch(
                request.form['searchterms'], limit=5)
            return render_template('en-select-song.html', results=videosSearch.result()['result'])
        except:
            if os.path.exists("./Video/vid.mp4"):
                os.remove("./Video/vid.mp4")
            YouTube(request.form['youtubeid']).streams.get_highest_resolution(
            ).download(output_path='./Video', filename='vid.mp4')
            video = VideoFileClip(r'./Video/vid.mp4').set_duration(13)
            if os.path.exists("./Audio/song.wav"):
                os.remove("./Audio/song.wav")
            video.audio.write_audiofile(r"./Audio/song.wav")
            print("Complete")
            print("Generating the dance")
            # os.system("python Learning2Dance/main_orjwan.py -p test --input Audio/song.wav --cpk_path Learning2Dance/weights/generator.pt --audio_ckp Learning2Dance/weights/audio_classifier.pt --out_video ./PoseVideos --fps 30")
            print("Done generating")
            # print("Fixing codec and attaching audio")
            # video = VideoFileClip('./PoseVideos/output/output_black.mp4')
            # video.audio = CompositeAudioClip(
            # [AudioFileClip('./Audio/song.wav')])
            # if os.path.exists("./static/img/2.mp4"):
            # os.remove("./static/img/2.mp4")
            # video.write_videofile("static/img/2.mp4", codec='libx264')
            return render_template('en-select-song.html')
        return render_template('en-select-song.html')


@app.route("/ar/rec/select/search", methods=['GET', 'POST'])
@app.route("/ar/ai/select/search", methods=['GET', 'POST'])
def load_search_ar():
    if request.method == 'POST':
        try:
            videosSearch = VideosSearch(
                request.form['searchterms'], limit=5)
            return render_template('ar-select-song.html', results=videosSearch.result()['result'])
        except:
            if os.path.exists("./Video/vid.mp4"):
                os.remove("./Video/vid.mp4")
            YouTube(request.form['youtubeid']).streams.get_highest_resolution(
            ).download(output_path='./Video', filename='vid.mp4')
            video = VideoFileClip(r'./Video/vid.mp4').set_duration(13)
            if os.path.exists("./Audio/song.wav"):
                os.remove("./Audio/song.wav")
            video.audio.write_audiofile(r"./Audio/song.wav")
            print("Complete")
            print("Generating the dance")
            # os.system("python Learning2Dance/main_orjwan.py -p test --input Audio/song.wav --cpk_path Learning2Dance/weights/generator.pt --audio_ckp Learning2Dance/weights/audio_classifier.pt --out_video ./PoseVideos --fps 30")
            # print("Done generating")
            # print("Fixing codec and attaching audio")
            # video = VideoFileClip('./PoseVideos/output/output_black.mp4')
            # video.audio = CompositeAudioClip(
            # [AudioFileClip('./Audio/song.wav')])
            # if os.path.exists("./static/img/2.mp4"):
            # os.remove("./static/img/2.mp4")
            # video.write_videofile("static/img/2.mp4", codec='libx264')
            return render_template('ar-select-song.html')
    elif request.method == 'GET':
        return render_template('ar-select-song.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/search')
# def search():


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        try:
            print("Downloading video")
            if os.path.exists("./Video/vid.mp4"):
                os.remove("./Video/vid.mp4")
            YouTube(request.form['youtubeid']).streams.get_highest_resolution(
            ).download(output_path='./Video', filename='vid.mp4')
            print("Converting to audio")
            video = VideoFileClip(r'./Video/vid.mp4').set_duration(13)
            if os.path.exists("./Audio/song.wav"):
                os.remove("./Audio/song.wav")
            video.audio.write_audiofile(r"./Audio/song.wav")
            print("Complete")
            print("Generating the dance")
            os.system("python Learning2Dance/main_orjwan.py -p test --input Audio/song.wav --cpk_path Learning2Dance/weights/generator.pt --audio_ckp Learning2Dance/weights/audio_classifier.pt --out_video ./PoseVideos --fps 30")
            print("Done generating")
            print("Fixing codec and attaching audio")
            video = VideoFileClip('./PoseVideos/output/output_black.mp4')
            video.audio = CompositeAudioClip(
                [AudioFileClip('./Audio/song.wav')])
            if os.path.exists("./static/img/2.mp4"):
                os.remove("./static/img/2.mp4")
            video.write_videofile("static/img/2.mp4", codec='libx264')
            return render_template('game.html', success="Success")
        except:
            print("Oops, something went wrong. Try again.")
            print(traceback.format_exc())
            return render_template('game.html', error="Something went wrong.")
    elif request.method == 'GET':
        return render_template('game.html')


if __name__ == "__main__":
    app.run(debug=True)
