from flask import Flask, request, render_template, jsonify
import os
import requests

app = Flask(__name__)

# Set the API key as an environment variable (for security, you can set this in your environment directly).
os.environ['API_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imtlc2F2LnNhbnRob3NoQHN0cmFpdmUuY29tIn0.w6n7WvhB4h5hpb7ZjQIZf5LiRxnJnqlM10O-N8gPuK8'  # Replace this with your actual API key

@app.route('/')
def index():
    # Render the HTML page with a form
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    # Get data from the form submission
    sentence = request.form['sentence']
    language = request.form.get('language')
    
    # Define the target language based on the input
    target_language = 'hi' if language == 'hindi' else 'en'
    # API request to translate the input
    response = requests.post(
        "https://llmfoundry.straive.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['API_KEY']}:my-test-project"},  # Access the API key using the environment variable name
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": f"Translate this into {target_language},all words in that language only, just give one sentence and only the sentence, not anything else with it: {sentence}"}
            ]
        }
    )
    # Process the API response
    if response.status_code == 200:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        return jsonify({"translated_text": content})
    else:
        return jsonify({"error": f"Request failed with status code: {response.status_code}"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
