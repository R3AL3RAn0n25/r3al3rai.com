import express from 'express';
import axios from 'axios';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'build')));

app.post('/api/auth/register', async (req, res) => {
  const { username, password } = req.body;
  try {
    if (!username || !password) {
      return res.status(400).json({ success: false, error: 'Username and password required' });
    }
    const password_hash = password; // Replace with bcrypt.hash in production
    res.json({ success: true, message: 'User registered' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.post('/api/auth/login', async (req, res) => {
  const { username, password } = req.body;
  if (username === 'testuser' && password === 'password123') {
    const token = jwt.sign({ username }, process.env.JWT_SECRET || 'secret', { expiresIn: '1h' });
    res.json({ success: true, token });
  } else {
    res.json({ success: false, error: 'Invalid credentials' });
  }
});

app.post('/api/thebrain', async (req, res) => {
  const { userInput, user_id, conversation_history } = req.body;
  try {
    const response = await axios.post(
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent',
      { contents: [{ parts: [{ text: userInput }] }] },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${process.env.GEMINI_API_KEY}`,
        },
      }
    );
    res.json({ success: true, response: response.data.candidates[0].content.parts[0].text });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.get('/api/status', (req, res) => {
  res.json({ status: 'idle' });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(process.env.PORT || 3000, '0.0.0.0', () => console.log('Server running on port 3000'));