from flask import Flask, request, jsonify
import openai
import requests
import os

# Create Flask app
app = Flask(__name__)

# Get API keys from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Ensure API keys are set
if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Make sure it's set in the environment variables.")
if not google_maps_api_key:
    raise ValueError("Google Maps API key is missing. Make sure it's set in the environment variables.")

# Endpoint for diagnosing based on image and symptoms
@app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        # Get the image data and symptoms from the request
        data = request.get_json()
        image_data = data.get('image_data')
        symptoms = data.get('symptoms')

        if not image_data or not symptoms:
            return jsonify({"error": "Both image_data and symptoms are required"}), 400

        # Step 1: Mock call to OpenAI Vision API for image analysis (as a placeholder)
        vision_result = call_vision_api(image_data)

        # Step 2: Call GPT-4 API to generate a diagnosis based on vision analysis and symptoms
        diagnosis = call_gpt4_api(vision_result, symptoms)

        return jsonify({"diagnosis": diagnosis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Mock function to simulate OpenAI Vision API
def call_vision_api(image_data):
    return "mocked_vision_result"

# Function to call GPT-4 API for diagnosis
def call_gpt4_api(vision_result, symptoms):
    try:
        prompt = f"Given this skin analysis: {vision_result} and these symptoms: {symptoms}, what is the diagnosis?"
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=300
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error calling GPT-4 API: {str(e)}"

# Endpoint for finding nearby hospitals based on location
@app.route('/hospitals', methods=['POST'])
def find_hospitals():
    try:
        # Get location from the request (e.g., "37.7749,-122.4194")
        data = request.get_json()
        location = data.get('location')

        if not location:
            return jsonify({"error": "Location is required"}), 400

        # Call the Google Maps Places API to get nearby hospitals
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=5000&type=hospital&key={google_maps_api_key}"
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": f"Error fetching hospitals: {response.status_code}"}), 500

        hospitals = response.json().get('results', [])

        return jsonify(hospitals)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
