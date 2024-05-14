# Tourism Companion API

The Tourism Companion API is designed to assist users with travel-related inquiries. It provides information about tourist attractions, landmarks, cultural sites, travel advice, language translation, image descriptions, and more. It also supports GPS-based searches for nearby places like restaurants, hotels, and tourist spots.

## Table of Contents

- [API Endpoints](#api-endpoints)
  - [Chat](#chat)
- [Request and Response Schemas](#request-and-response-schemas)
  - [Chat Request](#chat-request)
  - [Chat Response](#chat-response)
- [Setup Instructions](#setup-instructions)
- [Calling the API from a Node.js Application](#calling-the-api-from-a-nodejs-application)
  - [Example Code](#example-code)
    - [Text Request](#text-request)
    - [Audio Request](#audio-request)
    - [Image Request](#image-request)
    - [GPS-Based Search Request](#gps-based-search-request)
- [Conclusion](#conclusion)

## API Endpoints

### Chat

- **Endpoint:** `/api/v1/chat/`
- **Method:** `POST`
- **Description:** Handles chat requests, including text, audio, image inputs, and web searches. Determines if the request needs GPS information to find nearby places like restaurants, hotels, or tourist spots.

## Request and Response Schemas

### Chat Request

```json
{
  "text": "string",
  "file": "binary",
  "image": "binary",
  "gps_position": "string",
  "place_type": "string",
  "user_id": "integer",
  "target_lang": "string"
}
```

- **text:** Optional string. User's text input.
- **file:** Optional binary. Audio file input.
- **image:** Optional binary. Image file input.
- **gps_position:** Optional string. GPS coordinates (latitude, longitude).
- **place_type:** Optional string. Type of place to search for (e.g., restaurants, hotels).
- **user_id:** Required integer. User's ID.
- **target_lang:** Required string. Target language for translation.

### Chat Response

```json
{
  "response": "string",
  "session_id": "integer"
}
```

- **response:** AI's response to the user's query.
- **session_id:** Session ID for the conversation.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/tourism-companion-api.git
   cd tourism-companion-api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file with the following content:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   DATABASE_URL=sqlite:///./conversations.db
   GOOGLE_API_KEY=your-google-api-key
   GOOGLE_CSE_ID=your-google-cse-id
   ```

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Calling the API from a Node.js Application

### Example Code

Install the required packages:

```bash
npm install axios form-data
```

#### Text Request

```javascript
const axios = require('axios');

const chatText = async (text, userId, targetLang) => {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/chat/', {
      text: text,
      user_id: userId,
      target_lang: targetLang,
    });
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};

// Usage
chatText('Tell me about the Eiffel Tower', 1, 'en');
```

#### Audio Request

```javascript
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

const chatAudio = async (filePath, userId, targetLang) => {
  try {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('user_id', userId);
    form.append('target_lang', targetLang);

    const response = await axios.post('http://localhost:8000/api/v1/chat/', form, {
      headers: {
        ...form.getHeaders(),
      },
    });

    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};

// Usage
chatAudio('./path_to_audio_file.wav', 1, 'en');
```

#### Image Request

```javascript
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

const chatImage = async (filePath, userId, targetLang) => {
  try {
    const form = new FormData();
    form.append('image', fs.createReadStream(filePath));
    form.append('user_id', userId);
    form.append('target_lang', targetLang);

    const response = await axios.post('http://localhost:8000/api/v1/chat/', form, {
      headers: {
        ...form.getHeaders(),
      },
    });

    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};

// Usage
chatImage('./path_to_image_file.jpg', 1, 'en');
```

#### GPS-Based Search Request

```javascript
const axios = require('axios');

const chatGPS = async (text, gpsPosition, userId, targetLang) => {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/chat/', {
      text: text,
      gps_position: gpsPosition,
      user_id: userId,
      target_lang: targetLang,
    });
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};

// Usage
chatGPS('Find nearby restaurants', '40.748817,-73.985428', 1, 'en');
```

## Conclusion

The Tourism Companion API provides comprehensive functionalities to assist users with travel-related inquiries. By integrating various tools and using LangChain's capabilities, the API can handle text, audio, image, and GPS-based requests, offering a robust solution for enhancing the travel experience.
