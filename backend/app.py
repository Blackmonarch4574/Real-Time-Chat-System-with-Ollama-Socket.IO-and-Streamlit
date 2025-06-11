import socketio
import asyncio
import ollama
import os

# Initialize Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asyncio')
app = socketio.ASGIApp(sio, static_files={'/': './public'})

# Ollama model (set as environment variable, default to llama3)
MODEL = os.environ.get("OLLAMA_MODEL", "llama3")

print(f"Using model: {MODEL}")

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.on('message')
async def handle_message(sid, data):
    user_message = data['message']
    print(f"Received message from {sid}: {user_message}")

    try:
        # Stream responses from Ollama
        response_stream = await ollama.astream(
            model=MODEL,
            prompt=user_message,
            stream=True
        )

        full_response = ""
        async for part in response_stream:
            if 'response' in part:
                response_text = part['response']
                full_response += response_text
                await sio.emit('bot_message', {'message': response_text}, room=sid) # Send incrementally

        print(f"Full response to {sid}: {full_response}")

    except Exception as e:
        error_message = f"Error generating response: {e}"
        print(error_message)
        await sio.emit('bot_message', {'message': error_message}, room=sid)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
