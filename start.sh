#!/bin/bash

# Activate venv
source venv/bin/activate

# Run Flask App
export FLASK_APP=flaskr
export FLASK_ENV=development
export GOOGLE_VISION_API_KEY="<API Key of Vision API>"
export REMOTE_URL=http://127.0.0.1:5508

flask run --port=5508
