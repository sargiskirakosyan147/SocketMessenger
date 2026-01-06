# Django WebSocket Chat (Ephemeral & Hashed)

## Description

A Django-based real-time web chat application built with WebSockets. Users join a room by providing a room ID and a username. Messages are ephemeral (no database is used) and are hashed on the server side. Chat history is cleared on page refresh, ensuring privacy and lightweight operation.

## Features

- Real-time communication via WebSockets
- No database storage (in-memory only)
- Server-side message hashing
- Room-based chats
- Chat history cleared on refresh
- Lightweight and privacy-focused

## Requirements

- Python 3.9+
- Virtual environment (recommended)
- Dependencies listed in `requirements.txt`

## Installation (Local / LAN)

### 1. Create a virtual environment

python -m venv venv

### 2. Activate the virtual environment

Windows:
venv\Scripts\activate

macOS / Linux:
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the application

daphne -b 0.0.0.0 -p 8000 chatproject.asgi:application

## Access in Local Network (LAN)

Because the server binds to 0.0.0.0, other devices in the same local network can access the app using:

http://<your-local-ip>:8000

Example:
http://192.168.1.55:8000

## Deployment on a Global Linux Server

For production deployment on a public Linux server, it is recommended to use:

- Gunicorn
- Daphne (ASGI worker)
- Nginx (reverse proxy)
- SSL (Let’s Encrypt)

### Install Gunicorn

pip install gunicorn

### Run with Gunicorn + Daphne worker

gunicorn chatproject.asgi:application \
  -k daphne.chatprotocol.DaphneApplication \
  -b 0.0.0.0:8000

## Security Notes

- Messages are hashed on the server side
- No messages are persisted
- Server memory is cleared on restart
- Designed for temporary, private communication

## License

MIT License
