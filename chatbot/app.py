from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the Gemini API key
GEMINI_API_KEY = 'AIzaSyDJoyChEYC8FLHWHY6sfE257P8-hVSPJmI'
genai.configure(api_key=GEMINI_API_KEY)

# Create a model instance
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Store Indo field data (back-end only)
indo_field_data = []

# Adding a detailed description of Sampreethi and her friends
sampreethi_info = """
There is a girl named Sampreethi, affectionately called Sampi. She is currently studying at Vivekananda College, pursuing a Bachelor of Pharmacy. 
We jokingly refer to her as "Syrup Doctor" because making syrup is part of her academic curriculum. 
A humorous saying among us is that if a patient comes to her, only God can save them, implying she might not be the best doctor yet! 
Sampi has a brother named Sampu and many friends, including Bharath, who is an engineer; Sharath; Sowmya; Ranjith; Deviprasad; and Durga Prasad, who has an entrepreneurial mindset and works as a software engineer. 
Her best friend is Vishwas, whom she loves the most. Gayatri Mausi is her favorite person.

Sampi loves to talk and is very respectful. We often call Vishwas by his nickname "Bhatta" in college. 
The nickname "Syrup" combines both Sampi's and Vishwas's names and also humorously suggests poison. 
Additionally, Sampi is sometimes called "Kiulli" because she is short in stature.

Overall, Sampi has a vibrant personality and a close-knit group of friends who support each other in their academic and personal endeavors.
"""

# Appending the information to the list
indo_field_data.append(sampreethi_info)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"reply": "Please provide a valid input."})

    # Prepare the initial context with Sampreethi's information
    initial_context = sampreethi_info.strip()

    # Send the user's message along with the context to the generative model
    try:
        chat = model.start_chat()
        # Combine initial context with user input for the generative model
        combined_input = f"{initial_context}\nUser: {user_input}"
        response = chat.send_message(combined_input)
        ai_reply = response.text.strip()
    except Exception as e:
        ai_reply = f"Error: {str(e)}"

    return jsonify({"reply": ai_reply})

@app.route('/add_indo', methods=['POST'])
def add_indo_data():
    new_info = request.json.get("info")
    if new_info:
        indo_field_data.append(new_info)
        return jsonify({"message": "Information added to Indo field."})
    return jsonify({"message": "No information provided."})

@app.route('/get_indo', methods=['GET'])
def get_indo_data():
    return jsonify({"indo_data": indo_field_data})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
