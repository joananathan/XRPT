from flask import Flask, render_template, request, redirect, url_for, flash
import os
import download


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecurekey'
app.config['UPLOAD_FOLDER'] = 'videos'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_file = request.files.get('video_file')
        youtube_url = request.form.get('youtube_url')
        if video_file and youtube_url:
            flash("Please provide only one input: either upload a file or provide a YouTube URL.", "error")
            return redirect(url_for('home'))

        if not video_file and not youtube_url:
            flash("Please provide a video file or a YouTube URL.", "error")
            return redirect(url_for('home'))

        clip_length = int(request.form.get('clip_length', 60))
        caption_style = request.form.get('caption_style', 'default')
        num_clips = int(request.form.get('num_clips', 1))

        print(clip_length, caption_style, num_clips)
        
        folder = "videos"
        for filename in os.listdir(folder):
            file = os.path.join(folder, filename)
            if os.path.isfile(file):
                os.remove(file)
                
        if video_file:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_video.mp4')
            video_file.save(video_path)
            
        elif youtube_url:
            download.download_yt(youtube_url)


        flash("Video processing started.", "success")
        return redirect(url_for('home'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)