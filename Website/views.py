from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for

from urllib.parse import urlparse, parse_qs
from flask_login import login_required, current_user
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import os
from .models import Meme, Note, Jokes, User, Video
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)





@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/about')

def about():
   
    return render_template('about.html', user = current_user)

@views.route('/jokes', methods = ['GET','POST'])
@login_required
def jokes():
    if request.method == 'POST':
        joke = request.form.get('jokes')
        if len(joke) <=1:
            flash('Joke is too short', category='error')
        else:
            new_joke = Jokes(data=joke, user_id=current_user.id)
            db.session.add(new_joke)
            db.session.commit()
            flash('Joke added', category='success')

    return render_template('jokes.html', user = current_user)

@views.route('/delete-jokes', methods=['POST'])
def delete_joke():
    joke_data = json.loads(request.data)
    jokeId = joke_data['jokeId']
    joke = Jokes.query.get(jokeId)
    if joke:
        if joke.user_id == current_user.id:
            db.session.delete(joke)
            db.session.commit()
            return jsonify({'message': 'Joke deleted'}), 200
    return jsonify({'message': 'Joke not found'}), 404

@views.route('/videos', methods=['GET', 'POST'])
@login_required
def upload_video():
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        video_title = request.form.get('video_title')

        if not video_url:
            flash('No video URL provided', category='error')
            return render_template('videos.html', user=current_user)

        yt_video_id = get_youtube_video_id(video_url)
        
        if yt_video_id:
            new_video = Video(yt_video_id=yt_video_id, title=video_title, user_id=current_user.id)
            db.session.add(new_video)
            db.session.commit()
            flash('Video uploaded successfully!', category='success')
            return redirect(url_for('views.upload_video'))
        else:
            flash('Invalid YouTube URL.', category='error')
    
    # For GET requests and after POST redirect
    videos = Video.query.filter_by(user_id=current_user.id).all()
    return render_template('videos.html', user=current_user, videos=videos)

@views.route('/delete-video', methods=['POST'])
@login_required
def delete_video():
    data = json.loads(request.data)
    video_id = data['videoId']
    video = Video.query.get(video_id)
    if video and video.user_id == current_user.id:
        db.session.delete(video)
        db.session.commit()
        return jsonify({'message': 'Video deleted'}), 200
    else:
        return jsonify({'message': 'Video not found'}), 404








def get_youtube_video_id(url):
    if isinstance(url, bytes):
        url = url.decode('utf-8')  # Convert bytes to string if necessary
  
    video_url = request.form.get('video_url')
    print(f'video_url before parsing: {video_url}')
    url_parse = urlparse(url)
        
        

    query_string = parse_qs(url_parse.query)
    video_id = query_string.get("v")

    if video_id:
        return video_id[0]
    if url_parse.path.startswith('/embed/'):
        return url_parse.path.split('/')[2]
    if url_parse.path.startswith('/v/'):
        return url_parse.path.split('/')[2]

    # This covers shortened youtu.be URLs
    if 'youtu.be' in url_parse.netloc:
        return url_parse.path.split('/')[1]

    return None


@views.route('memes', methods=['POST', 'GET'])
@login_required
def memes():
    if request.method == 'POST':
        file = request.files.get('meme_image', None)
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join( 'website', 'static', 'memes', filename).replace('\\', '/')
            file.save(save_path)
            new_meme = Meme(image_path=os.path.join('memes', filename), user_id=current_user.id)
            db.session.add(new_meme)
            db.session.commit()
            flash('Meme uploaded successfully!', category='success')
        return redirect(url_for('views.memes'))
    else:
            flash('No selected file', category='error')
    memes = Meme.query.filter_by(user_id=current_user.id).all()
    return render_template('memes.html', memes=memes,  user=current_user)

@views.route('/delete-meme', methods=['POST'])
@login_required
def delete_meme():
    meme_data = json.loads(request.data)
    memeId = meme_data['memeId']
    meme = Meme.query.get(memeId)
    if meme:
        if meme.user_id == current_user.id:
            db.session.delete(meme)
            db.session.commit()
            return jsonify({'message': 'Meme deleted'}), 200
    return jsonify({'message': 'Meme not found'}), 404



@views.route('/search', methods=['GET', 'POST'])
def search():
    search_query = request.form.get('search') if request.method == 'POST' else ''
    # Perform search across all models only if there is a search query
    if search_query:
        notes_results = Note.query.filter(Note.data.like(f'%{search_query}%')).all()
        jokes_results = Jokes.query.filter(Jokes.data.like(f'%{search_query}%')).all()
        memes_results = Meme.query.filter(Meme.image_path.like(f'%{search_query}%')).all()
        videos_results = Video.query.filter(Video.title.like(f'%{search_query}%')).all()
        user_results = User.query.filter(User.first_name.like(f'%{search_query}%')).all()
        
        # Combine results into a single structure
        results = {
            'notes': notes_results,
            'jokes': jokes_results,
            'memes': memes_results,
            'videos': videos_results,
            'users': user_results
        }
    else:
        # Return empty lists if no search query is provided
        results = {
            'notes': [],
            'jokes': [],
            'memes': [],
            'videos': [],
            'users': []
        }
    
    # Always return the search query and results to avoid 'results' being undefined
    return render_template('search.html', search_query=search_query, results=results, user=current_user)





