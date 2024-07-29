from flask import Blueprint
from audio.audio_routes import audio_router
from video.video_routes import video_router

global_router = Blueprint('global_router', __name__)
global_router.register_blueprint(audio_router, url_prefix='/audio')
global_router.register_blueprint(video_router, url_prefix='/video')
