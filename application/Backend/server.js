// A simple Express.js server for the R3ÆLƎR AI backend

const express = require('express');
const app = express();
const port = 3000; // You can change this port if needed

// This line allows our server to understand JSON sent from the frontend
app.use(express.json());

// This is the API endpoint the frontend is calling
app.post('/api/process-command', (req, res) => {
  // The user's spoken text is in the 'body' of the request
  const userText = req.body.text;

  console.log(`[Backend] Received command: "${userText}"`);

  // --- THIS IS WHERE YOUR AI LOGIC WILL GO ---
  // For now, we'll just create a simple, placeholder response.
  let aiResponseText = '';
  if (userText.toLowerCase().includes('hello')) {
    aiResponseText = 'Hello. I am R3ÆLƎR AI. How can I assist you?';
  } else {
    aiResponseText = `Command acknowledged. You said: ${userText}`;
  }
  // ---------------------------------------------

  // Send the response back to the frontend in the correct format
  res.json({
    responseText: aiResponseText,
  });
});

// Start the server and listen for requests
app.listen(port, () => {
  console.log(`[Backend] R3ÆLƎR AI server is online and listening on http://localhost:${port}`);
});
