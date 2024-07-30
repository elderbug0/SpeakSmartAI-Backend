import os
import time
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyBbM4yocZZEj550euQasJXJhLsT-O0E3Z4"
genai.configure(api_key=GEMINI_API_KEY)

def update_status(status):
    # Print the status, replacing the previous one
    print(f"\r{status}", end="", flush=True)
    # Also write the status to a log file for record-keeping
    with open('process.txt', 'w') as file:
        file.write(status + '\n')

def upload_to_gemini(path, mime_type=None):
    update_status('Starting video upload...')
    file = genai.upload_file(path, mime_type=mime_type)
    update_status(f"Successfully uploaded '{file.display_name}'. Processing...")
    return file

def wait_for_files_active(files):
    update_status("Processing video. Please wait...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            update_status("Processing video... Almost done.")
            time.sleep(2)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"Processing of file {file.name} failed.")
    update_status("Video processing complete!")

def get_prompt(language):
    base_path = os.path.dirname(os.path.abspath(__file__))
    prompt_file = 'prompt1g.txt' if language == 'en' else 'prompt2g.txt'
    prompt_path = os.path.join(base_path, prompt_file)
    with open(prompt_path, 'r', encoding="utf-8") as file:
        return file.read()

def analyze_video(video_path, language):
    try:
        update_status('Starting video analysis...')
        uploaded_file = upload_to_gemini(video_path, mime_type="video/mp4")
        wait_for_files_active([uploaded_file])

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash"
        )

        prompt = get_prompt(language)
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        uploaded_file,
                    ],
                },
            ]
        )

        update_status("Analyzing the video. Please wait...")
        response = chat_session.send_message(prompt)
        update_status("Video analysis complete!")
        return response.text
        
    except Exception as e:
        update_status('An error occurred during video analysis')
        print(f"\nError in analyze_video: {str(e)}")
        raise

def delete_uploaded_files(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"\rDeleted file: {file_path}", end="", flush=True)
    except Exception as e:
        print(f"\nError in delete_uploaded_files: {str(e)}")
        raise

# Example usage:
# result = analyze_video('path_to_your_video.mp4', 'en')
# print(result)