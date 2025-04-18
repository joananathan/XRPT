from flask import Flask, render_template, request, redirect, url_for, flash
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecurekey'
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the video source (either file or YouTube link)
        video_file = request.files.get('video_file')
        youtube_url = request.form.get('youtube_url')

        if video_file and youtube_url:
            flash("Please provide only one input: either upload a file or provide a YouTube URL.", "error")
            return redirect(url_for('home'))

        if not video_file and not youtube_url:
            flash("Please provide a video file or a YouTube URL.", "error")
            return redirect(url_for('home'))

        # Get the options
        clip_length = int(request.form.get('clip_length', 60))
        caption_style = request.form.get('caption_style', 'default')
        num_clips = int(request.form.get('num_clips', 1))

        # Process based on input
        print(clip_length, caption_style, num_clips)
        # if video_file:
        #     video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        #     video_file.save(video_path)
        #     from process_video_file import process_uploaded_video
        #     process_uploaded_video(video_path, clip_length, caption_style, num_clips)
        # elif youtube_url:
        #     from process_youtube_link import process_youtube_video
        #     process_youtube_video(youtube_url, clip_length, caption_style, num_clips)

        flash("Video processing started.", "success")
        return redirect(url_for('home'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)