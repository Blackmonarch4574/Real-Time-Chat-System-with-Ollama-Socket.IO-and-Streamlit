

# 🧠 Real-Time LLM Chat App with Ollama + Streamlit + Socket.IO

## Features
- Run a **local LLM** using Ollama (supports models like LLaMA 3)
- Real-time **async communication** via Flask + Socket.IO
- Multi-user web interface using **Streamlit**
- Fully **Dockerized** setup

---

## Prerequisites
- Docker and Docker Compose installed

---

## Setup Instructions

```bash
git clone https://github.com/yourusername/ollama-chat-app.git
cd ollama-chat-app
chmod +x models/ollama-model-pull.sh
./models/ollama-model-pull.sh
```

Then run:
```bash
docker-compose up --build
```

Access the app at: [http://localhost:8501](http://localhost:8501)


## Architecture
- `ollama`: runs local LLM model server
- `backend`: handles real-time socket communication and routes prompts to LLM
- `frontend`: Streamlit interface for users to chat with the model


## Notes
- You can change the model in `backend/app.py` and pull it using `ollama pull <model>`
- Tested with llama3 and mistral models

## License
MIT

Let me know your GitHub username so I can customize the README further. Once confirmed, you can copy this full project structure into your GitHub repo and deploy. Let me know if you want a `.zip` version or CI/CD support too.
