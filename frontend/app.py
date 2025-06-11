import streamlit as st
import socketio
import asyncio

# Socket.IO client
sio = socketio.AsyncClient()

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'connected' not in st.session_state:
    st.session_state['connected'] = False

if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ""

async def connect_to_server():
    try:
        await sio.connect('http://backend:5000')
        print("Connected to server!")
        st.session_state['connected'] = True
    except Exception as e:
        print(f"Connection failed: {e}")
        st.session_state['connected'] = False

async def send_message(message):
    if st.session_state['connected'] and message.strip():
        await sio.emit('message', {'message': message.strip()})
        st.session_state['chat_history'].append({'user': 'You', 'message': message.strip()})
        st.session_state['input_text'] = ""  # Clear input after sending
    else:
        st.warning("Not connected to the server. Please wait...")

async def receive_message(data):
    st.session_state['chat_history'].append({'user': 'Bot', 'message': data['message']})
    st.experimental_rerun()  # re-run Streamlit to update UI

async def main():
    st.title("Ollama Chat with Streamlit")

    # Connect once if not connected
    if not st.session_state['connected']:
        await connect_to_server()

        @sio.on('bot_message')
        async def on_message(data):
            await receive_message(data)

    # Controlled input text linked to session_state
    input_message = st.text_input("Your message:", key='input_text')

    send_clicked = st.button("Send")

    if send_clicked and input_message.strip():
        await send_message(input_message)

    # Display chat history
    for chat in st.session_state['chat_history']:
        align = "right" if chat["user"] == "You" else "left"
        color = "blue" if chat["user"] == "You" else "green"
        st.markdown(
            f'<div style="text-align: {align}; color: {color};"><strong>{chat["user"]}: </strong>{chat["message"]}</div>',
            unsafe_allow_html=True)

if __name__ == '__main__':
    asyncio.run(main())
