from flask import Flask, request, jsonify
import openai
import requests
import os  # Import os to access environment variables

# Create Flask app
app = Flask(__name__)

# Set up your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Access the Google Maps API key from environment variable
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Endpoint for diagnosing based on image and symptoms
@app.route('/diagnose', methods=['POST'])
def diagnose():
    # Get the image data and symptoms from the request
    data = request.json
    image_data = data['image_data']
    symptoms = data['symptoms']

    # Step 1: Mock call to OpenAI Vision API for image analysis
    vision_result = call_vision_api(image_data)

    # Step 2: Use GPT-4 API to provide a diagnosis based on image analysis and symptoms
    diagnosis = call_gpt4_api(vision_result, symptoms)

    return jsonify({"diagnosis": diagnosis})

# Mock function to simulate OpenAI Vision API
def call_vision_api(image_data):
    return "mocked_vision_result"

# Function to call GPT-4 API to generate diagnosis
def call_gpt4_api(vision_result, symptoms):
    prompt = f"Given this skin analysis: {vision_result} and these symptoms: {symptoms}, what is the diagnosis?"
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=300
    )
    return response['choices'][0]['text']

# Endpoint for finding nearby hospitals based on location
@app.route('/hospitals', methods=['POST'])
def find_hospitals():
    location = request.json['location']  # Example: "37.7749,-122.4194" (latitude, longitude)

    # Use the Google Maps API key from environment variable
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=5000&type=hospital&key={google_maps_api_key}"
    response = requests.get(url)
    hospitals = response.json()['results']

    return jsonify(hospitals)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
