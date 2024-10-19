import React, { useState } from 'react';
import axios from 'axios';

function UploadForm() {
    // Define state variables to store form inputs and results
    const [image, setImage] = useState(null);  // To store the image file
    const [symptoms, setSymptoms] = useState("");  // To store the symptoms
    const [diagnosis, setDiagnosis] = useState("");  // To store the diagnosis result
    const [location, setLocation] = useState("");  // To store the location (latitude, longitude)
    const [hospitals, setHospitals] = useState([]);  // To store the nearby hospitals

    // Handle form submission when the user clicks "Submit"
    const handleSubmit = async (e) => {
      e.preventDefault();
  
      // Input validation: Check if image, symptoms, and location are provided
      if (!image || !symptoms || !location) {
          alert("Please provide all inputs: image, symptoms, and location.");
          return;
      }
  
      setLoading(true);  // Start loading when form is submitted
  
      try {
          // Step 1: Use Google Geocoding API to convert place name into coordinates
          const geocodeUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(location)}&key=AIzaSyD1_7YDJWMFcA4TkENRib6Z8qYkZaAN7UU`;
          const geocodeResponse = await axios.get(geocodeUrl);
          const { lat, lng } = geocodeResponse.data.results[0].geometry.location;  // Extract latitude and longitude
  
          // Step 2: Call the Flask backend API for diagnosis
          const diagnosisResponse = await axios.post('http://localhost:5000/diagnose', { image_data: image, symptoms });
          setDiagnosis(diagnosisResponse.data.diagnosis);
  
          // Step 3: Call the Flask backend API for hospitals, using the latitude and longitude from the Geocoding API
          const hospitalResponse = await axios.post('http://localhost:5000/hospitals', { location: `${lat},${lng}` });
          setHospitals(hospitalResponse.data);  // Set the hospitals in state
  
      } catch (error) {
          // Handle any errors that occur
          console.error("Error occurred:", error);
          alert("An error occurred, please try again.");
      } finally {
          setLoading(false);  // Stop loading after API call finishes
      }
  };
  

  return (
    <div>
        {loading ? (
            <p>Loading...</p>  // Show loading message when API calls are in progress
        ) : (
            <form onSubmit={handleSubmit}>
                <label>
                    Upload Image:
                    <input type="file" onChange={(e) => setImage(e.target.files[0])} />
                </label>
                <label>
                    Symptoms:
                    <textarea value={symptoms} onChange={(e) => setSymptoms(e.target.value)} />
                </label>
                <label>
                    Location (Place Name):
                  <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Enter a place name (e.g., New York City)" />
                </label>
                <button type="submit">Submit</button>
            </form>
        )}
    </div>
);
}

export default UploadForm;