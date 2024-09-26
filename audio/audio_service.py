import os
import requests
import openai

class AudioService:
    def __init__(self):
        self.auth_token = ''
        self.openai_api_key = ''
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }
        openai.api_key = self.openai_api_key

    def save_and_send_audio(self, file_path, language):
        url = "https://api.edenai.run/v2/audio/speech_to_text_async"
        data = {
            "providers": "openai",
            "language": language,
        }

        try:
            with open(file_path, 'rb') as audio_file:
                files = {'file': audio_file}
                response = requests.post(url, data=data, files=files, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error in save_and_send_audio: {error.response.text}")  # Log detailed error response
            raise Exception(f"Failed to analyze audio: {str(error)}")

    def analyze_text_with_gpt(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": prompt},
                ]
            )
            return response.choices[0].message['content'].strip()
        except Exception as error:
            print(f"Error in analyze_text_with_gpt: {str(error)}")
            raise Exception(f"Failed to analyze text with GPT-4: {str(error)}")

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
        except Exception as error:
            print(f"Error deleting file: {str(error)}")
            raise Exception(f"Failed to delete file: {str(error)}")
