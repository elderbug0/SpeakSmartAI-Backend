import os
from flask import request, jsonify
from .video_service import analyze_video, delete_uploaded_files

class VideoController:
    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def upload_video(self):
        try:
            if 'video' not in request.files:
                return jsonify({"error": "No file uploaded"}), 400

            file = request.files['video']
            language = request.form.get('language', 'en')  # Default to English if not provided
            video_upload_folder = os.path.join(self.root_path, 'video_data')
            if not os.path.exists(video_upload_folder):
                os.makedirs(video_upload_folder)
            video_path = os.path.join(video_upload_folder, file.filename)
            file.save(video_path)

            try:
                description = analyze_video(video_path, language)
                delete_uploaded_files(video_upload_folder)  # Delete files after processing
                return jsonify({"message": "Video uploaded and processed successfully", "description": description})
            except Exception as error:
                return jsonify({"error": str(error)}), 500

        except Exception as e:
            print(f"Error in upload_video: {str(e)}")
            return jsonify({"error": str(e)}), 500
