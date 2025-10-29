"""
droid.py - The AI Agent and Web Server
This module contains the R3al3rDroid class and the Flask web server
that connects the AI agent to the frontend interface.
"""
import logging
import os
from datetime import datetime
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import the KillSwitch from our helper file
from innovations import KillSwitch

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- The AI Droid Class (Your Original Logic) ---
class R3al3rDroid:
    """The personalized, adaptive AI assistant."""
    def __init__(self, user_id, mongo_uri):
        self.user_id = user_id
        self.adaptability = 0
        self.kill_switch = KillSwitch()
        self.user_profile = { 'likes': [], 'dislikes': [], 'habits': [], 'financial_goals': [] }
        try:
            # Added a timeout to prevent the app from hanging on connection issues
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client["r3al3r_db"]
            self.profiles = self.db["user_profiles"]
            # Test the connection
            self.client.server_info()
            logging.info(f"R3al3rDroid for user {self.user_id} connected to MongoDB.")
        except Exception as e:
            logging.error(f"R3al3rDroid MongoDB connection failed: {e}")
            raise

    def adapt_to_user(self, user_data):
        """Adapts the droid's internal user profile based on user interactions."""
        if self.kill_switch.is_active():
            raise RuntimeError("Kill switch active, adaptation is disabled.")
        if self.adaptability < 5:
            self.adaptability += 1
        if isinstance(user_data, dict) and "intent" in user_data:
            intent = user_data["intent"]
            if intent == "personalize":
                entities = user_data.get("entities", [])
                self.user_profile['likes'].extend([e["value"] for e in entities if e.get("entity") == "like"])
                self.user_profile['dislikes'].extend([e["value"] for e in entities if e.get("entity") == "dislike"])
        try:
            self.profiles.update_one({"user_id": self.user_id}, {"$set": self.user_profile}, upsert=True)
            logging.info(f"R3al3rDroid adapted for user {self.user_id}.")
        except Exception as e:
            logging.error(f"Failed to update user profile for {self.user_id}: {e}")
            raise RuntimeError(f"Profile update failed: {e}")

    def process_chat(self, user_text):
        """Processes incoming text from the user and generates a response."""
        logging.info(f"Processing chat for user {self.user_id}: '{user_text}'")
        # --- THIS IS WHERE YOUR CORE AI LOGIC WILL GO ---
        # For now, it provides a simple echo response.
        # You can expand this to call your knowledge bases, language models, etc.
        if "hello" in user_text.lower():
            return "Hello. I am R3ÆLƎR AI. System status: online and adaptive."
        else:
            return f"Command acknowledged: '{user_text}'. Processing..."
        # -------------------------------------------------


# --- Flask Web Server Setup ---
app = Flask(__name__)
# This is crucial: It allows your frontend to make requests to this backend.
CORS(app)

# --- Initialize the Droid ---
# For security, get the MongoDB connection string from an environment variable
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    logging.error("FATAL: MONGO_URI environment variable not set.")
    # In a real app, you might exit here, but we'll let it raise an error in the droid init
    # to make debugging clearer.

# We'll create a single droid instance for a default user for now.
# In a real multi-user system, you would manage instances per user session.
try:
    droid_instance = R3al3rDroid(user_id="default_user", mongo_uri=MONGO_URI)
except Exception as e:
    droid_instance = None
    logging.error(f"Could not initialize R3al3rDroid. API will respond with errors. Exception: {e}")


# --- API Endpoint for the Frontend ---
@app.route('/api/process-command', methods=['POST'])
def process_command():
    """This is the endpoint the frontend calls."""
    if not droid_instance:
        return jsonify({"responseText": "Error: AI Droid is not initialized. Check MongoDB connection."}), 500

    try:
        data = request.json
        # 1. Get the incoming message from the 'text' key
        user_text = data.get('text', '')

        if not user_text.strip():
            return jsonify({"error": "Message cannot be empty"}), 400

        # 2. Use the droid instance to process the text
        ai_response = droid_instance.process_chat(user_text)

        # 3. Send the response back in the 'responseText' key
        return jsonify({"responseText": ai_response})

    except Exception as e:
        logging.error(f"An error occurred in /api/process-command: {e}")
        return jsonify({"responseText": f"An internal server error occurred: {str(e)}"}), 500


# --- Start the Server ---
if __name__ == "__main__":
    # The server will run on port 3000 to match the frontend's API call
    app.run(host="0.0.0.0", port=3000, debug=True)