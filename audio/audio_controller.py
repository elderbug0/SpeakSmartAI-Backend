import os
from flask import request, jsonify
from .audio_service import AudioService

class AudioController:
    def __init__(self, audio_service: AudioService):
        self.audio_service = audio_service
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    def upload_and_send_audio(self):
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        file = request.files['audio']
        audio_upload_folder = os.path.join(self.base_path, 'audio_data')

        # Ensure directory exists
        try:
            if not os.path.exists(audio_upload_folder):
                os.makedirs(audio_upload_folder)
        except Exception as error:
            print(f"Error creating directory: {str(error)}")
            return jsonify({"error": "Failed to create directory"}), 500

        audio_path = os.path.join(audio_upload_folder, file.filename)

        try:
            file.save(audio_path)
        except Exception as error:
            print(f"Error saving audio file: {str(error)}")
            return jsonify({"error": "Failed to save audio file"}), 500

        language = request.form.get('language', 'en')

        try:
            result = self.audio_service.save_and_send_audio(audio_path, language)
            return jsonify(result)
        except Exception as error:
            print(f"Error: {str(error)}")  # Log the error
            return jsonify({"error": str(error)}), 500
        finally:
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as error:
                print(f"Error deleting file: {str(error)}")  # Log the error

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
