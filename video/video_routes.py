from flask import Blueprint
from .video_controller import VideoController

video_router = Blueprint('video_router', __name__)
video_controller = VideoController()

@video_router.route('/upload', methods=['POST'])
def upload_video():
    return video_controller.upload_video()
