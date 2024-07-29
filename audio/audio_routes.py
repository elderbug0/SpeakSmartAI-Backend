# audio_routes.py

from flask import Blueprint
from .audio_service import AudioService
from .audio_controller import AudioController

audio_router = Blueprint('audio_router', __name__)
audio_service = AudioService()
audio_controller = AudioController(audio_service)

audio_router.route('/upload', methods=['POST'])(audio_controller.upload_and_send_audio)
audio_router.route('/analyze-text', methods=['POST'])(audio_controller.analyze_speech_text)

