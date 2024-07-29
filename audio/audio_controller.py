import os
from flask import request, jsonify
from moviepy.editor import VideoFileClip
from .audio_service import AudioService

class AudioController:
    def __init__(self, audio_service: AudioService):
        self.audio_service = audio_service
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    def upload_and_send_audio(self):
        if 'video' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['video']
        video_upload_folder = os.path.join(self.base_path, 'video_data')
        audio_upload_folder = os.path.join(self.base_path, 'audio_data')

        # Ensure directories exist
        try:
            if not os.path.exists(video_upload_folder):
                os.makedirs(video_upload_folder)
            if not os.path.exists(audio_upload_folder):
                os.makedirs(audio_upload_folder)
        except Exception as error:
            print(f"Error creating directories: {str(error)}")
            return jsonify({"error": "Failed to create directories"}), 500

        video_path = os.path.join(video_upload_folder, file.filename)
        audio_path = os.path.join(audio_upload_folder, f"{os.path.splitext(file.filename)[0]}.mp3")

        try:
            file.save(video_path)
        except Exception as error:
            print(f"Error saving video file: {str(error)}")
            return jsonify({"error": "Failed to save video file"}), 500

        language = request.form.get('language', 'en')

        try:
            # Extract audio from video
            self.extract_audio_from_video(video_path, audio_path)
            result = self.audio_service.save_and_send_audio(audio_path, language)
            return jsonify(result)
        except Exception as error:
            print(f"Error: {str(error)}")  # Log the error
            return jsonify({"error": str(error)}), 500
        finally:
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as error:
                print(f"Error deleting file: {str(error)}")  # Log the error

    def extract_audio_from_video(self, video_path, audio_path):
        try:
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(audio_path)
            audio_clip.close()
            video_clip.close()
        except Exception as error:
            print(f"Error extracting audio: {str(error)}")  # Log the error
            raise Exception(f"Failed to extract audio from video: {str(error)}")

    def analyze_speech_text(self):
        data = request.get_json()
        text = data.get('text')
        language = data.get('language', 'en')

        if not text:
            return jsonify({"error": "No text provided for analysis"}), 400

        try:
            prompt_file = 'prompt1.txt' if language == 'en' else 'prompt2.txt'
            prompt_path = os.path.join(self.base_path, prompt_file)
            with open(prompt_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
                prompt_template = file.read()

            prompt = prompt_template.replace("${text}", text)

            gpt_response = self.audio_service.analyze_text_with_gpt(prompt)
            return jsonify({"gpt_response": gpt_response})
        except Exception as error:
            print(f"Error: {str(error)}")  # Log the error
            return jsonify({"error": str(error)}), 500
